
class PID(object):
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.expected_value = 0
        self.error = 0

        self.last_error = 0
        self.accumulate_error = 0
        
    def UpdateOutput(self, current_value):
        self.error = self.expected_value - current_value
        self.P_value = self.kp * self.error
        self.D_value = self.kd * (self.error - self.last_error)
        self.last_error = self.error
        self.accumulate_error = self.accumulate_error + self.error
        self.I_value = self.ki * self.accumulate_error

        PID_output = self.P_value + self.I_value + self.D_value

        return PID_output
    
    def SetExpectedOutput(self, expected_value):
        self.expected_value = expected_value

