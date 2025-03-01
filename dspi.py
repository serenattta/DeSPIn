import time
import threading
import sys
from picarx import Picarx
from vilib import Vilib

###############################################################################
# 1) 占位：与本地部署的大语言模型（Deepseek）通信，解析命令
###############################################################################
def parse_command_with_LLM(command_text):
    """
    假设我们可以通过某种接口调用树莓派上部署的 Deepseek LLM。
    这里写成一个占位函数，演示如何拿到一个结构化结果。

    示例：
      输入: "去找红色的球再拿回来"
      输出: {"action": "find", "object": "ball", "color": "red"}

    如果 LLM 仅输出一个字符串 "red"，则可以直接返回字符串。
    """
    # --------------------
    # pseudo code:
    # response = deepseek_llm_inference(command_text)
    # structured_output = parse_json(response)  # or however your LLM outputs it
    # --------------------
    
    # hard code for examples
    # 你要用实际的 LLM 接口替换掉
    structured_output = {
        "action": "find",
        "object": "ball",
        "color": "red"
    }
    
    return structured_output



# 全局变量，标记是否需要终止
stop_signal = False
###############################################################################
# 监听键盘输入的线程
###############################################################################
def listen_keyboard():
    global stop_signal
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


def track_color(px, target_color="red", speed=20):
    """
    根据 target_color 在摄像头中检测目标，并小车前进追踪。
    直到手动中断或目标消失。
    """

    # 启动摄像头与检测
    Vilib.camera_start()
    Vilib.display()
    Vilib.color_detect(target_color)  # 启用颜色检测

    dir_angle = 0
    x_angle   = 0
    y_angle   = 0

    try:
        while not stop_signal:
            # 检测目标数量
            if Vilib.detect_obj_parameter['color_n'] != 0:
                # 取检测到的目标坐标
                coordinate_x = Vilib.detect_obj_parameter['color_x']
                coordinate_y = Vilib.detect_obj_parameter['color_y']

                # 1) 调整云台
                x_angle += (coordinate_x * 10 / 640) - 5
                x_angle = clamp_number(x_angle, -35, 35)
                px.set_cam_pan_angle(x_angle)

                y_angle -= (coordinate_y * 10 / 480) - 5
                y_angle = clamp_number(y_angle, -35, 35)
                px.set_cam_tilt_angle(y_angle)

                # 2) 调整底盘转向以跟随目标
                if dir_angle > x_angle:
                    dir_angle -= 1
                elif dir_angle < x_angle:
                    dir_angle += 1
                px.set_dir_servo_angle(dir_angle)

                # 3) 前进
                px.forward(speed)
                time.sleep(0.05)

            else:
                # 如果未检测到目标，则停止或搜索
                px.forward(0)
                time.sleep(0.05)

    finally:
        px.stop()
        print("Tracking finished.")
        time.sleep(0.1)


###############################################################################
# 3) 主程序：先解析指令，再执行追踪
###############################################################################
def main():
    px = Picarx()
    global stop_signal

    # 启动键盘监听线程（防止阻塞主线程）
    keyboard_thread = threading.Thread(target=listen_keyboard, daemon=True)
    keyboard_thread.start()
    
    # ============ A. 接收/定义自然语言指令 ============
    user_input = "Get the red ball and come back"  # 假设我们在PC上输入传给树莓派
    print("[User Command]：", user_input)

    # ============ B. 调用 LLM，解析指令 ============
    parsed = parse_command_with_LLM(user_input)
    # 期望结果类似：{"action": "find", "object": "ball", "color": "red"}
    target_color = parsed.get("color", None)
    if not target_color:
        print("Cannot find target color in the LLM.")
        return
    
    print("[LLM Result] : Target Color = ", target_color)

    # ============ C. 执行追踪逻辑 ============
    print(f"Chasing mooooooo: {target_color}")
    try:
        # 执行追踪（如果目标丢失，则执行搜索）
        track_color(px, target_color=target_color, speed=20)
    except KeyboardInterrupt:
        print("\nCTRL C detected, Safely exiting...\n")
        stop_signal = True  # 让主循环退出
    finally:
        px.stop()  # **确保小车完全停止**
        print("Fully stopped. Prgram exit.")

###############################################################################
# 启动
###############################################################################
if __name__ == "__main__":
    main()
