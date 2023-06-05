import sys
import os
from PyQt6 import QtCore

def fix_pyqt_paths():
    if getattr(sys, "frozen", False):
        # If the application is bundled by PyInstaller
        basedir = os.path.dirname(sys.executable)
        QtCore.QCoreApplication.addLibraryPath(os.path.join(basedir, "platforms"))
        QtCore.QCoreApplication.addLibraryPath(os.path.join(basedir, "styles"))
