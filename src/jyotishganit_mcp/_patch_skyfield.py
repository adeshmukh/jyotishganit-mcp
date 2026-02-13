"""Patch Skyfield loader to use local hip_main.dat when JYOTISHGANIT_HIP_MAIN_DAT is set.

Applied before jyotishganit is imported so the PyPI jyotishganit (which does not
read this env var) uses the local file and does not try to download from CDS.
"""

import os

from skyfield.api import load
from skyfield.data import hipparcos

_HIPPARCOS_URL = hipparcos.URL
_original_open = load.open


def _patched_open(url, mode="rb", reload=False, filename=None, backup=False):
    """Use local hip_main.dat when JYOTISHGANIT_HIP_MAIN_DAT is set and valid."""
    if url == _HIPPARCOS_URL:
        path = os.environ.get("JYOTISHGANIT_HIP_MAIN_DAT", "").strip()
        if path and os.path.isfile(path):
            url = path
    return _original_open(url, mode=mode, reload=reload, filename=filename, backup=backup)


load.open = _patched_open
