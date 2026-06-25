import math

class HELPERS:
    def reduce_negative_180_to_180(angle):
        while angle > 180:
            angle -= 360
        while angle < -180:
            angle += 360

        return angle
    
    def quaternion_to_yaw(x, y, z, w):
        siny_cosp = 2 * (w*z + x*y)
        cosy_cosp = 1 - 2 * (y*y + z*z)
        return math.degrees(math.atan2(siny_cosp, cosy_cosp))
    
    def clamp(value, lower, upper):
        if value > upper:
            return upper
        if value < lower:
            return lower
        return value
