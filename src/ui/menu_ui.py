



class MenuUi:

    def menu(self):
        print("\nChoose search method:")
        print("1. Search by item name")
        print("2. Search by farma_id")
        print("3. Search by bar_code")
        print("4. Use camera to search")
        print("5. Show all orders")
        print("6. Exit program")
        choice = int(input())
        return choice