import pygame
import time

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.is_playing = False
        self.is_paused = False
        self.start_time = 0
        self.pause_time = 0
        self.volume = 0.5  # Начальный уровень громкости (от 0.0 до 1.0)
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
        self.volume = min(self.volume + 0.1, 1.0)  # Увеличение громкости на 0.1, максимум 1.0
        pygame.mixer.music.set_volume(self.volume)

    def volume_down(self):
        self.volume = max(self.volume - 0.1, 0.0)  # Уменьшение громкости на 0.1, минимум 0.0
        pygame.mixer.music.set_volume(self.volume)