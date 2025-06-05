# 💳 ATM Simulator (Client-Server Banking System)

Welcome to the **ATM Simulator**, a Python-based client-server application that emulates an Automated Teller Machine system. This project demonstrates networking, multithreading, and file-based data persistence while providing a clean command-line interface for managing simple banking operations.

---

## 🚀 Features

- 🧑‍💼 Create Account with optional initial deposit
- 🔐 Secure Login with PIN authentication
- 💰 Deposit and Withdraw funds
- 🧾 Check Balance
- 🔁 Logout and Exit gracefully
- 🧵 Threaded server handles multiple clients simultaneously
- 📁 Simple file-based persistence using `accounts.txt`
- 🧠 Thread safety with locks to prevent data races

---

## ⚙️ How It Works

This is a client-server system where:

- The **Server** handles incoming client connections and manages the bank database.
- The **Client** (used by the ATM UI or CLI) sends commands like `LOGIN`, `DEPOSIT`, `BALANCE`, etc.
- The **ATM UI** (`atm_ui.py`) provides an interactive menu-driven interface for users.

All communication takes place over TCP using Python's built-in `socket` module.

---

## 🧪 Example Interaction

```
=== ATM Simulator ===
1. Login
2. Create Account
3. Exit
Select option: 2
Choose account number: 12345
Choose PIN: 6789
Initial deposit (optional, default 0): 100
SUCCESS Account 12345 created

1. Login
Select option: 1
Enter account number: 12345
Enter PIN: 6789
SUCCESS Logged in as 12345

1. Check Balance
2. Deposit
3. Withdraw
4. Logout
Select option: 1
SUCCESS Current balance: 100.0
```

---

## 📌 Notes

- The server stores all accounts in `accounts.txt` (auto-created).
- Each client runs independently and communicates over the network.
- Ensure the server is running before launching the client or ATM UI.

---

## 🧹 Future Improvements (Optional)

- Use hashed passwords instead of plain PINs
- Implement network encryption (SSL)
- Add support for transaction history
- Switch to SQLite or PostgreSQL for better scalability
- Web or GUI frontend

---

## ✅ Requirements

- Python 3.6+
- No external libraries required

---

## 📜 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute.

---

## 🧠 Conclusion

This ATM Simulator was built as a learning project to reinforce core concepts in:
- **Networking** with `sockets`
- **Concurrency** using `threading`
- **File-based persistence**
- **Client-server architecture**

Whether you're a beginner looking to learn Python networking or just want to simulate banking operations in the terminal, this project is a great place to start!
