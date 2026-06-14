import os
import sys
import random

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QGuiApplication
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl

from constants import (
    IDLE_FOLDER, 
    WALK_FOLDER, 
    BOUNCE_FOLDER, 
    SLEEP_FOLDER, 
    WAKE_FOLDER,
    PETTING_FOLDER
)

from systems.animation import AnimationSystem
from systems.movement import MovementSystem
from systems.brain import BrainSystem
from systems.render import render_pet

# =========================================================
#  MAIN PET CLASS
# =========================================================
class PetWindow(QWidget):
    def __init__(self):
        super().__init__()

        # =========================
        # WINDOW SETUP
        # =========================

        # size of window (adjust later if needed)
        self.resize(100, 100)

        # make window frameless + transparent + always on top
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setCursor(Qt.PointingHandCursor)
        self.setWindowFlag(Qt.Tool)
        self.drag_offset = None
        
        # =========================
        #  STATE VARIABLES
        # =========================

        # animation variables
        self.animation = AnimationSystem(self.update)
        self.animation.load_frames(IDLE_FOLDER)
        self.movement = MovementSystem(self)
        self.brain = BrainSystem(self)

        self.state = "idle"
        self.facing = "left"
        self.frozen = False
        self.hover = False
        self.dragging_pet = False
        self.pre_petting_state = "idle"

        #sound effect variables
        self.audio_output = QAudioOutput()
        self.baa_player = QMediaPlayer()
        self.baa_player.setAudioOutput(self.audio_output)
        self.baa_player.setSource(QUrl.fromLocalFile(os.path.join(BASE_DIR, "assets", "baa.mp3")))
        self.audio_output.setVolume(0.5)

        # =========================
        #  TIMERS
        # =========================

        self.brain_timer = QTimer()
        self.brain_timer.timeout.connect(self.update_brain)
        self.brain_timer.start(100)

        # timer (controls animation speed)
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)
        self.timer.start(160)  # 100ms = slow smooth animation

        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.move_pet)
        self.move_timer.start(30)


    # =========================================================
    #  ANIMATION SYSTEM
    # =========================================================

    def next_frame(self):
     result = self.animation.next_frame(self.state)

     if result == "bounce_done":
        self.set_state("walk")
        self.movement.choose_random_direction()

     elif result == "wake_done":
        self.set_state("idle")

     elif result == "sleep_hold":
        return
     
     elif result == "petting_cycle_done":
       if self.dragging_pet:
        return  # loop again, frame_index already reset to 0
       else:
        self.set_state(self.pre_petting_state)

    # =========================================================
    #  STATE SYSTEM (BRAIN)
    # =========================================================
    
    def update_brain(self):
      self.brain.update()

    
    def set_state(self, new_state):
     self.state = new_state

     if new_state != "sleep":
        self.brain.on_leave_sleep()

     self.brain.reset_thresholds()

     if self.state == "idle":
        self.animation.load_frames(IDLE_FOLDER)

     elif self.state == "bounce":
        self.animation.load_frames(BOUNCE_FOLDER)
        self.baa_player.setPosition(0)
        self.baa_player.play()

     elif self.state == "walk":
        self.animation.load_frames(WALK_FOLDER)

     elif self.state == "sleep":
        self.animation.load_frames(SLEEP_FOLDER)
        self.brain.on_enter_sleep()

     elif self.state == "petting":
        self.animation.load_frames(PETTING_FOLDER)

     elif self.state == "wake":
        self.animation.load_frames(WAKE_FOLDER)

     self.animation.frame_index = 0
    
    
    def toggle_freeze(self):
     self.frozen = not self.frozen

     if not self.frozen:
        self.brain.on_unfreeze()
    
    # =========================================================
    # 🏃 MOVEMENT SYSTEM
    # =========================================================

    def move_pet(self):
     self.movement.move()

    def get_screen_size(self):
      screen = QGuiApplication.primaryScreen()
      geo = screen.geometry()
      return geo.width(), geo.height()
    
    def update_facing(self):
     self.facing = "left" if self.movement.dx < 0 else "right"

    # =========================================================
    # INPUT SYSTEM
    # =========================================================
    
    def mousePressEvent(self, event):
     self.mark_activity()

     if self.frozen:
        self.drag_offset = event.globalPosition().toPoint() - self.pos()
    
    def mouseMoveEvent(self, event):
     if self.frozen:
        if event.buttons() & Qt.LeftButton and self.drag_offset is not None:
            self.move(event.globalPosition().toPoint() - self.drag_offset)
        return
     
     if event.buttons() & Qt.LeftButton:
        if not self.dragging_pet:
            self.dragging_pet = True
            if self.state in ("idle", "walk"):
                self.pre_petting_state = self.state
                self.set_state("petting")
    

    def mouseReleaseEvent(self, event):
     if self.frozen:
        self.drag_offset = None
        return
     
     if self.dragging_pet:
        self.dragging_pet = False
        # petting will finish its loop naturally via petting_cycle_done
        return

     # it was a real click (no drag) — existing bounce/walk logic
     if self.state == "sleep":
        self.set_state("wake")
        return

     if self.state != "idle":
        return

     self.set_state("bounce")

    def mouseDoubleClickEvent(self, event):
       self.toggle_freeze()

    
    # =========================================================
    #  ACTIVITY SYSTEM
    # =========================================================

    def mark_activity(self):
       self.brain.mark_activity()
      
    # =========================================================
    #  RENDER SYSTEM
    # =========================================================

    def paintEvent(self, event):
     painter = QPainter(self)
     render_pet(self, painter)
