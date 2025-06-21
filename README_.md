
# 💳 SKF ATM System

A secure and user-friendly desktop ATM simulation built with Python and Tkinter. This application allows users to log in, manage their balance, withdraw and deposit funds, view transaction history, and securely change their PIN.

## 🧰 Features

- 🛡 Secure login system using PIN authentication
- 💰 Balance inquiry
- 💵 Withdrawals (up to Rs. 25,000 in multiples of Rs. 5.00)
- 💸 Deposits (up to Rs. 90,000 in multiples of Rs. 5.00)
- 🧾 Transaction logging
- 🔐 PIN change functionality
- 📜 Transaction history viewer
- 💡 User-friendly GUI with a modern design and color scheme

## 🖼 GUI Preview

> This app uses **Tkinter's themed widgets (`ttk`)** for a professional GUI appearance with color styling and layouts for different operations.

## 📂 Directory Structure

```
.
├── users/                # Stores user data (PIN and balance)
├── transactions/         # Stores user transaction logs
├── icon.png              # Optional application icon
├── atm_app.py            # Main application script
└── README.md             # Project documentation
```

## 🏁 Getting Started

### ✅ Prerequisites

- Python 3.7+
- `tkinter` module (comes pre-installed with standard Python distributions)

### 📦 Installation

1. Clone or download this repository:
   ```bash
   git clone https://github.com/yourusername/skf-atm-system.git
   cd skf-atm-system
   ```

2. Run the application:
   ```bash
   python atm_app.py
   ```

3. If `icon.png` is missing, the app will still run without it.

## 👥 Default User Info

- Default PIN: `5678`
- Default Balance: `Rs. 250,000`

On first login with any new Account ID, this default information is used.

## 📝 Notes

- PINs are hashed using SHA-256 for demonstration purposes.
- Data is stored as plain `.txt` files under `users/` and `transactions/`.

## ⚠ Limitations

- This application is designed for **demonstration and academic purposes**.
- Not intended for real banking environments.
- No real encryption or database is used beyond SHA-256 hashing.

## 📜 License

MIT License © 2025 SKF Bank Simulation

## 🤝 Acknowledgements

- Inspired by modern ATM interfaces.
- Developed using Python and the `tkinter` GUI toolkit.

---

> Developed by [Your Name / Institution]
