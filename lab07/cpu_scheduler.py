from collections import deque


def show_summary(processes, finish_times, first_start):
    total_wait = 0
    total_turnaround = 0
    total_response = 0

    print("\nProcess | Waiting | Turnaround | Response")

    for pid, burst in processes:
        # All processes arrive at time 0.
        turnaround = finish_times[pid]
        waiting = turnaround - burst
        response = first_start[pid]

        total_wait += waiting
        total_turnaround += turnaround
        total_response += response

        print(
            f"{pid:7} | {waiting:7} | "
            f"{turnaround:10} | {response:8}"
        )

    count = len(processes)
    print(f"Average Waiting Time: {total_wait / count:.2f}")
    print(f"Average Turnaround Time: {total_turnaround / count:.2f}")
    print(f"Average Response Time: {total_response / count:.2f}")


def simulate_fcfs(processes):
    print("\n--- FCFS ---")

    current_time = 0
    finish_times = {}
    first_start = {}

    for pid, burst in processes:
        first_start[pid] = current_time
        end_time = current_time + burst

        print(f"[Time {current_time:02d}-{end_time:02d}] {pid}")

        current_time = end_time
        finish_times[pid] = current_time

    show_summary(processes, finish_times, first_start)


def simulate_round_robin(processes, quantum):
    if quantum <= 0:
        raise ValueError("Quantum must be greater than 0.")

    print(f"\n--- Round Robin (Quantum = {quantum}) ---")

    remaining = {pid: burst for pid, burst in processes}
    ready_queue = deque(pid for pid, _ in processes)

    current_time = 0
    finish_times = {}
    first_start = {}

    while ready_queue:
        pid = ready_queue.popleft()

        if pid not in first_start:
            first_start[pid] = current_time

        run_time = min(quantum, remaining[pid])
        end_time = current_time + run_time

        print(f"[Time {current_time:02d}-{end_time:02d}] {pid}")

        current_time = end_time
        remaining[pid] -= run_time

        if remaining[pid] > 0:
            ready_queue.append(pid)
        else:
            finish_times[pid] = current_time

    show_summary(processes, finish_times, first_start)


def main():
    processes = [
        ("P1", 10),
        ("P2", 2),
        ("P3", 3),
    ]

    print("All processes arrive at time 0.")
    print("Time unit: simulated CPU time")
    print("Context-switch overhead is not included.")

    simulate_fcfs(processes)
    simulate_round_robin(processes, quantum=3)


if __name__ == "__main__":
    main()