""" update __version__ in version.py.

This is only for the pre-commit local
hook track-version (refer to ../.pre-commit-config.yml)
"""

from pathlib import Path
import re

CDIR = Path(__file__).absolute().parent
PDIR = CDIR.parent
PYPROJECT_FILE = Path(PDIR) / "pyproject.toml"


def get_version(filename=None, startswith="version"):
    """ get version via ../pyproject.toml.

    >>> get_version()[:3] in ["2.0"]
    True
    """
    if filename is None:
        filename = PYPROJECT_FILE
    line = [
        line
        for line in Path(filename).read_text(encoding="utf8").splitlines()
        if line.strip().startswith(startswith)
    ]

    version = ""
    if line:
        _ = re.findall(r'"([^\"]+)', line[0])
        if _:
            version = _[0]

    return version


filename = Path(CDIR / "version.py")

# fetch __verion__ from version.py
try:
    __version__ = get_version(filename, "__version__")
except Exception as exc:
    print("get_version(filename, '__version__') failed, exc: %s" % exc)
    __version__ = ""

# gen version from ../pyproject.toml
try:
    version = get_version()
except Exception as exc:
    print("get_version() failed, exc: %s" % exc)
    version = str(exc)

# update only when not the same
if version not in [__version__]:
    filepath = CDIR / "version.py"
    print(f" Updating {filepath}")
    cont = f'''
r"""
version info from pyproject.toml
updated via pre-commit local hook track-version in .pre-commit-config.yaml

this file is auto-updated as soon as the
__versoin__ is different from that in ../pyproject.toml
"""

__version__ = "{version}"
'''

    try:
        filepath.write_text(cont.lstrip(), encoding="utf-8")
    except Exception as exc:
        print(" Writing failed, exc: %s" % exc)
