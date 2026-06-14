import sys
import os
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon
from pet import PetWindow

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

window = PetWindow()
window.show()

# system tray icon
icon_path = os.path.join(BASE_DIR, "assets", "idle", "frame_000.png")
tray = QSystemTrayIcon()
tray.setIcon(QIcon(icon_path))
tray.setVisible(True)

menu = QMenu()
quit_action = menu.addAction("Quit Desktop Sheep")
quit_action.triggered.connect(app.quit)
tray.setContextMenu(menu)

sys.exit(app.exec())