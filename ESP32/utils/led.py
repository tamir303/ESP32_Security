from machine import Pin, PWM

# Set up RGB pins with PWM
#red = PWM(Pin(4))
#green = PWM(Pin(5))
#blue = PWM(Pin(18))

# Set PWM frequency
#red.freq(1000)
#green.freq(1000)
# blue.freq(1000)

def set_color(r, g, b):
    """Set the color of the RGB LED."""
    red.duty_u16(r)   # 0-65535 for duty cycle
    green.duty_u16(g)
    blue.duty_u16(b)