import random
import time

class OBD_Simulator:
    def __init__(self):
        self.rpm = random.randint(700, 900)  # Idle RPM
        self.speed = 0
        self.coolant_temp = random.randint(70, 90)  # Normal temp

    def get_rpm(self):
        """Simulate RPM changes"""
        if self.speed > 0:
            self.rpm = random.randint(1500, 4000)
        else:
            self.rpm = random.randint(700, 900)
        return self.rpm

    def get_speed(self):
        """Simulate speed changes"""
        if random.random() > 0.5:
            self.speed += random.randint(1, 5)
        else:
            self.speed = max(0, self.speed - random.randint(1, 3))
        return self.speed

    def get_coolant_temp(self):
        """Simulate coolant temperature"""
        self.coolant_temp = min(110, self.coolant_temp + random.uniform(-0.5, 0.5))
        return round(self.coolant_temp, 1)

    def get_all_data(self):
        """Return all simulated parameters"""
        return {
            "RPM": self.get_rpm(),
            "Speed": self.get_speed(),
            "Coolant Temp": self.get_coolant_temp()
        }

# Test the simulator
if __name__ == "__main__":
    simulator = OBD_Simulator()
    while True:
        print(simulator.get_all_data())  # Print simulated values
        time.sleep(1)
