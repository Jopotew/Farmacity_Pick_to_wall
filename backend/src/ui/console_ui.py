class Console:
    def menu(self):
        print("\nChoose search method:")
        print("1. Ingreso Manual")
        print("2. Utilizar lector")

        try:
            while True:
                choice = int(input("Enter your choice: "))
                if 1 <= choice <= 2:
                    return choice
                else:
                    print("Invalid choice, please select a number between 1 and 6.")
        except ValueError:
            print("Invalid input, please enter a valid number.")
