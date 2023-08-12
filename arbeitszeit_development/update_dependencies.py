import subprocess

from . import update_python_packages


def main() -> None:
    update_flake()
    update_bulma()
    update_python_packages.main()
    update_constraints()
    generate_type_stubs()


def update_flake() -> None:
    subprocess.run(["nix", "flake", "update"], check=True)


def update_bulma() -> None:
    subprocess.run(
        ["python", "-m", "arbeitszeit_development.update_bulma"],
        check=True,
    )


def update_constraints() -> None:
    subprocess.run(
        [
            "nix",
            "develop",
            "-c",
            "python",
            "-m",
            "arbeitszeit_development.update_constraints",
        ],
        check=True,
    )


def generate_type_stubs() -> None:
    subprocess.run(
        [
            "nix",
            "develop",
            "-c",
            "python",
            "-m",
            "arbeitszeit_development.generate_type_stubs",
        ]
    )


if __name__ == "__main__":
    main()
