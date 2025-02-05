import subprocess

def get_installed_packages():
    """Returns a set of installed packages and versions from `pip freeze`."""
    result = subprocess.run(["pip", "freeze"], capture_output=True, text=True, check=True)
    return set(result.stdout.strip().split("\n"))

def get_required_packages(requirements_file="requirements.txt"):
    """Returns a set of packages and versions from the requirements file."""
    try:
        with open(requirements_file, "r") as file:
            return set(line.strip() for line in file if line.strip() and not line.startswith("#"))
    except FileNotFoundError:
        print(f"Error: {requirements_file} not found.")
        return set()

def check_requirements():
    installed = get_installed_packages()
    required = get_required_packages()

    missing = required - installed
    extra = installed - required

    if not missing and not extra:
        print("✅ Everything is up to date!")
        exit(0)
    else:
        if missing:
            print("❌ Missing packages:")
            print("\n".join(missing))
            exit(1)
        if extra:
            print("⚠️ Extra packages installed:")
            print("\n".join(extra))
            exit(0)

if __name__ == "__main__":
    check_requirements()
