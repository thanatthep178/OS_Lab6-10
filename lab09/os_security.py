import json
import os
import stat


def main():
    secure_file = "secret_config.json"

    # Allow rerunning this experiment.
    if os.path.exists(secure_file):
        os.chmod(secure_file, 0o600)

    # This is a dummy key for the experiment.
    with open(secure_file, "w") as f:
        json.dump({"api_key": "DEMO_KEY_ONLY"}, f)

    print(f"Created {secure_file}.")

    print("Locking file permissions to Read-Only (0o400)...")
    os.chmod(secure_file, 0o400)

    permissions = stat.filemode(os.stat(secure_file).st_mode)
    print(f"New Permissions: {permissions}")

    print("\nAttempting to overwrite the file...")

    try:
        with open(secure_file, "a") as f:
            f.write("\nMALICIOUS HACKER DATA")
        print("Write succeeded unexpectedly. Check user privileges.")
    except PermissionError as e:
        print(f">>> [OS KERNEL BLOCKED] PermissionError: {e}")
        print(">>> The Operating System successfully protected the file!")


if __name__ == "__main__":
    main()