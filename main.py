import tkinter as tk
from gui import BankLiteGUI

def main():
    """Main entry point for BankLite"""
    root = tk.Tk()
    app = BankLiteGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
