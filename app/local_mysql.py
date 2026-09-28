"""Start the project-local MySQL server when it is installed on this host."""

import socket
import subprocess
import time
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MYSQL_ROOT = PROJECT_ROOT / ".mysql" / "mysql-8.4.0-winx64"
MYSQL_SERVER = MYSQL_ROOT / "bin" / "mysqld.exe"
MYSQL_CONFIG = PROJECT_ROOT / ".mysql" / "my.ini"
MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
_mysql_process = None


def _is_listening():
    try:
        with socket.create_connection((MYSQL_HOST, MYSQL_PORT), timeout=0.5):
            return True
    except OSError:
        return False


def ensure_local_mysql():
    """Start MySQL in the background if this host's local package is present."""
    global _mysql_process
    if _is_listening():
        return
    if not MYSQL_SERVER.exists() or not MYSQL_CONFIG.exists():
        return

    creation_flags = 0
    if hasattr(subprocess, "CREATE_NO_WINDOW"):
        creation_flags |= subprocess.CREATE_NO_WINDOW
    # Keep the Popen handle alive for as long as Flask is running. Detaching
    # mysqld on Windows can make process supervisors clean it up prematurely.
    _mysql_process = subprocess.Popen(
        [str(MYSQL_SERVER), f"--defaults-file={MYSQL_CONFIG}"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creation_flags,
        close_fds=True,
    )

    for _ in range(40):
        if _is_listening():
            return
        time.sleep(0.25)

    error_log = PROJECT_ROOT / ".mysql" / "mysql-error.log"
    raise RuntimeError(f"Không thể khởi động MySQL. Xem log tại: {error_log}")
