from gpiozero import DigitalOutputDevice, Button
import time

class StepperMotor:
    def __init__(self, 
                 step_pin, 
                 dir_pin, 
                 enable_pin=None, 
                 min_switch_pin=None, 
                 max_switch_pin=None):
        """
        step_pin        : GPIO pin for the STEP signal
        dir_pin         : GPIO pin for the DIRECTION signal
        enable_pin      : GPIO pin for the ENABLE signal (optional)
        min_switch_pin  : GPIO pin connected to the minimum limit switch (optional)
        max_switch_pin  : GPIO pin connected to the maximum limit switch (optional)
        """
        
        # Set up step, direction, and optionally enable pins
        self.step_pin = DigitalOutputDevice(step_pin)
        self.dir_pin = DigitalOutputDevice(dir_pin)
        
        self.enable_pin = None
        if enable_pin is not None:
            self.enable_pin = DigitalOutputDevice(enable_pin)
            # Depending on your driver, you may have to set enable_pin.off() or on()
            # to enable the motor. Check your driver’s datasheet.
            self.enable_pin.off()  # Example: off() might be 'enabled'
        
        # Set up limit switches if provided
        self.min_switch = None
        if min_switch_pin is not None:
            self.min_switch = Button(min_switch_pin, pull_up=True)
        
        self.max_switch = None
        if max_switch_pin is not None:
            self.max_switch = Button(max_switch_pin, pull_up=True)
        
    
    def calibrate(self):
        """
        Move the motor to find the minimum position, set that as 0,
        then move the motor to find the maximum position, record that,
        and optionally set self.neutral.
        """
        print("Starting calibration...")
        
        # 1) Find the min switch
        if self.min_switch:
            print("Moving to find minimum limit switch...")
            self.dir_pin.off()  # Example: off() might be 'reverse' direction
            while not self.min_switch.is_pressed:
                self._step_once()
            # Once we hit the min switch, set current position as 0
            self.position = 0
            self.min_position = 0
            print("Minimum found. Position set to 0.")
        
        # 2) Find the max switch
        if self.max_switch:
            print("Moving to find maximum limit switch...")
            self.dir_pin.on()  # Example: on() might be 'forward' direction
            while not self.max_switch.is_pressed:
                self._step_once()
                self.position += 1
            self.max_position = self.position
            print(f"Maximum found at position: {self.max_position}")
        
        self.neutral = self.max_position/2
        
        # Optionally define a neutral position
        self.neutral = self.max_position // 2
        print(f"Calibration done. min_position={self.min_position}, "
              f"max_position={self.max_position}, neutral={self.neutral}")

    def _step_once(self, delay=0.001):
        """
        Pulse the step pin once. Adjust 'delay' for motor speed.
        """
        # Step pin on
        self.step_pin.on()
        time.sleep(delay)
        # Step pin off
        self.step_pin.off()
        time.sleep(delay)

    def move_position(self, new_position):
        """
        Move the motor to a specified step position, respecting limit switches if present.
        """
        steps_to_move = new_position - self.position
        print(f"Moving from {self.position} to {new_position} (steps={steps_to_move})")
        
        if steps_to_move == 0:
            print("No movement needed.")
            return
        
        direction = 1 if steps_to_move > 0 else -1
        
        # Set direction pin
        if direction > 0:
            self.dir_pin.on()  # forward
        else:
            self.dir_pin.off() # reverse
        
        # Move step by step
        steps = abs(steps_to_move)
        for _ in range(steps):
            # Check if limit switch is about to be hit
            if direction < 0 and self.min_switch and self.min_switch.is_pressed:
                print("Min switch triggered; stopping movement.")
                self.position = self.min_position
                return
            if direction > 0 and self.max_switch and self.max_switch.is_pressed:
                print("Max switch triggered; stopping movement.")
                self.position = self.max_position
                return
            
            self._step_once()
            self.position += direction
        
        print(f"New position: {self.position}")

    def move_motor_max_position(self):
        """
        Go to max position.
        """
        self.move_position(self.max_position)

    def move_motor_min_position(self):
        """
        Go to min position.
        """
        self.move_position(self.min_position)
    
    def move_motor_neutral(self):
        """
        Move to neutral.
        """
        self.move_position(self.neutral)