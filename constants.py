import sys
import os

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

WINDOW_SIZE = 100

MOVE_INTERVAL = 30
FRAME_INTERVAL = 160
TURN_INTERVAL = 3000

IDLE_FOLDER = os.path.join(BASE_DIR, "assets", "idle")
WALK_FOLDER = os.path.join(BASE_DIR, "assets", "walk")
BOUNCE_FOLDER = os.path.join(BASE_DIR, "assets", "bounce")
SLEEP_FOLDER = os.path.join(BASE_DIR, "assets", "sleep")
WAKE_FOLDER = os.path.join(BASE_DIR, "assets", "wake")
PETTING_FOLDER = os.path.join(BASE_DIR, "assets", "petting")