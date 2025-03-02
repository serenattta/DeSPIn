from picarx import Picarx

def main():
    px = Picarx()

    while True:
        distance = round(px.ultrasonic.read(), 2)
        if distance < 20:
            print("distance: ",distance)


if __name__ == "__main__":
    main()
