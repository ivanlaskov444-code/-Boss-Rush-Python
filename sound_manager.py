from PyQt6 import QtMultimedia, QtCore
from constants import SOUNDS_DIR, BULLET_SOUND
import os


class SoundManager:
    def __init__(self):
        self.sound_path = os.path.join(SOUNDS_DIR, BULLET_SOUND)

    def play_bullet_sound(self):
        """Тихая версия без каких-либо сообщений"""
        try:
            audio_output = QtMultimedia.QAudioOutput()
            audio_output.setVolume(1.0)

            player = QtMultimedia.QMediaPlayer()
            player.setAudioOutput(audio_output)
            player.setSource(QtCore.QUrl.fromLocalFile(self.sound_path))
            player.play()

            # Тихая очистка
            QtCore.QTimer.singleShot(2000, lambda: self.silent_cleanup(player, audio_output))

        except Exception:
            # Полное молчание об ошибках
            pass

    def silent_cleanup(self, player, audio_output):
        """Тихая очистка"""
        try:
            player.stop()
            player.deleteLater()
            audio_output.deleteLater()
        except:
            pass