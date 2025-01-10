from gpiozero import Button

# A dictionary to store button instances mapped to unique position identifiers.
# Each button corresponds to a GPIO pin on the Raspberry Pi.

button_pos = {
    1: Button(10),  # Button mapped to GPIO pin 10
    2: Button(9),  # Button mapped to GPIO pin 9
    3: Button(11),  # Button mapped to GPIO pin 11
}
