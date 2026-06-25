import math


class PID:
    def __init__(self, error, kp, ki, kd, starti=0, settle_error=1, settle_time=250, timeout=0, update_period=10):
        self.error = error; 
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.starti = starti

        self.settle_error = settle_error
        self.settle_time = settle_time
        self.timeout = timeout
        self.update_period = update_period

        self.accumulated_error = 0
        self.previous_error = error
        self.time_spent_settled = 0
        self.time_spent_running = 0

    def compute(self, error):
        if self.starti == 0 or math.fabs(error) < self.starti:
            self.accumulated_error += error

        if (error > 0 > self.previous_error) or (error < 0 < self.previous_error):
            self.accumulated_error = 0

        derivative = (error - self.previous_error)

        output = (
            self.kp * error
            + self.ki * self.accumulated_error
            + self.kd * derivative
        )

        self.previous_error = error

        if math.fabs(error) < self.settle_error:
            self.time_spent_settled += self.update_period
        else:
            self.time_spent_settled = 0

        self.time_spent_running += self.update_period

        return output

    def is_settled(self):
        if self.timeout != 0 and self.time_spent_running > self.timeout:
            return True

        if self.time_spent_settled > self.settle_time:
            return True

        return False

    def reset(self):
        self.accumulated_error = 0
        self.previous_error = 0
        self.time_spent_settled = 0
        self.time_spent_running = 0
