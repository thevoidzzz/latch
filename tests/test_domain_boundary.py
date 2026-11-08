"""The domain package stays free of drivers. The architecture test is the lock."""

import ast
from pathlib import Path

_PACKAGE = Path(__file__).resolve().parents[1] / "src" / "latch"
_ROOTS = (_PACKAGE / "domain", _PACKAGE / "application")
_FORBIDDEN_PREFIXES = (
    "latch.infrastructure",
    "latch.api",
    "fastapi",
    "httpx",
    "langgraph",
    "langfuse",
    "openai",
)


def test_domain_does_not_import_drivers() -> None:
    missing = [root.name for root in _ROOTS if not root.is_dir()]
    assert missing == []
    violations: list[str] = []
    for root in _ROOTS:
        for path in sorted(root.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                modules: list[str] = []
                if isinstance(node, ast.Import):
                    modules = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module is not None:
                    modules = [node.module]
                for module in modules:
                    if module.startswith(_FORBIDDEN_PREFIXES):
                        violations.append(f"{path.name} imports {module}")
    assert violations == []
