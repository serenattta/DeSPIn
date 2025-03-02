from picarx import Picarx
import time

POWER = 50
SafeDistance = 40   # > 40 安全距离
DangerDistance = 20 # > 20 && < 40 转弯,
                    # < 20 倒退

def main():
    try:
        px = Picarx()
        # px = Picarx(ultrasonic_pins=['D2','D3']) # trigger, echo

        while True:
            distance = round(px.ultrasonic.read(), 2)
            print("distance: ",distance)
            if distance >= SafeDistance:
                px.set_dir_servo_angle(0)
                px.forward(POWER)
            elif distance >= DangerDistance:
                px.set_dir_servo_angle(30)
                px.forward(POWER)
                time.sleep(0.1)
            else:
                px.set_dir_servo_angle(-30)
                px.backward(POWER)
                time.sleep(0.5)

    finally:
        px.forward(0)


if __name__ == "__main__":
    main()



    
    # 启动摄像头与颜色检测
    Vilib.camera_start()
    Vilib.display()
    Vilib.color_detect(target_color)  

    dir_angle = 0
    x_angle   = 0
    y_angle   = 0
    lost_count = 0  # 记录连续丢失目标的次数
    search_turn = 30  # 搜索旋转角度（左右摆动）
    SafeDistance = 40   # > 40 安全距离
    DangerDistance = 20

    try:
        while not stop_signal:  # **添加 stop_signal 控制**
            # 0) 检测距离
            distance = round(px.ultrasonic.read(), 2)
            
            # 0.5) 避障
            if distance < DangerDistance:
                px.set_dir_servo_angle(-30)
                px.backward(speed)
                time.sleep(0.5)
                continue

            elif distance < SafeDistance:
                px.set_dir_servo_angle(30)
                px.forward(speed)
                time.sleep(0.1)

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

                print(f"当前目标面积: {color_area}")

                # **检测目标是否达到足够接近的阈值**
                if color_area >= found_area:
                    print(f"目标已接近 (面积 >= {found_area})，播放音乐！")
                    play_music()
                    px.forward(0)  # 停止小车
                    time.sleep(2)  # 停留 2 秒
                    continue  # 继续检测

            else:
                # 目标丢失，进入“原地旋转搜索”模式
                lost_count += 1
                print(f"[搜索模式] 丢失目标次数: {lost_count}")

                if lost_count < 10:  # 允许短时间丢失，不立即搜索
                    px.forward(0)
                    time.sleep(0.1)
                else:
                    # 进入原地旋转模式（左右交替旋转）
                    px.forward(0)
                    px.set_dir_servo_angle(search_turn)
                    px.forward(search_speed)
                    time.sleep(0.5)
                    px.forward(0)

                    # 交替改变方向（先右转，后左转）
                    search_turn = -search_turn

    finally:
        px.stop()
        print("Vehicle Fully stopped")

