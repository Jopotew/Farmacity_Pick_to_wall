from gpiozero import LED, Button
from time import sleep
from order import order_position

led_gpio = {"red": LED(17), "green": LED(27)}  
button = Button(22)  


search_led = "red"
completion_led = "green"


def search_order(order_position, item_to_search):
    """
    Search for a specific item across all orders.
    If found, return the position and the specific order containing the item.
    """
    for position, items in order_position.items():
        if item_to_search in items:
            return position, items
    return None, None  


def search_and_process_item(order_position, item_to_search, led_gpio):
    """
    Searches for a specific item in the orders.
    - If found, turns on the red LED.
    - Waits for the button press to "confirm" the item removal.
    - Removes the item from the order and checks if the order is complete.
    - If the order is completed, turns on the green LED.
    """
    while True:
        
        position, order = search_order(order_position, item_to_search)
        
        if position:
            print(f"Item '{item_to_search}' found in order position {position}.")
            
            # Turn on the red LED
            red_led = led_gpio[search_led]
            red_led.on()
            print("Red LED ON. Waiting for button press to confirm...")

            # Wait for button press to confirm item processing
            button.wait_for_press()
            print(f"Button pressed. Removing '{item_to_search}' from the order.")
            button.wait_for_release()

            # Turn off the red LED after confirmation
            red_led.off()

            # Remove the item from the order
            order.remove(item_to_search)

            # Check if the order is now empty (completed)
            if not order:
                print(f"Order at position {position} is now complete.")
                
                # Turn on the green LED to signal completion
                green_led = led_gpio[completion_led]
                green_led.on()
                print("Green LED ON. Order completed!")
                sleep(2)  # Keep green LED on for 2 seconds
                green_led.off()
                break  # Exit the loop after completing the order

            else:
                print(f"Remaining items in order {position}: {order}")
                return order_position

        else:
            print(f"Item '{item_to_search}' not found in any order.")
            break


def turn_led_sequence(led_gpio):
    """
    Turn LEDs on and off sequentially.
    """
    red = led_gpio["red"]
    green = led_gpio["green"]
    print("Running LED sequence...")
    while True:
        red.on()
        sleep(1)
        red.off()
        green.on()
        sleep(1)
        green.off()
        sleep(1)


def button_control(led, led_gpio):
    """
    Turns on a specific LED when the button is pressed and turns it off when released.
    """
    print(f"Press the button to control the {led} LED.")
    selected_led = led_gpio[led]
    while True:
        button.wait_for_press()
        print("Button pressed. Turning on the LED.")
        selected_led.on()

        button.wait_for_release()
        print("Button released! Turning off the LED.")
        selected_led.off()


# Example Usage
try:
    item_to_find = "Lechuga"  # Example item to search for
    print("Starting the item search process...")
    search_and_process_item(order_position, item_to_find, led_gpio)
    

except KeyboardInterrupt:
    print("Exiting program.")

finally:
    # Cleanup LEDs on exit
    print("Cleaning up GPIO...")
    for led in led_gpio.values():
        led.off()




