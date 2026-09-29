def show_result(path):
    total_movement = 0

    for start, end in zip(path, path[1:]):
        movement = abs(end - start)
        total_movement += movement
        print(f"Track {start:3} -> {end:3} | Movement: {movement}")

    print("Path:", " -> ".join(map(str, path)))
    print(f"Total Head Movement: {total_movement} cylinders")

    return total_movement


def simulate_fcfs(requests, initial_position):
    print("\n--- FCFS Disk Scheduling ---")

    # Service requests in their arrival order.
    path = [initial_position] + list(requests)
    return show_result(path)


def simulate_scan(requests, initial_position, max_cylinder=199):
    print("\n--- SCAN Disk Scheduling (UP first) ---")

    left = sorted(
        req for req in requests if req < initial_position
    )
    right = sorted(
        req for req in requests if req >= initial_position
    )

    # Move toward higher track numbers first.
    path = [initial_position] + right

    # Reach the disk boundary before reversing direction.
    if path[-1] != max_cylinder:
        path.append(max_cylinder)

    # Move downward and stop after the final pending request.
    path.extend(reversed(left))

    return show_result(path)


def main():
    io_requests = [98, 183, 37, 122, 14, 124, 65, 67]
    start_position = 53

    print("Disk tracks: 0-199")
    print(f"Initial Head Position: {start_position}")
    print(f"I/O Requests: {io_requests}")

    fcfs_movement = simulate_fcfs(io_requests, start_position)
    scan_movement = simulate_scan(io_requests, start_position)

    reduction = (
        (fcfs_movement - scan_movement) / fcfs_movement * 100
    )

    print("\n--- SUMMARY ---")
    print(f"FCFS Total Head Movement: {fcfs_movement} cylinders")
    print(f"SCAN Total Head Movement: {scan_movement} cylinders")
    print(f"Movement reduction: {reduction:.2f}%")


if __name__ == "__main__":
    main()