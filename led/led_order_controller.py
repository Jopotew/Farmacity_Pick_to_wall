from gpiozero import LED, Button
from time import sleep
import json
import button_led_position

# Define GPIO LEDs and Button
led_gpio = led_position
button_po = button_pos

# Load order data from JSON file
with open("order.json", "r") as file:
    order_data = json.load(file)

# Orders loaded from JSON
order_position = {
    1: [
        {"farma_id": 22960, "item_name": "RENNIE X 36 COMPRIMIDOS", "bar_code": 7793640117230},
        {"farma_id": 23207, "item_name": "ORALSONE TOPICO SOLUCION X 20 ML", "bar_code": 7791984000072},
        {"farma_id": 25939, "item_name": "ACTRON X 10 CAPSULAS BLANDAS", "bar_code": 7793640215479},
    ],
    2: [
        {"farma_id": 29273, "item_name": "BUSCAPINA GRAGEAS X 20", "bar_code": 7795312108393},
        {"farma_id": 48104, "item_name": "BAYASPIRINA X 10 BLISTER", "bar_code": 8881110010221},
    ],
    3: [
        {"farma_id": 145303, "item_name": "MYLANTA LIMON TABLETAS X 24", "bar_code": 7796285275440},
        {"farma_id": 152643, "item_name": "FLORATIL VL X 10 CAPSULAS", "bar_code": 7795337990997},
    ]
}

search_led = "red"
completion_led = "green"

def search_item_by_partial_name(order_position, partial_name):
    """
    Search for items in orders that start with the provided partial name.
    """
    matches = []
    for position, items in order_position.items():
        for item in items:
            if item["item_name"].lower().startswith(partial_name.lower()):
                matches.append({"position": position, "item": item})
    return matches

def search_and_remove_item_by_name(order_position, partial_name, led_gpio, button):
    """
    Search for an item by partial name in the orders, confirm the item, and remove it.
    """
    matches = search_item_by_partial_name(order_position, partial_name)
    if not matches:
        print(f"No items found starting with '{partial_name}'.")
        return

    for match in matches:
        position = match["position"]
        item = match["item"]
        confirmation = input(f"Is this the item you were looking for? '{item['item_name']}' (yes/no): ").strip().lower()
        if confirmation == "yes":
            print(f"Item '{item['item_name']}' found in position {position}. Waiting for button press...")
            led_gpio[search_led].on()

            button.wait_for_press()
            print(f"Button pressed! Removing '{item['item_name']}' from position {position}.")
            led_gpio[search_led].off()

            # Remove the item from the order
            order_position[position].remove(item)

            # Check if the order is complete 
            if not order_position[position]:
                print(f"Order at position {position} is now complete!")
                led_gpio[completion_led].on()
                sleep(2)
                led_gpio[completion_led].off()

            return  

    print("No items were confirmed for removal.")

def search_and_remove_item_by_data(order_position, search_item_data, led_gpio, button):
    """
    Search for an item by its full data (dictionary) in the orders, confirm it, and remove it.
    """
    for position, items in order_position.items():
        for i, item in enumerate(items):
            if item == search_item_data:
                print(f"Item with data {search_item_data} found in position {position}. Waiting for button press...")
                led_gpio[search_led].on()

                button.wait_for_press()
                print(f"Button pressed! Removing item with data {search_item_data} from position {position}.")
                led_gpio[search_led].off()

                items.pop(i)

                if not items:
                    print(f"Order at position {position} is now complete!")
                    led_gpio[completion_led].on()
                    sleep(2)
                    led_gpio[completion_led].off()

                return  
    print(f"Item with data {search_item_data} not found in any order.")

def main():
    """
    Main program loop to simulate item search and button interaction.
    """
    try:
        while True:
            
            print("\nChoose search method:")
            print("1. Search by item name")
            print("2. Search by item data (JSON)")
            print("Type 'exit' to quit.")
            choice = input("Enter choice: ")

            if choice.lower() == "exit":
                print("Exiting program...")
                break

            if choice == "1":
                partial_name = input("Enter the partial item name to search: ")
                search_and_remove_item_by_name(order_position, partial_name, led_gpio, button)
            elif choice == "2":
                try:
                    search_item_data = input(
                        "Enter the full item data as JSON (e.g., {'farma_id': 22960, 'item_name': '...', 'bar_code': ...}): "
                    )
                    search_item_data = json.loads(search_item_data.replace("'", '"'))  # Safely parse input as JSON
                    search_and_remove_item_by_data(order_position, search_item_data, led_gpio, button)
                except json.JSONDecodeError:
                    print("Invalid JSON format. Please try again.")
            else:
                print("Invalid choice. Please select 1, 2, or 'exit'.")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        print("Cleaning up GPIO...")
        for led in led_gpio.values():
            led.off()

if __name__ == "__main__":
    print(led_gpio)
    #main()
