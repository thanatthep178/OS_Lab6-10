def simulate_fifo(reference_string, num_frames):
    frames = []
    page_faults = 0

    print(f"\n--- FIFO (Frames: {num_frames}) ---")

    for page in reference_string:
        if page not in frames:
            page_faults += 1

            if len(frames) >= num_frames:
                victim = frames.pop(0)
                status = f"FAULT: evicted {victim}"
            else:
                status = "FAULT: empty frame"

            frames.append(page)
        else:
            status = "HIT"

        print(f"Page {page} | {status:<22} | RAM: {frames}")

    print(f"Total FIFO Page Faults: {page_faults}")
    return page_faults


def simulate_lru(reference_string, num_frames):
    frames = []
    page_faults = 0

    print(f"\n--- LRU (Frames: {num_frames}) ---")

    for page in reference_string:
        if page not in frames:
            page_faults += 1

            if len(frames) >= num_frames:
                victim = frames.pop(0)
                status = f"FAULT: evicted {victim}"
            else:
                status = "FAULT: empty frame"

            frames.append(page)
        else:
            status = "HIT"

            # Move the accessed page to the most recently used position.
            frames.remove(page)
            frames.append(page)

        print(f"Page {page} | {status:<22} | RAM: {frames}")

    print(f"Total LRU Page Faults: {page_faults}")
    return page_faults


def main():
    ai_memory_requests = [2, 3, 2, 1, 5, 2, 4, 5, 3, 2, 5, 2]
    total_physical_frames = 3

    print("Reference string:", ai_memory_requests)
    print("Physical frames:", total_physical_frames)

    fifo_faults = simulate_fifo(
        ai_memory_requests, total_physical_frames
    )
    lru_faults = simulate_lru(
        ai_memory_requests, total_physical_frames
    )

    total_requests = len(ai_memory_requests)

    print("\n--- SUMMARY ---")
    print("Algorithm | Page Faults | Page Hits")
    print(
        f"FIFO      | {fifo_faults:11d} | "
        f"{total_requests - fifo_faults:9d}"
    )
    print(
        f"LRU       | {lru_faults:11d} | "
        f"{total_requests - lru_faults:9d}"
    )


if __name__ == "__main__":
    main()