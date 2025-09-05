# BankLite - Python Banking System with GUI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/Tkinter-GUI-orange.svg)](https://docs.python.org/3/library/tkinter.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A comprehensive banking management system built in Python featuring account creation, secure transactions, and an intuitive graphical user interface.

## 🚀 Features

### Core Banking Operations
- ✅ **Account Management**: Create accounts with unique IDs, PIN authentication, and mobile verification
- 💰 **Financial Transactions**: Deposit, withdraw, and transfer money with real-time balance updates
- 🔐 **Security Features**: PIN-based authentication, mobile number verification for PIN changes
- 📊 **Transaction History**: Detailed logs with timestamps for all account activities
- 💾 **Data Persistence**: JSON-based storage with automatic loading and saving

### User Interface
- 🖥️ **Graphical Interface**: Modern Tkinter-based GUI with scrollable design
- 🎯 **User-Friendly**: Intuitive dialogs for account selection and input validation
- 📱 **Responsive Design**: Mouse wheel scrolling support for various screen sizes
- ⚡ **Real-Time Feedback**: Status updates and error handling with clear messages

### Advanced Features
- 🔄 **Inter-Account Transfers**: Secure money transfers between accounts
- 📞 **Mobile Verification**: Unique mobile number registration for enhanced security
- 📈 **Transaction Logging**: Complete audit trail for compliance and transparency
- 🛡️ **Error Handling**: Comprehensive validation and user-friendly error messages

## 📋 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features in Detail](#features-in-detail)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Tkinter (usually included with Python)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/banklite.git
   cd banklite
   ```

2. Run the application:
   ```bash
   python main.py
   ```

## 📖 Usage

### Getting Started
1. Launch the application using `python main.py`
2. The GUI will open with a welcome screen
3. Use the buttons to perform various banking operations

### Key Operations

#### Creating an Account
- Click "Create Account"
- Enter name, initial balance, PIN, and mobile number
- Receive confirmation with your new account details

#### Making Transactions
- Authenticate with Account ID and PIN
- Choose deposit, withdrawal, or transfer
- View real-time balance updates

#### Viewing History
- Access detailed transaction logs
- Filter by date and transaction type
- Export history if needed

## 🎯 Features in Detail

### Account Creation
- Unique account ID generation
- PIN and mobile number validation
- Duplicate prevention for names and mobile numbers

### Transaction Management
- Real-time balance calculations
- Transaction history with timestamps
- Support for deposits, withdrawals, and transfers

### Security Features
- PIN-based authentication
- Mobile number verification for sensitive operations
- Secure data storage with JSON encryption

### User Interface
- Scrollable main window
- Modal dialogs for inputs
- Status bar for operation feedback
- Error messages with helpful guidance

## 📁 Project Structure

```
banklite/
├── account.py          # Account class and transaction methods
├── bank.py            # Bank management and file operations
├── gui.py             # Tkinter GUI implementation
├── main.py            # Application entry point
├── bank.json          # Data storage file
└── README.md          # Project documentation
```

### File Descriptions
- **account.py**: Handles individual account operations and data serialization
- **bank.py**: Manages multiple accounts, authentication, and persistence
- **gui.py**: Implements the graphical user interface with Tkinter
- **main.py**: Launches the application and initializes the GUI

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Future Enhancements

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Multi-user session management
- [ ] Interest calculation and account statements
- [ ] API endpoints for external integrations
- [ ] Mobile app companion
- [ ] Advanced reporting and analytics

## 📞 Support

If you have any questions or need help, please open an issue on GitHub.

---

**Made with ❤️ using Python and Tkinter**
