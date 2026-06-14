import random
from PySide6.QtCore import QTimer


class BrainSystem:
    def __init__(self, pet):
        self.pet = pet  # reference back to PetWindow

        self.idle_threshold = random.randint(50, 150)
        self.walk_threshold = random.randint(80, 200)
        self.sleep_timeout = random.randint(600, 1200)

        self.behaviour_counter = 0
        self.time_since_input = 0
        self.sleep_timer_active = False
        self.sleep_token = 0

    def update(self):
        pet = self.pet

        if pet.frozen or pet.state in ("sleep", "petting", "bounce", "wake"):
          return

        self.time_since_input += 1
        self.behaviour_counter += 1
        screen_width, screen_height = pet.get_screen_size()

        if self.time_since_input >= self.sleep_timeout and pet.state == "idle":
            pet.set_state("sleep")

        if pet.state == "idle":
            if self.behaviour_counter > self.idle_threshold:
                choice = random.choices(["walk", "sleep"], weights=[0.95, 0.05])[0]

                if choice == "walk":
                    pet.set_state("walk")
                    pet.movement.choose_safe_direction(screen_width, screen_height)
                else:
                    pet.set_state("sleep")

                self.behaviour_counter = 0

        elif pet.state == "walk":
            if self.behaviour_counter > self.walk_threshold:
                pet.set_state("idle")
                self.behaviour_counter = 0

    def reset_thresholds(self):
        self.behaviour_counter = 0
        self.idle_threshold = random.randint(120, 250)
        self.walk_threshold = random.randint(80, 200)
        self.sleep_timeout = random.randint(600, 1200)

    def on_enter_sleep(self):
        if not self.sleep_timer_active:
            self.sleep_timer_active = True
            self.sleep_token += 1
            token = self.sleep_token
            sleep_time = random.randint(100, 400)
            QTimer.singleShot(sleep_time * 1000, lambda t=token: self.auto_wake(t))

    def on_leave_sleep(self):
        self.sleep_timer_active = False

    def auto_wake(self, token):
        if token != self.sleep_token:
            return

        self.sleep_timer_active = False

        if self.pet.state == "sleep" and not self.pet.frozen:
            self.pet.set_state("wake")
            self.mark_activity()

    def mark_activity(self):
        self.time_since_input = 0

    def on_unfreeze(self):
        self.behaviour_counter = 0
        self.time_since_input = 0
        self.idle_threshold = random.randint(50, 150)
        self.walk_threshold = random.randint(80, 200)