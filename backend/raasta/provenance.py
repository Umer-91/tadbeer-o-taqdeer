"""Record the actual execution environment and source, without user identifiers."""

import hashlib
import platform
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path


def environment_metadata() -> dict:
    source_dir = Path(__file__).resolve().parent
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(), "os": platform.system(),
        "os_release": platform.release(), "machine": platform.machine(),
        "processor": platform.processor(),
        "packages": {name: version(name) for name in ("qiskit", "qiskit-aer", "numpy", "scipy")},
        "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted(source_dir.glob("*.py"))},
        "synthetic": True, "execution_environment": "CPU; quantum runs use a noiseless simulator, no quantum hardware",
    }
