import time
import math
from gz.transport13 import Node
from gz.msgs10.imu_pb2 import IMU as ImuMsg

from helpers import HELPERS


class ImuSensor:
    def __init__(self, topic="/imuTest"):
        self.node = Node()
        self.topic = topic

        self.latest_msg = None
        self.latest_yaw = 0.0
        self.latest_angular_z = 0.0
        self.offset = 0
        self.sample_count = 0

        self.node.subscribe(ImuMsg, self.topic, self.callback)

    def quaternion_to_yaw(self, x, y, z, w):
        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        return math.degrees(math.atan2(siny_cosp, cosy_cosp))

    def callback(self, msg):
        self.latest_msg = msg

        q = msg.orientation
        self.latest_yaw = -self.quaternion_to_yaw(q.x, q.y, q.z, q.w)

        self.latest_angular_z = -msg.angular_velocity.z
        self.sample_count += 1

    def yaw(self):
        return HELPERS.reduce_negative_180_to_180(self.latest_yaw + self.offset)

    def angular_z(self):
        return self.latest_angular_z
    
    def set_heading(self, heading):
        self.offset = HELPERS.reduce_negative_180_to_180(heading - self.latest_yaw)

    def wait_for_update(self, previous_count=None, timeout=1.0):
        start = time.monotonic()

        while self.latest_msg is None:
            if time.monotonic() - start > timeout:
                return False
            time.sleep(0.01)

        if previous_count is None:
            return True

        while self.sample_count <= previous_count:
            if time.monotonic() - start > timeout:
                return False
            time.sleep(0.01)

        return True
