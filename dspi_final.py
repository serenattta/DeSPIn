import time
import threading
import sys
import os
from picarx import Picarx
from vilib import Vilib
from time import sleep
from robot_hat import Music,TTS
import readchar
from ollama import Client
import json
import re

###############################################################################
# 1) Placeholder: Communicate with locally deployed LLM (Deepseek) to parse commands
SYSTEM_PROMPT = """
    You are a autonomous vehicle navigator. Your job is to convert the user's requests into
    precise instructions the vehicle to operate on in order to complete the user's request.
    You are experienced in converting natural commands to a structured JSON format. 
    You are only allowed to go to certain colors: Red, Blue, Green, Yellow, Purple, Orange and you will 
    change the users request into the following array format: 
    [
        {{"step": 1, "target": "red"}},
        {{"step": 2, "target": "green"}},
            ... more steps if needed
    ]

    The vehicle you are operating ONLY requires the color, so you can 
    disregard any additional information that isn't related to the color.
    DO NOT output any other text than the JSON array.
    Here is your first request: 
        {request}
    Begin!
"""
###############################################################################
def parse_command_with_LLM(command_text):

    client = Client(
        host='http://localhost:8888',
    )
    stream = client.chat(model='deepseek-r1:1.5b', messages=[
        {
            'role': 'system',
            'content': SYSTEM_PROMPT.format(request=command_text),
        },
    ], stream=True)

    response = ""
    for chunk in stream:
        word = chunk['message']['content']
        response += word
        print(word, end='', flush=True)
    #     compressed_text = " ".join(word.split())
    #     tts.say(compressed_text)
    print("\n\n\n")
    # 解析 LLM 的输出
    # 使用正则表达式匹配最大的 JSON 数组
    json_pattern = r'\[.*?\]'
    # greedy match largest json array in response
    json_arrays = re.findall(json_pattern, response.replace("\n", ""))
    if len(json_arrays):
        structured_output = json.loads(json_arrays[0])
    else:
        structured_output = []

    # structured_output = [
    #     {"step": 1, "target": "green"},
    #     {"step": 2, "target": "yellow"},
    #     {"step": 3, "target": "purple"}
    # ]
    
    return structured_output


def u_turn(px, search_speed=10):
    """
    让小车在旋转过程中不断使用摄像头检测目标
    """
    xxx = Vilib.detect_obj_parameter['color_n']
    print(f"🔄 目标丢失，执行 U-Turn 掉头，过程中检查摄像头{xxx}...")
    
    rotation_angle = 6  # 初始旋转角度
    max_rotation_angle = 35  # 最大旋转角度

    for _ in range(20):  # turn 20 times
        px.forward(0)  # 确保小车停止
        px.set_dir_servo_angle(rotation_angle)  # 方向盘右转
        px.forward(search_speed)  # 小车前进，模拟右转
        time.sleep(0.1)  # 每次转一点


        for times in range(10):
            if Vilib.detect_obj_parameter['color_n'] != 0:
                px.forward(0)
                time.sleep(0.05)
                print("🎯 旋转过程中找到目标，立即停止 U-Turn")
                return  # **找到目标就停止旋转**

        # 动态调整旋转角度
        rotation_angle = min(rotation_angle + 5, max_rotation_angle)

    print("❌ 旋转完成，未找到目标，停止")
    px.forward(0)  # **停止**




# 全局变量，标记是否需要终止
stop_signal = False
###############################################################################
# 监听键盘输入的线程
###############################################################################
def listen_keyboard():
    global stop_signal  # Add global declaration
    while True:
        key = input("Enter T/t to stop the car any time.").strip().lower()
        if key == "t":
            stop_signal = True
            print("\nT/t detected, safely exit...\n")
            break  # 退出键盘监听线程


###############################################################################
# 2) 小车追踪颜色的主要逻辑
###############################################################################
# prevent the camera servo out of order and broken.
def clamp_number(num, a, b):
    return max(min(num, max(a, b)), min(a, b))



def play_music(MUSIC_FILE = "mario-coin.mp3"):
    """ 播放找到目标的提示音乐 """
    if os.path.exists(MUSIC_FILE):
        music = Music()
        music.music_set_volume(10)
        music.music_play(MUSIC_FILE)
        time.sleep(5)
    else:
        print(f"File not found")


def track_color_with_search(px, target_color="green", speed=50, search_speed=30,found_area = 40000): # 57600 is 75% of the camara area
    """
    追踪目标颜色，如果目标丢失，则旋转
    """
    global stop_signal  # Add global declaration
    
    # 启动摄像头与颜色检测
    Vilib.camera_start()
    Vilib.display()
    Vilib.color_detect(target_color)  

    dir_angle = 0
    x_angle   = 0
    y_angle   = 0
    SafeDistance = 40   # > 40 安全距离
    DangerDistance = 20
    lost_count = 0  # 记录连续丢失目标的次数


    # 云台回正
    px.set_cam_pan_angle(0)
    px.set_cam_tilt_angle(0)
    try:
        while not stop_signal:  # **添加 stop_signal 控制**
            # 0) 避开障碍
            distance = round(px.ultrasonic.read(), 2)
            if 0 < distance < DangerDistance:
                print("distance: ",distance, "🚫 避开障碍")
                px.set_dir_servo_angle(-30)
                px.backward(speed/2)
                time.sleep(0.5)
                continue

            elif 0 < distance < SafeDistance:
                print("distance: ",distance, "🚫 靠近障碍")
                px.set_dir_servo_angle(30)
                px.forward(speed/2)
                time.sleep(0.5)
                continue

            # 1) 检测目标是否存在
            if Vilib.detect_obj_parameter['color_n'] != 0:
                lost_count = 0  # **重置丢失计数**

                # 取目标的坐标
                coord_x = Vilib.detect_obj_parameter['color_x']
                coord_y = Vilib.detect_obj_parameter['color_y']

                # 2) 调整摄像头云台，使其对准目标
                x_angle += (coord_x * 10 / 640) - 5
                x_angle = clamp_number(x_angle, -35, 35)
                px.set_cam_pan_angle(x_angle)

                y_angle -= (coord_y * 10 / 480) - 5
                y_angle = clamp_number(y_angle, -35, 35)
                px.set_cam_tilt_angle(y_angle)

                # 3) 调整小车方向
                if dir_angle > x_angle:
                    dir_angle -= 1
                elif dir_angle < x_angle:
                    dir_angle += 1
                px.set_dir_servo_angle(dir_angle)

                # 4) 向目标方向前进
                px.forward(speed)
                time.sleep(0.05)

                # 5） 判断目标是否足够大（判定为找到）
                color_w = Vilib.detect_obj_parameter['color_w']
                color_h = Vilib.detect_obj_parameter['color_h']
                color_area = color_w * color_h  # 计算目标面积

                print(f"📏 当前目标面积: {color_area},   {distance}")

                # **检测目标是否达到足够接近的阈值**
                if (color_area >= found_area) and (distance < 100):
                        px.forward(0)
                        print(f"🎯 目标已接近 (面积 >= {found_area},Distance = {distance})，播放音乐！")
                        play_music()
                        # 停止小车
                        time.sleep(1)  # 停留 1 秒
                        return

            else:
                # **8) 目标丢失**
                if lost_count == 0:
                    lost_time = time.time()  # **记录最初丢失目标的时间**
                
                lost_count += 1
                print(f"[搜索模式] 丢失目标次数: {lost_count}, 当前目标: {target_color}")

                # **短暂丢失（小于 5 秒），等待目标重现**
                if time.time() - lost_time < 2:
                    px.forward(0)
                    time.sleep(0.1)
                else:
                    # 目标丢失执行转弯
                    print("🔄 目标丢失 2 秒，执行 U-Turn")
                    u_turn(px)
                    lost_count = 0
                    lost_time = time.time()
    finally:
        px.stop()
        print("Vehicle Fully stopped")


###############################################################################
# 3) 主程序：先解析指令，再执行追踪
###############################################################################
def main():
    px = Picarx()
    global stop_signal

    # ============ A. 接收/定义自然语言指令 ============
    user_input = input("Enter your command: ")
    print("[User Command]: ", user_input)

    # 启动键盘监听线程（防止阻塞主线程）
    keyboard_thread = threading.Thread(target=listen_keyboard, daemon=True)
    keyboard_thread.start()

    # ============ B. 调用 LLM，解析指令 ============
    parsed = parse_command_with_LLM(user_input)
    color_list=["red","orange","yellow","green","blue","purple"]
    for i in range(len(parsed)):
        target_color = parsed[i].get("target", None).lower()

        if target_color not in color_list:
            print(f"❌ 无法识别的目标颜色: {target_color}")
            continue  # 跳过这个目标

        print(f"\n🚗 开始寻找第 {parsed[i]['step']} 步目标颜色: {target_color}")
    
        # 追踪颜色目标
        try:
        # 执行追踪（如果目标丢失，则执行搜索）
            track_color_with_search(px, target_color=target_color, speed=20, search_speed = 10)
        except KeyboardInterrupt:
            print("\nCTRL C detected, Safely exiting...\n")
            stop_signal = True  # 让主循环退出

    print("✅ 所有目标颜色查找任务已完成！")
    
    play_music(MUSIC_FILE = "triumph.mp3")
    print("[LLM Result] : Target Color = ", target_color)

    # ============ C. 执行追踪逻辑 ============
    print(f"Chasing mooooooo: {target_color}")


###############################################################################
# 启动
###############################################################################
if __name__ == "__main__":
    main()
