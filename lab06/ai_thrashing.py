import time
import os


def fast_ram_access(iterations):
    """Simulate processing data held in RAM."""
    simulated_ram = [0.0] * 1000
    start_time = time.perf_counter()

    for _ in range(iterations):
        for i in range(len(simulated_ram)):
            simulated_ram[i] += 1.5

    return time.perf_counter() - start_time


def slow_swap_thrashing_access(iterations, filename="swap_file.bin"):
    """Illustrate repeated file I/O; this does not cause real OS swapping."""
    with open(filename, "wb") as f:
        f.write(b"\x00" * 1000)

    start_time = time.perf_counter()

    for _ in range(iterations):
        with open(filename, "r+b") as f:
            data = bytearray(f.read())

            for i in range(len(data)):
                data[i] = (data[i] + 1) % 255

            f.seek(0)
            f.write(data)

    elapsed = time.perf_counter() - start_time
    os.remove(filename)
    return elapsed


def main():
    iterations = 10000
    print(f"--- Simulation: {iterations:,} Iterations ---")

    print("\n1. Processing in RAM")
    ram_time = fast_ram_access(iterations)
    print(f"Processing time: {ram_time:.4f} seconds")

    print("\n2. Processing with repeated file I/O")
    swap_time = slow_swap_thrashing_access(iterations)
    print(f"Processing time: {swap_time:.4f} seconds")

    ratio = swap_time / ram_time

    print("\n--- SUMMARY ---")
    print(f"RAM time:     {ram_time:.4f} seconds")
    print(f"File I/O time: {swap_time:.4f} seconds")
    print(f"File I/O / RAM time ratio: {ratio:.2f}x")


if __name__ == "__main__":
    main()