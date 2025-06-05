import socket
import threading
from bank import Bank

class ATMServer:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.bank = Bank()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = False

    def start(self): 
        print("Starting ATM Server...")
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"ATM Server started on {self.host}:{self.port}")
        self.running = True

        try:
            while self.running:
                client_socket, addr = self.server_socket.accept()
                print(f"New connection from {addr}")
                client_handler = ClientHandler(client_socket, addr, self.bank)
                client_handler.start()
        except KeyboardInterrupt:
            print("Shutting down server...")
        finally:
            self.server_socket.close()

    def stop(self):
        self.running = False
        try:
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.host, self.port))
        except:
            pass

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, addr, bank):
        super().__init__()
        self.client_socket = client_socket
        self.addr = addr
        self.bank = bank
        self.current_account_number = None
        self.current_pin = None

    def run(self):
        try:
            with self.client_socket:
                print(f"Connection established with {self.addr}")
                self.client_socket.sendall(b"Welcome to ATM Server. Please authenticate.\n")
                while True:
                    data = self.client_socket.recv(1024).decode().strip()
                    if not data:
                        break
                    response = self.process_command(data)
                    self.client_socket.sendall((response + '\n').encode())
                    if response == "GOODBYE":
                        break
        except ConnectionResetError:
            print(f"Client {self.addr} disconnected abruptly")
        finally:
            print(f"Connection with {self.addr} closed")

    def process_command(self, command):
        parts = command.split()
        if not parts:
            return "ERROR Invalid command"

        cmd = parts[0].upper()

        if cmd == "CREATE" and len(parts) >= 3:
            account_number, pin = parts[1], parts[2]
            try:
                initial_balance = float(parts[3]) if len(parts) > 3 else 0
            except ValueError:
                return "ERROR Invalid initial balance"
            if self.bank.create_account(account_number, pin, initial_balance):
                return f"SUCCESS Account {account_number} created"
            else:
                return "ERROR Account already exists"

        elif cmd == "LOGIN" and len(parts) == 3:
            account_number, pin = parts[1], parts[2]
            account = self.bank.authenticate(account_number, pin)
            if account:
                self.current_account_number = account_number
                self.current_pin = pin
                return f"SUCCESS Logged in as {account_number}"
            else:
                return "ERROR Invalid username or PIN"

        elif cmd == "BALANCE":
            if not self.current_account_number:
                return "ERROR Not authenticated"
            account = self.bank.authenticate(self.current_account_number, self.current_pin)
            if account:
                return f"SUCCESS Current balance: {account.get_balance()}"
            else:
                return "ERROR Failed to retrieve balance"

        elif cmd == "DEPOSIT" and len(parts) == 2:
            if not self.current_account_number:
                return "ERROR Not authenticated"
            try:
                amount = float(parts[1])
                if amount <= 0:
                    return "ERROR Amount must be positive"
                if self.bank.deposit(self.current_account_number, amount):
                
                    # Re-authenticate to get the updated balance 
                    account = self.bank.authenticate(self.current_account_number, self.current_pin)
                    return f"SUCCESS Deposited {amount}. New balance: {account.get_balance()}"
                else:
                    return "ERROR Deposit failed"
            except ValueError:
                return "ERROR Invalid amount"

        elif cmd == "WITHDRAW" and len(parts) == 2:
            if not self.current_account_number:
                return "ERROR Not authenticated"
            try:
                amount = float(parts[1])
                if amount <= 0:
                    return "ERROR Amount must be positive"
                if self.bank.withdraw(self.current_account_number, amount):
                    account = self.bank.authenticate(self.current_account_number, self.current_pin)
                    return f"SUCCESS Withdrew {amount}. New balance: {account.get_balance()}"
                else:
                    return "ERROR Insufficient funds"
            except ValueError:
                return "ERROR Invalid amount"

        elif cmd == "LOGOUT":
            self.current_account_number = None
            self.current_pin = None
            return "SUCCESS Logged out"

        elif cmd == "EXIT":
            return "GOODBYE"

        else:
            return "ERROR Unknown command"
if __name__ == "__main__":
    server = ATMServer()
    server.start()
