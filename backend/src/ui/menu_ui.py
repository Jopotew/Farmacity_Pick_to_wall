class MenuUi:

    def menu(self):
        print("\nChoose search method:")
        print("1. Search by item name")
        print("2. Search by farma_id")
        print("3. Search by bar_code")
        print("4. Show all orders")
        print("5. Exit program")
        try:
            choice = int(input("Enter your choice: "))
            if 1 <= choice <= 5:
                return choice
            else:
                print("Invalid choice, please select a number between 1 and 6.")
        except ValueError:
            print("Invalid input, please enter a valid number.")
