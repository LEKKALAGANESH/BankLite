# BankLite - Console Banking System with GUI

## Overview
BankLite is a simple banking system implemented in Python. It allows users to create accounts, deposit and withdraw money, view balances and transaction history, and save data persistently. The project now includes a Tkinter-based graphical user interface (GUI) for improved user experience.

## Features
- Create new bank accounts with unique IDs, PIN authentication, and mobile number registration
- Deposit and withdraw money with input validation and balance checks
- Transfer money between accounts with secure authentication and recipient selection
- Change PIN with mobile number verification for enhanced security
- View account balance and detailed transaction history with timestamps
- Account selection dialogs for easy transfer recipient selection
- Scrollable GUI interface with mouse wheel support for all screen sizes
- Persistent data storage using JSON files with automatic data loading
- User-friendly GUI with advanced styling using Tkinter and ttk
- Comprehensive error handling and user feedback
- Transaction logging for all account activities including PIN changes

## Installation
1. Ensure Python 3.x is installed on your system.
2. Clone or download the repository.
3. Navigate to the `BankLite` directory.

## Usage
Run the application with:
```
python main.py
```
This will launch the GUI interface.

## How to Use Each Feature

### Creating an Account
1. Click "Create Account" button.
2. Enter account holder's name, initial balance, and set a PIN.
3. Enter your mobile number (used as unique identifier for security features).
4. After creation, a message will display your new Account ID, Mobile number, and PIN - save this information securely as it's needed for all authenticated operations.
5. Mobile number is validated to ensure uniqueness across all accounts.

### Depositing Money
1. Click "Deposit Money" button.
2. Enter your Account ID and PIN for authentication.
3. Enter the amount to deposit (must be positive).
4. View the updated balance in the success message.

### Withdrawing Money
1. Click "Withdraw Money" button.
2. Enter your Account ID and PIN for authentication.
3. Enter the amount to withdraw (must be positive and not exceed balance).
4. View the updated balance in the success message.

### Transferring Money
1. Click "Transfer Money" button.
2. Enter your Account ID and PIN for authentication.
3. Select the receiver account from the list of existing accounts.
4. Enter the amount to transfer (must be positive and not exceed your balance).
5. View both your new balance and the receiver's new balance in the success message.

### Changing PIN
1. Click "Change PIN" button.
2. Enter your Account ID.
3. Enter your registered mobile number for verification.
4. Enter your new PIN (must be at least 4 digits).
5. PIN will be changed and logged in transaction history.

### Viewing Balance
1. Click "View Balance" button.
2. Enter your Account ID and PIN for authentication.
3. View your current account details including balance.

### Viewing Transaction History
1. Click "View Transaction History" button.
2. Enter your Account ID and PIN for authentication.
3. View a list of all transactions with dates, types, amounts, and balances.

### Saving and Exiting
1. Click "Save & Exit" button to save all data to file and close the application.

## Why These Features Were Added

### Account Creation with ID and PIN Display
- **Why**: In real banking systems, customers receive account numbers and PINs immediately after account opening. This prevents confusion and ensures users know their credentials for future transactions.
- **Benefit**: Eliminates the need to guess or manually track account IDs, improving user experience and security.

### Transfer Money Feature
- **Why**: Money transfers between accounts are a core banking service, allowing customers to send money to family, friends, or businesses without physical cash.
- **Benefit**: Provides a secure, authenticated way to move funds, with proper validation and transaction logging.

### Account Selection for Transfers
- **Why**: In banking apps, users select recipients from contacts or account lists rather than entering IDs manually, reducing errors.
- **Benefit**: Prevents transfer failures due to incorrect account IDs and makes the process more user-friendly.

### Change PIN Feature
- **Why**: Real banking systems require secure PIN changes with identity verification to prevent unauthorized access, similar to how banks verify identity before allowing password changes.
- **Benefit**: Enhances security by requiring mobile number verification and ensures users can update their PINs securely when needed.

### GUI Interface
- **Why**: Modern banking systems use graphical interfaces for better accessibility and user experience compared to command-line interfaces.
- **Benefit**: Makes the system more intuitive for non-technical users and provides visual feedback for operations.

### Transaction History with Timestamps
- **Why**: Banking regulations require detailed transaction records for auditing and customer transparency.
- **Benefit**: Allows users to track their financial activity and detect any unauthorized transactions.

### Persistent Storage
- **Why**: Banking systems must maintain data integrity across sessions, similar to how banks store account information in databases.
- **Benefit**: Ensures user data is not lost when the application closes.

### Mobile Number Registration
- **Why**: Real banking systems use mobile numbers as unique identifiers for account verification and security features like PIN reset and two-factor authentication.
- **Benefit**: Provides an additional layer of security and enables secure account recovery features.

### Scrollable GUI Interface
- **Why**: Modern applications need to work on different screen sizes and resolutions, ensuring all features remain accessible regardless of window size.
- **Benefit**: Provides a responsive user experience with mouse wheel scrolling support for better usability on various devices.

### Comprehensive Error Handling
- **Why**: Banking applications must handle errors gracefully to prevent data loss and provide clear feedback to users about what went wrong.
- **Benefit**: Improves user experience by providing helpful error messages and preventing application crashes.

### Transaction Logging
- **Why**: Financial institutions are required by law to maintain detailed transaction records for auditing, compliance, and customer dispute resolution.
- **Benefit**: Provides complete audit trail and helps users track their financial activities.

## Project Structure
- `account.py`: Defines the Account class with methods for transactions and data serialization.
- `bank.py`: Defines the Bank class managing multiple accounts and file persistence.
- `gui.py`: Implements the Tkinter GUI for user interaction.
- `main.py`: Entry point to launch the GUI.
- `bank.json`: JSON file for storing account data.

## Future Improvements
- Add database support (e.g., SQLite) for better scalability.
- Implement multi-user support with session management.
- Enhance GUI with more features and responsive design.
- Add interest calculation and account statements.

## License
MIT License
