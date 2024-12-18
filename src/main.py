from services.order_service import OrderService

def main():
    """
    Main program loop to interact with the orders.
    """
    orderService = OrderService()
    sorted_order = orderService.getOrders()

    while True:
        item_name = input("Write the item you are looking for (or type 'exit' to quit): ")
        
        # Handle exit condition
        if item_name.lower() == "exit":
            print("Exiting...")
            break

        # Handle empty input
        if not item_name.strip():
            print("No input given.")
            continue

        # Search for the item
        item = orderService.search_by_name(sorted_order, item_name)
        if item is None:
            print("Item not found or invalid input.")
              
            continue

        # Remove the item if found
        sorted_order = orderService.remove_from_order(sorted_order, item)
        print("Order after removing item:")
        orderService.print_orders(sorted_order)


if __name__ == '__main__':
    main()
