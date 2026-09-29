import tempfile
import time
from pathlib import Path


def setup_test_files(base_dir, num_files, file_size):
    small_dir = base_dir / "raw_images_folder"
    small_dir.mkdir()

    block = b"\x00" * file_size

    for i in range(num_files):
        with open(small_dir / f"img_{i}.bin", "wb") as f:
            f.write(block)

    # Plain binary data used to illustrate a packed dataset.
    # This is not an actual TFRecord file.
    packed_file = base_dir / "packed_dataset.bin"

    with open(packed_file, "wb") as f:
        for _ in range(num_files):
            f.write(block)

    return small_dir, packed_file


def test_small_files(small_dir, num_files):
    total_bytes = 0
    start = time.perf_counter()

    for i in range(num_files):
        with open(small_dir / f"img_{i}.bin", "rb") as f:
            total_bytes += len(f.read())

    elapsed = time.perf_counter() - start
    return elapsed, total_bytes


def test_packed_file(packed_file, num_files, file_size):
    total_bytes = 0
    start = time.perf_counter()

    with open(packed_file, "rb") as f:
        for _ in range(num_files):
            total_bytes += len(f.read(file_size))

    elapsed = time.perf_counter() - start
    return elapsed, total_bytes


def main():
    num_files = 1000
    file_size = 4096
    expected_bytes = num_files * file_size

    print("--- AI Dataset I/O Benchmark ---")
    print(f"Small files: {num_files}")
    print(f"Bytes per small file: {file_size}")
    print(f"Total bytes per test: {expected_bytes}")
    print("Setting up test files...")

    # Temporary files are automatically removed after the test.
    with tempfile.TemporaryDirectory(prefix="lab08_io_") as temp_dir:
        small_dir, packed_file = setup_test_files(
            Path(temp_dir), num_files, file_size
        )

        print("\nTest 1: Reading 1,000 separate files")
        small_time, small_bytes = test_small_files(
            small_dir, num_files
        )
        print(f"Time: {small_time:.6f} seconds")
        print(f"Bytes read: {small_bytes}")

        print("\nTest 2: Reading one packed file sequentially")
        packed_time, packed_bytes = test_packed_file(
            packed_file, num_files, file_size
        )
        print(f"Time: {packed_time:.6f} seconds")
        print(f"Bytes read: {packed_bytes}")

        if small_bytes != expected_bytes or packed_bytes != expected_bytes:
            raise RuntimeError("The number of bytes read is incorrect.")

        print("\n--- SUMMARY ---")
        print(f"Small files time: {small_time:.6f} seconds")
        print(f"Packed file time: {packed_time:.6f} seconds")
        print(f"Small / Packed time ratio: {small_time / packed_time:.2f}x")
        print("Both tests read the same number of bytes.")

    print("Temporary test files cleaned up.")


if __name__ == "__main__":
    main()