"""Validate example backend lists without importing their framework applications."""

import ast
from pathlib import Path

from social_core.backends.base import BaseAuth
from social_core.utils import module_member


def check_backends(path: Path) -> list[str]:
    """Return configuration errors for an example's backend tuple."""
    errors = []
    settings = {"AUTHENTICATION_BACKENDS", "SOCIAL_AUTH_AUTHENTICATION_BACKENDS"}
    configurations = [
        node
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id in settings
            for target in node.targets
        )
    ]
    if len(configurations) != 1:
        return [f"{path}: expected exactly one backend configuration"]

    paths: set[str] = set()
    names: set[str] = set()
    for backend_path in ast.literal_eval(configurations[0].value):
        if backend_path in paths:
            errors.append(f"{path}: duplicate backend path {backend_path}")
        paths.add(backend_path)
        # Framework authentication backends are outside social-auth-core.
        if not backend_path.startswith("social_core.backends."):
            continue
        try:
            backend = module_member(backend_path)
        except (ImportError, AttributeError) as error:
            errors.append(f"{path}: cannot load {backend_path}: {error}")
            continue
        if not isinstance(backend, type) or not issubclass(backend, BaseAuth):
            errors.append(f"{path}: {backend_path} is not a social backend")
            continue
        if backend.name in names:
            errors.append(f"{path}: duplicate backend name {backend.name}")
        names.add(backend.name)
    return errors


def main() -> int:
    """Check every example and report all failures together."""
    root = Path(__file__).resolve().parent.parent
    configurations = sorted(root.glob("example-*/**/settings.py"))
    if not configurations:
        print("No example settings found")
        return 1
    errors = [error for path in configurations for error in check_backends(path)]
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Validated backend configurations in {len(configurations)} examples")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
