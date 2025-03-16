import pygame
import time

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.is_playing = False
        self.is_paused = False
        self.start_time = 0
        self.pause_time = 0
        self.volume = 0.5  # Initial volume level (from 0.0 to 1.0)
        self.is_muted = False
        self.previous_volume = self.volume
        pygame.mixer.music.set_volume(self.volume)

    def play(self, filepath):
        if self.is_playing:
            self.stop()
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        self.is_playing = True
        self.is_paused = False
        self.start_time = time.time()

    def pause(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.pause_time = time.time()
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.start_time += time.time() - self.pause_time

    def stop(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False

    def seek(self, seconds):
        if self.is_playing:
            current_pos = time.time() - self.start_time
            new_pos = current_pos + seconds
            if new_pos < 0:
                new_pos = 0
            self.stop()
            pygame.mixer.music.play(start=new_pos)
            self.is_playing = True
            self.is_paused = False
            self.start_time = time.time() - new_pos

    def get_current_time(self):
        if self.is_playing:
            current_pos = time.time() - self.start_time
            minutes = int(current_pos // 60)
            seconds = int(current_pos % 60)
            milliseconds = int((current_pos * 1000) % 1000)
            return f"{minutes}:{seconds}.{milliseconds}"
        return "0:0.0"

    def volume_up(self):
        self.volume = min(self.volume + 0.1, 1.0)  # Increase volume by 0.1, maximum 1.0
        pygame.mixer.music.set_volume(self.volume)

    def volume_down(self):
        self.volume = max(self.volume - 0.1, 0.0)  # Decrease volume by 0.1, minimum 0.0
        pygame.mixer.music.set_volume(self.volume)

    def mute(self):
        if self.is_muted:
            self.volume = self.previous_volume
            self.is_muted = False
        else:
            self.previous_volume = self.volume
            self.volume = 0.0
            self.is_muted = True
        pygame.mixer.music.set_volume(self.volume)