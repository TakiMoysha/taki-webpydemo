def run_cli() -> None:
    import os
    import sys
    from pathlib import Path

    package_name = Path(__file__).parent.name
    workdir_path = Path(__file__).parent.parent.resolve()

    print(f"Workdir: {workdir_path}")
    print(f"Package: {package_name}")
    print(f"UV_PROJECT: {os.getenv('UV_PROJECT')}")

    sys.path.append(str(workdir_path))
    os.environ.setdefault("LITESTAR_APP", f"{package_name}.asgi:create_app")

    try:
        from litestar.__main__ import run_cli as run_litestar_cli
    except ImportError as exc:
        print("Failed to import litestar: ", str(exc), file=sys.stderr)
        sys.exit(1)

    run_litestar_cli()


if __name__ == "__main__":
    run_cli()
