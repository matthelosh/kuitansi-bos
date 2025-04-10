import os
import platform
import sys

def setup_ghostscript():
    """Tambahkan path ghostscript portable ke environment jika di Windows."""
    if platform.system() == "Windows":
        base_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
        gs_bin_path = os.path.join(base_dir, "lib", "ghostscript", "bin")
        gs_exe_path = os.path.join(gs_bin_path, "gswin64.exe")

        if os.path.isfile(gs_exe_path):
            os.environ["PATH"] = gs_bin_path + os.pathsep + os.environ["PATH"]
            os.environ["GHOSTSCRIPT_PATH"] = gs_exe_path
            print(f"[INFO] Ghostscript PATH ditambahkan: {gs_bin_path}")
        else:
            print(f"[WARNING] Folder Ghostscript tidak ditemukan di: {gs_bin_path}")
