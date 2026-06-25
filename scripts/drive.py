import math
import time
from pid import PID
from imu import ImuSensor
from helpers import HELPERS

from gz.transport13 import Node
from gz.msgs10.vector2d_pb2 import Vector2d

class Drive: 
    def __init__(self, imu, topic="/tank_cmd"):
        self.node = Node()
        self.imu = ImuSensor(imu) #STRING
        self.x = 0
        self.y = 0
        self.heading = 0
        
        self.turn_max_voltage = 6
        # self.turn_kp = 0.08
        self.turn_kp = 0.4
        self.turn_ki = 0.03
        self.turn_kd = 3
        self.turn_starti = 15;
    
        self.turn_settle_error = 2
        self.turn_settle_time = 100
        self.turn_timeout = 3000

        self.topic = topic
        self.pub = self.node.advertise(self.topic, Vector2d)

        self.currLeftVolts = 0
        self.currRightVolts = 0

        
    def set_turn_constants(self, turn_max_voltage, turn_kp, turn_ki, turn_kd, turn_starti):
        self.turn_max_voltage = turn_max_voltage
        self.turn_kp = turn_kp
        self.turn_ki = turn_ki
        self.turn_kd = turn_kd
        self.turn_starti = turn_starti

    def set_turn_exit_conditions(self, turn_settle_error, turn_settle_time, turn_timeout):
        self.turn_settle_error = turn_settle_error
        self.turn_settle_time = turn_settle_time
        self.turn_timeout = turn_timeout
        
    def setLeftPower(self, volts):
        msg = Vector2d()
        msg.x = volts
        self.currLeftVolts = volts; 
        msg.y = self.currRightVolts 
        self.pub.publish(msg)

    def setRightPower(self, volts):
        msg = Vector2d()
        msg.y = volts
        self.currRightVolts = volts; 
        msg.x = self.currLeftVolts 
        self.pub.publish(msg)

    def drive_with_voltage(self, left, right):
        msg = Vector2d()
        msg.x = left
        msg.y = right
        self.currLeftVolts = left
        self.currRightVolts = right
        self.pub.publish(msg)

    def stop_drive(self):
        for _ in range(5):
            self.drive_with_voltage(0, 0)
            time.sleep(0.01)

    
    def leftPosition(self):
        pass

    def rightPosition(self):
        pass

    def drive_distance(self, distance):
        pass

    def drive_distance(self, distance, heading):
        pass

    def turn_to_angle(self, heading):
        heading = HELPERS.reduce_negative_180_to_180(heading)
        self.imu.wait_for_update()
        last_imu_sample = self.imu.sample_count

        turnPID = PID(
            HELPERS.reduce_negative_180_to_180(heading - self.imu.yaw()),
            self.turn_kp,
            self.turn_ki,
            self.turn_kd,
            self.turn_starti,
            self.turn_settle_error,
            self.turn_settle_time,
            self.turn_timeout)

        try:
            error = HELPERS.reduce_negative_180_to_180(heading - self.imu.yaw())

            while not turnPID.is_settled():
                error = HELPERS.reduce_negative_180_to_180(heading - self.imu.yaw())

                output = turnPID.compute(error)
                output = HELPERS.clamp(
                    output,
                    -self.turn_max_voltage,
                    self.turn_max_voltage)

                print(
                    "target:", heading,
                    "yaw:", self.imu.yaw(),
                    "error:", error,
                    "output:", output)

                self.drive_with_voltage(output, -output)
                time.sleep(0.01) # 10 msec
        finally:
            self.stop_drive()
            final_error = HELPERS.reduce_negative_180_to_180(heading - self.imu.yaw())
            print("Done with turn; error:", final_error)
            if abs(final_error) > self.turn_settle_error:
                print("Warning: turn ended before settling.")


    def turn_to_point(self, x, y):
        pass

    def drive_to_point(self, x, y):
        pass

    def get_x(self):
        pass

    def get_y(self):
        pass

    def get_heading(self):
        pass

    def set_pose(self, x, y, heading):
        pass

    def track_pos(self):
        pass
