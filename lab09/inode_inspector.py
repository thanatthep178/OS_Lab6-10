import os
import stat
import time


def inspect_file(filename):
    print(f"--- OS Inode Inspection for: {filename} ---")

    file_stats = os.stat(filename)

    print(f"Inode Number:     {file_stats.st_ino}")
    print(f"File Size:        {file_stats.st_size} bytes")
    print(f"Metadata Changed: {time.ctime(file_stats.st_ctime)}")
    print(f"Last Modified:    {time.ctime(file_stats.st_mtime)}")
    print(f"OS Permissions:   {stat.filemode(file_stats.st_mode)}")


def main():
    test_file = "dataset_sample.csv"

    with open(test_file, "w") as f:
        f.write("id,feature_1,feature_2,label\n")
        f.write("1,0.5,0.8,cat\n")

    inspect_file(test_file)


if __name__ == "__main__":
    main()