from gpiozero import DigitalOutputDevice, Button


class DC:

    def __init__(self, direction_pin_1, direction_pin_2):
        self.direction_1 = DigitalOutputDevice(direction_pin_1)
        self.direction_2 = DigitalOutputDevice(direction_pin_2)

        self.write_direction("off","1")
        self.write_direction("off","2")

    def write_direction(self, direction, state):
        if state == "on" and direction == "1":
            self.direction_1.on()
        elif state == "on" and direction == "2":
            self.direction_2.on()
        elif state == "off" and direction == "1":
            self.direction_1.off()
        elif state == "off" and direction == "2":
            self.direction_2.off()


