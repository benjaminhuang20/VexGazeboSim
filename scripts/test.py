import subprocess
import time

from gz.transport13 import Node
from gz.msgs10.imu_pb2 import IMU as ImuMsg
from gz.msgs10.twist_pb2 import Twist

def send_cmd(linear_x, angular_z):
    msg = f"linear {{ x: {linear_x} }} angular {{ z: {angular_z} }}"
    cmd = [
        "gz", "topic",
        "-t", "/cmd_vel",
        "-m", "gz.msgs.Twist",
        "-p", msg
    ]
    subprocess.run(cmd)


send_cmd(0.5, 0.0)
time.sleep(2)
send_cmd(0.0, 0.0)