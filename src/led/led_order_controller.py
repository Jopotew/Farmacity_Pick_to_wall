from time import sleep
import json
from button_led_position import led_pos, button_pos  #


grid_config = {"rows": 3, "columns": 3}  # Recieved from sql query

# Recieved from sql query
order_wave = {
    1: [
        {"farma_id": 22960, "item_name": "RENNIE X 36 COMPRIMIDOS",
            "bar_code": 7793640117230},
        {"farma_id": 23207, "item_name": "ORALSONE TOPICO SOLUCION X 20 ML",
            "bar_code": 7791984000072},
        {"farma_id": 25939, "item_name": "ACTRON X 10 CAPSULAS BLANDAS",
            "bar_code": 7793640215479},
    ],
    2: [
        {"farma_id": 29273, "item_name": "BUSCAPINA GRAGEAS X 20",
            "bar_code": 7795312108393},
        {"farma_id": 48104, "item_name": "BAYASPIRINA X 10 BLISTER",
            "bar_code": 8881110010221},
    ],
    3: [
        {"farma_id": 145303, "item_name": "MYLANTA LIMON TABLETAS X 24",
            "bar_code": 7796285275440},
        {"farma_id": 152643, "item_name": "FLORATIL VL X 10 CAPSULAS",
            "bar_code": 7795337990997},
    ],
    4: [
        {"farma_id": 33212, "item_name": "PARACETAMOL 500MG X 20",
            "bar_code": 7794321122334},
        {"farma_id": 44223, "item_name": "IBUPROFENO 400MG X 10",
            "bar_code": 7795321144455},
    ],
    5: [
        {"farma_id": 55234, "item_name": "DICLOFENAC 50MG X 20",
            "bar_code": 7796321166677},
        {"farma_id": 77256, "item_name": "LOPERAMIDA 2MG X 10",
            "bar_code": 7798321122001},
    ],
    6: [
        {"farma_id": 77256, "item_name": "LOPERAMIDA 2MG X 10",
            "bar_code": 7798321122001},
        {"farma_id": 88267, "item_name": "OMEPRAZOL 20MG X 14",
            "bar_code": 7799321133112},
    ],
    7: [
        {"farma_id": 99278, "item_name": "AMOXICILINA 500MG X 20",
            "bar_code": 7790321144223},
        {"farma_id": 102389, "item_name": "CIPROFLOXACINA 500MG X 10",
            "bar_code": 7791321155334},
    ],
    8: [
        {"farma_id": 112490, "item_name": "METFORMINA 850MG X 30",
            "bar_code": 7792321166445},
        {"farma_id": 122591, "item_name": "GLIBENCLAMIDA 5MG X 30",
            "bar_code": 7793321177556},
    ],
    9: [
        {"farma_id": 132692, "item_name": "ATENOLOL 50MG X 30",
            "bar_code": 7794321188667},
        {"farma_id": 142793, "item_name": "ENALAPRIL 10MG X 30",
            "bar_code": 7795321199778},
    ]
}


def receive_and_sort_order_wave(order_wave, grid_config, pos_removed=None):
    """
    Distribute orders into a grid based on rows, columns, and optionally remove a position.

    Args:
        order_wave (dict): Dictionary with multiple orders.
        grid_config (dict): Dictionary with "rows" and "columns" to define the grid layout.
        pos_removed (int): Position to be removed from the grid (optional).

    Returns:
        dict: Dictionary with grid positions as keys and orders (dict) as values.
    """
    # Grid dimensions
    rows = grid_config["rows"]
    columns = grid_config["columns"]

    # Generate the grid positions, excluding the removed position if given
    total_positions = rows * columns
    grid_positions = [i for i in range(
        1, total_positions + 1) if i != pos_removed]

    # Prepare the result dictionary
    sorted_order = {}
    order_keys = list(order_wave.keys())  # Order keys to iterate

    # Map each order to the available grid positions
    for idx, position in enumerate(grid_positions):
        if idx < len(order_keys):
            # Place the order dict
            sorted_order[position] = order_wave[order_keys[idx]]
        else:
            break  # Stop when there are no more orders

    return sorted_order


def search_item_by_partial_name(sorted_order, partial_name):
    """
    Search for items in orders that start with the provided partial name.
    Shows all instances and differentiates between them.
    """
    matches = []
    for position, items in sorted_order.items():
        # Use index to differentiate items in the same position
        for index, item in enumerate(items):
            if item["item_name"].lower().startswith(partial_name.lower()):
                matches.append(
                    {"position": position, "index": index, "item": item})
    return matches


def search_item_by_farma_id_and_bar_code(sorted_order, search_key, search_value):
    """
    Search for an item by its farma_id or bar_code and return all matches.

    Args:
        sorted_order (dict): The orders sorted in grid positions.
        search_key (str): The key to search for ('farma_id' or 'bar_code').
        search_value (int/str): The value to search for.

    Returns:
        list: A list of matches with their position and index.
    """
    matches = []
    for position, items in sorted_order.items():
        for index, item in enumerate(items):
            if item.get(search_key) == search_value:
                matches.append(
                    {"position": position, "index": index, "item": item})
    return matches


def search_item_by_data(sorted_order, search_item_data):
    """
    Search for an item by its full data (dictionary) in the orders.
    """
    for position, items in sorted_order.items():
        for item in items:
            if item == search_item_data:
                return {"position": position, "item": item}
    return None


def process_item_removal(sorted_order, position, item):
    """
    Handles LED and button interaction for the removal of an item at a specific position.
    """
    # Debugging to verify the inputs
    print("Current position:", position)
    print("Current items at position:", sorted_order[position])
    print("Item to remove:", item)

    # Check LED and button configuration
    search_led = led_pos[position]["red"]
    completion_led = led_pos[position]["green"]
    button = button_pos[position]

    print(f"Item '{item['item_name']}' found in position {position}. Waiting for button press...")

    # Turn on search LED
    search_led.on()

    # Wait for button press
    button.wait_for_press()
    print(f"Button pressed! Removing '{item['item_name']}' from position {position}.")

    # Turn off search LED
    search_led.off()

    # Remove the item
    try:
        sorted_order[position].remove(item)  # Ensure the exact item matches
    except ValueError:
        print(f"Error: Item {item} not found in position {position}.")
        return

    # If the position list is empty, mark order complete
    if not sorted_order[position]:
        print(f"Order at position {position} is now complete!")
        completion_led.on()
        sleep(2)
        completion_led.off()



def search_and_remove_item_by_name(sorted_order, partial_name):
    """
    Search for an item by partial name, confirm it, and remove it.
    This function removes only the first matched item from the orders.
    """
    # Search for the first match in positional order
    for position in sorted(sorted_order.keys()):  # Sort positions to ensure order
        for item in sorted_order[position]:
            if item["item_name"].lower().startswith(partial_name.lower()):
                # Process and remove the first matched item
                print(f"Found '{item['item_name']}' in position {position}.")
                confirmation = input(
                    f"Is this the item you were looking for? '{item['item_name']}' (yes/no): ").strip().lower()
                if confirmation == "yes":
                    process_item_removal(position, item)
                    return  # Stop after removing the first match

    print(f"No confirmed items found starting with '{partial_name}'.")


def search_and_remove_item_by_data(sorted_order, search_item_data):
    """
    Search for an item by its full data, confirm it, and remove it.
    This function removes only the first matched item from the orders.
    """
    # Iterate through positions in sorted order
    for position in sorted(sorted_order.keys()):  # Sort positions to ensure order
        for item in sorted_order[position]:
            if item == search_item_data:
                # Found the first match, confirm with the user
                print(
                    f"Found item '{item['item_name']}' at position {position}.")
                confirmation = input(
                    f"Is this the item you were looking for? '{item}' (yes/no): ").strip().lower()
                if confirmation == "yes":
                    process_item_removal(sorted_order, position, item)
                    return  # Stop after removing the first match

    print(f"Item with data {search_item_data} not found in any order.")


def main():
    """
    Main program loop to simulate item search and button interaction.
    """
    try:
        sorted_order = receive_and_sort_order_wave(
            order_wave, grid_config)  # Simulated SQL queries
        while True:
            print("\nChoose search method:")
            print("1. Search by item name")
            print("2. Search by farma_id")
            print("3. Search by bar_code")
            print("4. Show all orders")
            print("Type 'exit' to quit.")
            choice = input("Enter choice: ")

            if choice.lower() == "exit":
                print("Exiting program...")
                break

            if choice == "1":
                partial_name = input("Enter the partial item name to search: ")
                matches = search_item_by_partial_name(
                    sorted_order, partial_name)
                if matches:
                    print("Matches found:")
                    for match in matches:
                        pos = match["position"]
                        idx = match["index"]
                        item = match["item"]
                        print(f"Position {pos}, Index {idx}: {item}")
                    position = int(
                        input("Enter the position of the item to remove: "))
                    index = int(
                        input("Enter the index of the item to remove: "))
                    item_to_remove = sorted_order[position][index]
                    process_item_removal(
                        sorted_order, position, item_to_remove)
                else:
                    print(f"No items found starting with '{partial_name}'.")

            elif choice == "2":
                farma_id = int(input("Enter the farma_id to search: "))
                matches = search_item_by_farma_id_and_bar_code(
                    sorted_order, "farma_id", farma_id)
                if matches:
                    print("Matches found:")
                    for match in matches:
                        pos = match["position"]
                        idx = match["index"]
                        item = match["item"]
                        print(f"Position {pos}, Index {idx}: {item}")
                    position = int(
                        input("Enter the position of the item to remove: "))
                    index = int(
                        input("Enter the index of the item to remove: "))
                    item_to_remove = sorted_order[position][index]
                    process_item_removal(
                        sorted_order, position, item_to_remove)
                else:
                    print(f"No items found with farma_id '{farma_id}'.")

            elif choice == "3":
                bar_code = input("Enter the bar_code to search: ").strip()
                matches = search_item_by_farma_id_and_bar_code(
                    sorted_order, "bar_code", bar_code)
                if matches:
                    print("Matches found:")
                    for match in matches:
                        pos = match["position"]
                        idx = match["index"]
                        item = match["item"]
                        print(f"Position {pos}, Index {idx}: {item}")
                    position = int(
                        input("Enter the position of the item to remove: "))
                    index = int(
                        input("Enter the index of the item to remove: "))
                    item_to_remove = sorted_order[position][index]
                    process_item_removal(
                        sorted_order, position, item_to_remove)
                else:
                    print(f"No items found with bar_code '{bar_code}'.")

            elif choice == "4":
                print("Current Orders:")
                for position, items in sorted_order.items():
                    print(f"Position {position}: {items}")

            else:
                print("Invalid choice. Please select a valid option or 'exit'.")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
    finally:
        print("Cleaning up GPIO...")
        for position in led_pos:
            led_pos[position]["red"].off()
            led_pos[position]["green"].off()


if __name__ == "__main__":
    main()

"""
    NO HAY LUCES (CONECTADAS AL GPIO/PINES RASPI. NO SE PUEDE USAR EL MISMO EN OTRA POSITION) SUFICIENTES PARA CORRER CON ESTA WAVE, ACOMODAR ORDENES PARA QUE SEAN LAS RIMERAS 3
    SALE UN ERROR AL NO PONER NADA, MUETRA LISTA DE OTODS LOS ITEMS, NO DEBERIA. O SI NOC.
    VALUE ERROR : LIST.REMOVE(X) : X NOT IN LIST LINE 172. SORTED ORDER [POSITION].REMOVE(ITEM)
"""
