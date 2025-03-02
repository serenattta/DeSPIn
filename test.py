# from picarx import Picarx
# import time
# def turn_90():
#     search_speed = 20
#     px = Picarx()
#     px.set_dir_servo_angle(0)
#     time.sleep(0.25)
#     px.set_dir_servo_angle(33.5)  # 先右转 30°
#     time.sleep(0.25)
#     px.backward(search_speed)
#     time.sleep(1.2)  # 等待时间，确保旋转完成
#     px.set_dir_servo_angle(-33.5)
#     time.sleep(0.25)
#     px.forward(search_speed)
#     time.sleep(1.2)
#     px.forward(0)
#     px.set_dir_servo_angle(0)
#     px.stop()
# if __name__ == "__main__":
#     turn_90()
#     time.sleep(0.25)
#     turn_90()


import time
import threading
import sys
from picarx import Picarx
from vilib import Vilib
from time import sleep
from robot_hat import Music,TTS
import readchar


if __name__ == "__main__":
    # music = Music()
    # music.music_set_volume(20)
    # music.music_play("triumph.mp3")
    # time.sleep(5)
    tts = TTS()
    tts.lang("en-US")
    # 去掉换行和多余空格
    compressed_text = " ".join(text.split())

    print(compressed_text)
    tts.say(words)
