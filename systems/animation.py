import os
from PySide6.QtGui import QPixmap


class AnimationSystem:
    def __init__(self, update_callback):
        self.frames = []
        self.frame_index = 0
        self.update_callback = update_callback  # calls QWidget.update()

    def load_frames(self, folder):
        self.frames = []
        self.frame_index = 0

        for file in sorted(os.listdir(folder)):
            if file.endswith(".png"):
                path = os.path.join(folder, file)
                self.frames.append(QPixmap(path))

    def next_frame(self, state):
        if not self.frames:
            return

        self.frame_index += 1

        if self.frame_index >= len(self.frames):

            if state == "bounce":
                self.frame_index = 0
                return "bounce_done"

            elif state == "wake":
                self.frame_index = 0
                return "wake_done"
            
            elif state == "petting":
               self.frame_index = 0
               return "petting_cycle_done"

            elif state == "sleep":
                self.frame_index = len(self.frames) - 1
                return "sleep_hold"

            self.frame_index = 0

        self.update_callback()
        return None