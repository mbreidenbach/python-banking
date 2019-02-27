from tkinter import *
import json


class MainWindow(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("User Login For BankingWorlds.edu")
        self.pack(fill=BOTH, expand=1)
        self.the_labels()
        self.the_buttons()
        self.the_entries()

    def the_labels(self):
        label_welcome = Label(self, text="Welcome to the website! Please sign in.")
        label_welcome.grid(row=0, column=0)
        label_userbox = Label(self, text="Username:")
        label_userbox.grid(row=2, column=0)
        label_passbox = Label(self, text="Password:")
        label_passbox.grid(row=3, column=0)

    def the_buttons(self):
        quit_button = Button(self, text="Cancel Login", command=quit)
        quit_button.grid(row=0, column=1)
        login_button = Button(self, text="Login", command=self.login_button_command)
        login_button.grid(row=4, column=1)
        help_button = Button(self, text="Help", command=self.help_text)
        help_button.grid(row=4, column=0)

    def help_text(self):
        label_help1 = Label(self, text="Sign in below using the white boxes. ")
        label_help1.grid(row=1, column=0)
        label_help2 = Label(self, text="Make sure to click Login!")
        label_help2.grid(row=1, column=1)

    def the_entries(self):
        self.userbox = Entry(self)
        self.userbox.grid(row=2, column=1)
        self.passbox = Entry(self, show="*")
        self.passbox.grid(row=3, column=1)

    def login_button_command(self):
        self.data_entry_grab()
        self.confirmation_website()

    def data_entry_grab(self):
        MainWindow.current_username = self.userbox.get()
        MainWindow.current_password = self.passbox.get()
        return MainWindow.current_username, MainWindow.current_password

    def confirmation_website(self):
        root = Tk()
        ConfirmationWindow(root)
        self.master.destroy()


class ConfirmationWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Please Wait")
        self.pack(fill=BOTH, expand=1)
        self.the_labels()
        self.main_check_sequence()

    def the_labels(self):
        check_label = Label(self, text="Double checking the database...")
        check_label.grid(row=0, column=0, columnspan=3)

    def main_check_sequence(self):
        with open("database.json", "r") as f:
            loaded_accounts = json.load(f)
            for stored_user_name, stored_items in loaded_accounts.items():
                if stored_user_name == MainWindow.current_username and stored_items["password"] == MainWindow.current_password:
                    val = True
                    ConfirmationWindow.balance_val = float(stored_items["balance"])
                    self.open_user_page()
                    return ConfirmationWindow.balance_val, val
                elif stored_user_name == MainWindow.current_username:
                    oops_label = Label(self, text="\n Oops! Either you entered the wrong password or there is another"
                                                  " account with the username you are trying to make. Please try again.")
                    oops_label.grid(row=1, column=0, columnspan=3)
                    oops_button = Button(self, text="OK", command=self.main_window_reopen)
                    oops_button.grid(row=2, column=0, columnspan=3)
                    val = True
                    break
                else:
                    val = False
            if val is False:
                new_account_label = Label(self, text="\n We do not have an account with that username. "
                                                     "Would you like to create a new account or attempt to login again?")
                new_account_label.grid(row=1, column=0, columnspan=3)
                new_account_button = Button(self, text="Yes, Create a New Account", command=self.new_account_creation)
                new_account_button.grid(row=2, column=0)
                relog_button = Button(self, text="No, Go Back to Login", command=self.main_window_reopen)
                relog_button.grid(row=2, column=2)

    def open_user_page(self):
        root = Tk()
        UserPage(root)
        self.master.destroy()

    def main_window_reopen(self):
        root = Tk()
        MainWindow(root)
        self.master.destroy()

    def new_account_creation(self):
        with open("database.json") as f:
            loaded_accounts = json.load(f)
        var = {MainWindow.current_username: {"password": MainWindow.current_password, "balance": 0.00, }}
        ConfirmationWindow.balance_val = float(0.00)
        loaded_accounts.update(var)
        with open("database.json", "w") as f:
            json.dump(loaded_accounts, f, indent=4)
        self.open_user_page()
        return ConfirmationWindow.balance_val


class UserPage(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title(MainWindow.current_username + "'s Bank Account")
        self.pack(fill=BOTH, expand=1)
        self.the_labels()
        self.the_buttons()

    def the_labels(self):
        welcoming_label = Label(self, text="Welcome " + MainWindow.current_username + " to your bank account page!")
        welcoming_label.grid(row=0, column=0, columnspan=2)
        balance_label = Label(self, text="Balance:")
        balance_label.grid(row=1, column=0)
        fake_balance_button = Button(self, text="$" + str(ConfirmationWindow.balance_val))
        fake_balance_button.grid(row=1, column=1)

    def the_buttons(self):
        withdraw_button = Button(self, text="Withdraw Funds", command=self.withdraw_page_open)
        withdraw_button.grid(row=2, column=0)
        deposit_button = Button(self, text="Deposit Funds", command=self.deposit_page_open)
        deposit_button.grid(row=2, column=1)
        logout_button = Button(self, text="Logout", command=self.logout_button_command)
        logout_button.grid(row=0, column=2)
        settings_button = Button(self, text="Settings", command=self.settings_page_open)
        settings_button.grid(row=1, column=2)

    def withdraw_page_open(self):
        root = Tk()
        WithdrawPage(root)
        self.master.destroy()

    def deposit_page_open(self):
        root = Tk()
        DepositPage(root)
        self.master.destroy()

    def logout_button_command(self):
        root = Tk()
        MainWindow(root)
        self.master.destroy()

    def settings_page_open(self):
        root = Tk()
        SettingsPage(root)
        self.master.destroy()


class WithdrawPage(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Withdraw Funds Here")
        self.pack(fill=BOTH, expand=1)
        self.the_labels()
        self.the_buttons()
        self.the_entries()

    def the_labels(self):
        withdraw_label = Label(self, text="Enter the amount of funds you want to withdraw here:")
        withdraw_label.grid(row=0, column=0, columnspan=3)

    def the_buttons(self):
        submit_button = Button(self, text="OK", command=self.submit_command)
        submit_button.grid(row=1, column=1)
        cancel_button = Button(self, text="Cancel", command=self.gobackhome)
        cancel_button.grid(row=1, column=2)

    def the_entries(self):
        self.withdraw_entry = Entry(self)
        self.withdraw_entry.grid(row=1, column=0)

    def gobackhome(self):
        root = Tk()
        UserPage(root)
        self.master.destroy()

    def submit_command(self):
        try:
            withdraw_value = float(self.withdraw_entry.get())
        except ValueError:
            ur_wrong_label = Label(self, text="Please enter an actual number that makes sense!")
            ur_wrong_label.grid(row=2, column=0, columnspan=3)
        else:
            if withdraw_value < 0:
                ur_wrong_label = Label(self, text="Please enter an actual number that makes sense!")
                ur_wrong_label.grid(row=2, column=0, columnspan=3)
            else:
                if ConfirmationWindow.balance_val - withdraw_value < 0:
                    still_wrong_label = Label(self, text="Buddy you don't have enough cash to withdraw that amount!")
                    still_wrong_label.grid(row=3, column=0, columnspan=3)
                elif withdraw_value - ConfirmationWindow.balance_val <= 0:
                    with open("database.json") as f:
                        loaded_accounts = json.load(f)
                        for stored_user_name, stored_items in loaded_accounts.items():
                            if stored_user_name == MainWindow.current_username and stored_items["password"] == MainWindow.current_password:
                                stored_items["balance"] = float(ConfirmationWindow.balance_val) - float(withdraw_value)
                    with open("database.json", "w") as f:
                        json.dump(loaded_accounts, f, indent=4)
                    ConfirmationWindow.balance_val = float(ConfirmationWindow.balance_val) - float(withdraw_value)
                    self.gobackhome()
                else:
                    print("Call for assistance because you screwed up.")


class DepositPage(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Deposit Funds Here")
        self.pack(fill=BOTH, expand=1)
        self.the_labels()
        self.the_buttons()
        self.the_entries()

    def the_labels(self):
        deposit_label = Label(self, text="Enter the amount of funds you want to deposit here:")
        deposit_label.grid(row=0, column=0, columnspan=3)

    def the_buttons(self):
        submit_button = Button(self, text="OK", command=self.submit_command)
        submit_button.grid(row=1, column=1)
        cancel_button = Button(self, text="Cancel", command=self.gobackhome)
        cancel_button.grid(row=1, column=2)

    def the_entries(self):
        self.deposit_entry = Entry(self)
        self.deposit_entry.grid(row=1, column=0)

    def gobackhome(self):
        root = Tk()
        UserPage(root)
        self.master.destroy()

    def submit_command(self):
        try:
            deposit_value = float(self.deposit_entry.get())
        except ValueError:
            ur_wrong_label = Label(self, text="Please enter an actual number that makes sense!")
            ur_wrong_label.grid(row=2, column=0, columnspan=3)
        else:
            if deposit_value < 0:
                ur_wrong_label = Label(self, text="Please enter an actual number that makes sense!")
                ur_wrong_label.grid(row=2, column=0, columnspan=3)
            else:
                with open("database.json") as f:
                    loaded_accounts = json.load(f)
                    for stored_user_name, stored_items in loaded_accounts.items():
                        if stored_user_name == MainWindow.current_username and stored_items["password"] == MainWindow.current_password:
                            stored_items["balance"] = float(ConfirmationWindow.balance_val) + float(deposit_value)
                with open("database.json", "w") as f:
                    json.dump(loaded_accounts, f, indent=4)
                ConfirmationWindow.balance_val = float(ConfirmationWindow.balance_val) + float(deposit_value)
                self.gobackhome()


class SettingsPage(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Settings")
        self.pack(fill=BOTH, expand=1)
        self.the_buttons()
        self.the_labels()

    def the_labels(self):
        welcome_label = Label(self, text="Welcome to the settings page. Don't forget to save your work!")
        welcome_label.grid(row=0, column=0)

    def the_buttons(self):
        cancel_button = Button(self, text="Cancel", command=self.gobackhome)
        cancel_button.grid(row=0, column=1)
        passchange_button = Button(self, text="Change Password", command=self.changepasswindow)
        passchange_button.grid(row=1, column=0)

    def gobackhome(self):
        root = Tk()
        UserPage(root)
        self.master.destroy()

    def changepasswindow(self):
        root = Tk()
        PassWindow(root)
        self.master.destroy()


class PassWindow(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Change Password")
        self.pack(fill=BOTH, expand=1)
        self.the_labels()
        self.the_buttons()
        self.the_entries()

    def the_buttons(self):
        cancel_button = Button(self, text="Cancel", command=self.gobacksettings)
        cancel_button.grid(row=0, column=1)
        ok_button = Button(self, text="OK", command=self.pressed_ok)
        ok_button.grid(row=0, column=0)

    def the_labels(self):
        old_pass_label = Label(self, text="Old Password: ")
        old_pass_label.grid(row=1, column=0)
        new_pass_label = Label(self, text="New Password: ")
        new_pass_label.grid(row=2, column=0)
        confirm_pass_label = Label(self, text="Confirm Password:")
        confirm_pass_label.grid(row=3, column=0)

    def the_entries(self):
        self.old_entry = Entry(self)
        self.old_entry.grid(row=1, column=1)
        self.new_entry = Entry(self)
        self.new_entry.grid(row=2, column=1)
        self.confirm_entry = Entry(self)
        self.confirm_entry.grid(row=3, column=1)

    def pressed_ok(self):
        old_pass = self.old_entry.get()
        new_pass = self.new_entry.get()
        confirm_pass = self.confirm_entry.get()
        if old_pass == MainWindow.current_password:
            if new_pass == confirm_pass:
                with open("database.json") as f:
                    loaded_accounts = json.load(f)
                    for stored_user_name, stored_items in loaded_accounts.items():
                        if stored_user_name == MainWindow.current_username and stored_items["password"] == MainWindow.current_password:
                            stored_items["password"] = new_pass
                with open("database.json", "w") as f:
                    json.dump(loaded_accounts, f, indent=4)
                self.new_stuff()

            else:
                wrong_label_2 = Label(self, text="Please make sure your new \n password is properly confirmed!")
                wrong_label_2.grid(row=2, column=3, rowspan=2)
        else:
            wrong_label_1 = Label(self, text="Please make sure your \n old password is correct!")
            wrong_label_1.grid(row=0, column=3, rowspan="2")

    def gobacksettings(self):
        root = Tk()
        SettingsPage(root)
        self.master.destroy()

    def new_stuff(self):
        exit_label = Label(self, text="Your new password has been set, "
                                      "\n please press exit to save your settings!")
        exit_label.grid(row=4, column=0)
        exit_button = Button(self, text="Exit", command=self.gobacksettings)
        exit_button.grid(row=5, column=0)

root = Tk()
window_1 = MainWindow(root)
root.mainloop()

