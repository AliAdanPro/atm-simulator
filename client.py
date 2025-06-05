# client.py
import socket
import sys

class ATMClient:
    def __init__(self, host='127.0.0.1', port=65432):
        self.host = host
        self.port = port
        self.connected = False
        self.socket = None

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(self.receive_response())  # Welcome message
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def send_command(self, command):
        if not self.connected:
            print("Not connected to server")
            return None
        try:
            self.socket.sendall(command.encode())
            return self.receive_response()
        except Exception as e:
            print(f"Communication error: {e}")
            self.connected = False
            return None

    def receive_response(self):
        try:
            return self.socket.recv(1024).decode()
        except Exception as e:
            print(f"Receive error: {e}")
            self.connected = False
            return None

    def disconnect(self):
        if self.connected:
            self.send_command("EXIT")
            self.socket.close()
            self.connected = False

    def run(self):
        if not self.connect():
            return

        try:
            while True:
                command = input("ATM> ").strip()
                if not command:
                    continue
                
                response = self.send_command(command)
                if response == "GOODBYE":
                    print("Disconnecting...")
                    break
                elif response:
                    print(response)
                
                if not self.connected:
                    print("Disconnected from server")
                    break
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            self.disconnect()


def main():
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
    else:
        host = '127.0.0.1'
        port = 65432

    client = ATMClient(host, port)
    client.run()


if __name__ == "__main__":
    main()