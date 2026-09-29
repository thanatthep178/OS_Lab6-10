import os
import stat


def simulate_hpc_cluster():
    weight_file = "production_resnet50.pth"

    # Allow rerunning the experiment with this dummy file.
    if os.path.exists(weight_file):
        os.chmod(weight_file, 0o600)

    # Small dummy data, not an actual AI model.
    original_data = b"0101010101010101010"

    print("Creating simulated production model weights...")
    with open(weight_file, "wb") as f:
        f.write(original_data)

    print("Protecting model weights with permissions 0o444...")
    os.chmod(weight_file, 0o444)

    permissions = stat.filemode(os.stat(weight_file).st_mode)
    print(f"OS Permissions: {permissions}")

    print("\n[Training script] Attempting to overwrite the model...")

    try:
        with open(weight_file, "wb") as f:
            f.write(b"Initializing random weights... Overwriting!")
        print("Write succeeded unexpectedly. Check user privileges.")
    except PermissionError:
        print(">>> [DISASTER AVERTED] OS Kernel denied write access.")

    with open(weight_file, "rb") as f:
        current_data = f.read()

    print(f"Model data unchanged: {current_data == original_data}")


if __name__ == "__main__":
    simulate_hpc_cluster()