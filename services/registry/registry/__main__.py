def run_cli() -> None:
    import os
    import sys
    from pathlib import Path

    workdir_path = Path(__file__).parent.parent.resolve()
    sys.path.append(str(workdir_path))
    os.environ.setdefault("LITESTAR_APP", "registry.asgi:create_app")

    try:
        from litestar.__main__ import run_cli as run_litestar_cli
    except ImportError as exc:
        print("Failed to import litestar: ", str(exc), file=sys.stderr)  # noqa: T201
        sys.exit(1)

    run_litestar_cli()


if __name__ == "__main__":
    run_cli()
