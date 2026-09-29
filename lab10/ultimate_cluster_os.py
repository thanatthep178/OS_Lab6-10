import os
import queue
import threading
import time


class AIClusterOS:
    def __init__(self, total_ram_gb, num_gpus):
        self.total_ram_gb = total_ram_gb
        self.available_ram_gb = total_ram_gb
        self.state_lock = threading.Lock()

        self.gpu_locks = {
            i: threading.Lock() for i in range(num_gpus)
        }
        self.gpu_status = {
            i: "IDLE" for i in range(num_gpus)
        }

        self.job_queue = queue.Queue()
        self.active_jobs = []
        self.stop_event = threading.Event()

        self.scheduler_thread = threading.Thread(
            target=self._scheduler_loop
        )
        self.dashboard_thread = threading.Thread(
            target=self._dashboard_loop
        )

        self.scheduler_thread.start()
        self.dashboard_thread.start()

    def show_dashboard(self):
        with self.state_lock:
            print("\n" + "=" * 60)
            print(
                f"[DASHBOARD] RAM Available: "
                f"{self.available_ram_gb}/{self.total_ram_gb} GB"
            )
            print(" | ".join(
                f"GPU {i}: {status}"
                for i, status in self.gpu_status.items()
            ))
            print(
                f"Queue: {self.job_queue.qsize()} | "
                f"Active jobs (including waiting): "
                f"{len(self.active_jobs)}"
            )
            print("=" * 60)

    def _dashboard_loop(self):
        while not self.stop_event.wait(1.5):
            self.show_dashboard()

    def submit_job(
        self, job_name, dataset_path, req_ram, req_gpus, duration
    ):
        if not 0 <= req_ram <= self.total_ram_gb:
            raise ValueError("Invalid RAM request.")
        if duration < 0:
            raise ValueError("Duration cannot be negative.")
        if len(req_gpus) != len(set(req_gpus)):
            raise ValueError("Duplicate GPU IDs.")
        if any(gpu not in self.gpu_locks for gpu in req_gpus):
            raise ValueError("Unknown GPU ID.")

        self.job_queue.put(
            (job_name, dataset_path, req_ram, req_gpus, duration)
        )
        print(f"[API] Submitted: {job_name}")

    def _scheduler_loop(self):
        while not self.stop_event.is_set():
            try:
                job = self.job_queue.get(timeout=0.2)
            except queue.Empty:
                continue

            threading.Thread(
                target=self._execute_job, args=job
            ).start()

    def _execute_job(
        self, job_name, dataset_path, req_ram, req_gpus, duration
    ):
        allocated_ram = False
        acquired_gpus = []
        registered = False

        try:
            # File existence check, as in the lab.
            if not os.path.exists(dataset_path):
                print(f"[{job_name}] FAILED: Dataset not found.")
                return

            # Actually attempt to read the file.
            with open(dataset_path, "rb") as f:
                f.read(1)

            with self.state_lock:
                self.active_jobs.append(job_name)
                registered = True

            print(f"[{job_name}] Waiting for {req_ram} GB RAM...")

            while True:
                with self.state_lock:
                    if self.available_ram_gb >= req_ram:
                        self.available_ram_gb -= req_ram
                        allocated_ram = True
                        break
                time.sleep(0.5)

            print(f"[{job_name}] Allocated {req_ram} GB RAM.")

            # All jobs acquire GPUs in the same order.
            for gpu in sorted(req_gpus):
                self.gpu_locks[gpu].acquire()
                acquired_gpus.append(gpu)

                with self.state_lock:
                    self.gpu_status[gpu] = f"BUSY ({job_name})"

            if acquired_gpus:
                print(f"[{job_name}] Running on GPUs {acquired_gpus}")
            else:
                print(f"[{job_name}] Running on CPU only!")

            time.sleep(duration)
            print(f"[{job_name}] Finished successfully.")

        except OSError as error:
            print(f"[{job_name}] FAILED: {error}")

        finally:
            for gpu in reversed(acquired_gpus):
                with self.state_lock:
                    self.gpu_status[gpu] = "IDLE"
                self.gpu_locks[gpu].release()

            with self.state_lock:
                if allocated_ram:
                    self.available_ram_gb += req_ram
                if registered:
                    self.active_jobs.remove(job_name)

            self.job_queue.task_done()

    def shutdown(self):
        self.job_queue.join()
        self.stop_event.set()
        self.scheduler_thread.join()
        self.dashboard_thread.join()
        self.show_dashboard()
        print("\n=== Cluster OS Shutdown Gracefully ===")


def main():
    dataset = "secure_dataset.csv"

    with open(dataset, "w") as f:
        f.write("dummy data")

    print("=== AI Cluster OS: 64 GB RAM, 4 GPUs (SIMULATED) ===")
    cluster = AIClusterOS(total_ram_gb=64, num_gpus=4)

    cluster.submit_job(
        "Workload_A_LLaMA", dataset,
        req_ram=40, req_gpus=[2, 1, 0], duration=8
    )
    time.sleep(1)

    cluster.submit_job(
        "Workload_B_Preproc", dataset,
        req_ram=16, req_gpus=[], duration=6
    )
    time.sleep(1)

    cluster.submit_job(
        "Workload_C_Infer", dataset,
        req_ram=2, req_gpus=[3], duration=3
    )
    time.sleep(1)

    cluster.submit_job(
        "Workload_D_Hacker", "secret_keys.txt",
        req_ram=1, req_gpus=[], duration=1
    )

    cluster.shutdown()
    os.remove(dataset)


if __name__ == "__main__":
    main()