from client import ATMClient

class ATMSimulator:
    def __init__(self):
        self.client = ATMClient()
        self.logged_in = False

    def run(self):
        print("=== ATM Simulator ===")
        if not self.client.connect():
            print("Failed to connect to ATM server")
            return

        try:
            while True:
                if not self.logged_in:
                    self.show_login_menu()
                else:
                    self.show_main_menu()
        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            self.client.disconnect()

    def show_login_menu(self):
        print("\n1. Login")
        print("2. Create Account")
        print("3. Exit")
        choice = input("Select option: ").strip()
        
        if choice == "1":
            account_number = input("Enter account number: ").strip()
            pin = input("Enter PIN: ").strip()
            
            response = self.client.send_command(f"LOGIN {account_number} {pin}")
            print(response)
            if response and response.startswith("SUCCESS"):
                self.logged_in = True
        elif choice == "2":
            account_number = input("Choose account number: ").strip()
            pin = input("Choose PIN: ").strip()
            initial_balance = input("Initial deposit (optional, default 0): ").strip()
            if not initial_balance:
                initial_balance = "0"
            response = self.client.send_command(f"CREATE {account_number} {pin} {initial_balance}")
            print(response)
        elif choice == "3":
            raise KeyboardInterrupt
        else:
            print("Invalid choice")

    def show_main_menu(self):
        print("\n1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Logout")
        choice = input("Select option: ").strip()
        
        if choice == "1":
            response = self.client.send_command("BALANCE")
            print(response)
        elif choice == "2":
            amount = input("Enter amount to deposit: ").strip()
            response = self.client.send_command(f"DEPOSIT {amount}")
            print(response)
        elif choice == "3":
            amount = input("Enter amount to withdraw: ").strip()
            response = self.client.send_command(f"WITHDRAW {amount}")
            print(response)
        elif choice == "4":
            response = self.client.send_command("LOGOUT")
            print(response)
            self.logged_in = False
        else:
            print("Invalid choice")

if __name__ == "__main__":
    simulator = ATMSimulator()
    simulator.run()