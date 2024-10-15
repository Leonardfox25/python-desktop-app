#!/usr/bin/python3
import bcrypt 
from tkinter import *
from database.postgres_db import connect
from tkinter import messagebox as msg
import random

# Numeric validation function (placeholder)
def validate_numeric_input(char):
    return char.isdigit() or char == ""

def on_closing():
    if msg.askokcancel("Quit", "Do you want to quit?"):
        main_screen.destroy()

def generate_account_number():
    while True:
        start = random.choice[('22', '21')]
        remaining_digit = random.randit(10000000, 9999999)
        random_num = f'{start}{remaining_digit}'
        conn = connect()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT COUNT(*) FROM user_acct WHERE account_Number
            """, (random_num,)
        )
        count = cur.fetchone()[0]
        conn.close()
        cur.close()
        if count == 0:
            return random_num

def signup():
    global register_screen
    global username
    global password
    global email
    global phone_no
    global address
    global username_entry
    global password_entry
    global email_entry
    global phone_no_entry
    global address_entry

    register_screen = Toplevel(main_screen)
    register_screen.geometry("600x500")
    register_screen.title("Create an account")

    username = StringVar()
    password = StringVar()
    email = StringVar()
    phone_no = StringVar()
    address = StringVar()

    # Command for validating numeric input
    validate_cmd = register_screen.register(validate_numeric_input)

    Label(register_screen, text="").pack()
    Label(register_screen, text="Please enter the following details", bg="red", font=("Calibri", 13)).pack()

    # Username
    Label(register_screen, text="Username * ").pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()

    # Password
    Label(register_screen, text="Password * ").pack()
    password_entry = Entry(register_screen, textvariable=password, show="*")
    password_entry.pack()

    # Email
    Label(register_screen, text="Email * ").pack()
    email_entry = Entry(register_screen, textvariable=email)
    email_entry.pack()

    # Phone number with validation for numeric input
    Label(register_screen, text="Phone Number * ").pack()
    phone_no_entry = Entry(register_screen, textvariable=phone_no, validate="key", validatecommand=(validate_cmd, "%S"))
    phone_no_entry.pack()

    # Address
    Label(register_screen, text="Address * ").pack()
    address_entry = Entry(register_screen, textvariable=address)
    address_entry.pack()

    # Space and Register button
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", bg="green", font=("Calibri", 13), width=13, height=1, command=register_user).pack()

def register_user():
    # Declare global variables to use them inside the function
    global username, password, email, phone_no, address
    global username_entry, password_entry, email_entry, phone_no_entry, address_entry
    
    username_info = username.get()
    password_info = password.get()
    email_info = email.get()
    phone_no_info = phone_no.get()
    address_info = address.get()

    # Hashing the password
    hashed_password = bcrypt.hashpw(password_info.encode('utf-8'), bcrypt.gensalt())
    conn = None
    cur = None
    try:
        # Connecting to the database
        conn = connect()
        cur = conn.cursor()
        if conn is None:
            msg.showerror("Error", "Database connection failed.")
            return
        # Inserting user data into the database
        cur.execute(
            """
            INSERT INTO user_acct(username, password, email, phone_no, address)
            VALUES(%s, %s, %s, %s, %s)
            """, (username_info, hashed_password.decode('utf-8'), email_info, phone_no_info, address_info)
        )

        # Committing the transaction
        conn.commit()
    except Exception as e:
        msg.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

        # Clearing the form after successful registration
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        email_entry.delete(0, END)
        phone_no_entry.delete(0, END)
        address_entry.delete(0, END)

        # Displaying success message
        Label(register_screen, text="Registration successful", fg="green", font=("Calibri", 13)).pack()

def login():
    # from main import main_screen
    global login_screen
    global email_entry
    global password_entry
    global email
    global password

    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("600x500")

    email = StringVar()
    password = StringVar()

    # Instruction Label
    Label(login_screen, text="Please enter the following details", bg="red", font=("Calibri", 13)).pack()

    # Email input
    Label(login_screen, text="Email * ").pack()
    email_entry = Entry(login_screen, textvariable=email)
    email_entry.pack()

    # Password input
    Label(login_screen, text="Password * ").pack()
    password_entry = Entry(login_screen, textvariable=password, show="*")
    password_entry.pack()

    # Login Button
    Button(login_screen, text="Login", bg="green", command=login_verify).pack()

def login_verify():
    email_info = email_entry.get()
    password_info = password_entry.get()

    # Connecting to the database
    conn = connect()
    cur = conn.cursor()
    
    # Fetch hashed password from database
    cur.execute(
        """
        SELECT password FROM user_acct WHERE email = %s
        """, (email_info,)
    )
    result = cur.fetchone()

    conn.close()
    
    if result:
        stored_hashed_password = result[0].encode('utf-8')
        # Check if entered password matches the hashed password
        if bcrypt.checkpw(password_info.encode('utf-8'), stored_hashed_password):
            login_success()
        else:
            password_invalid()
    else:
        user_not_found()

def login_success():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    
    Label(login_success_screen, text="Login successfully", fg="green", font=("Calibri", 13)).pack()
    Button(login_success_screen, text="OK", command=login_success_screen.destroy).pack()

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Failed")
    user_not_found_screen.geometry("150x100")
    
    Label(user_not_found_screen, text="User not found", fg="red", font=("Calibri", 13)).pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found).pack()

def delete_user_not_found():
    user_not_found_screen.destroy()

def password_invalid():
    global password_invalid_screen
    password_invalid_screen = Toplevel(login_screen)
    password_invalid_screen.title("Invalid Password")
    password_invalid_screen.geometry("150x100")
    
    Label(password_invalid_screen, text="Password is invalid", fg="red", font=("Calibri", 13)).pack()
    Button(password_invalid_screen, text="OK", command=delete_password_invalid).pack()

def delete_password_invalid():
    password_invalid_screen.destroy()

def deposit():
    global name_entry
    global account_number_entry
    global amount_entry
    global name
    global account_number
    global amount

    name = StringVar()
    account_number = StringVar()
    amount = StringVar()

    deposit_screen = Toplevel(menu_screen)
    deposit_screen.title("Deposit Screen")
    deposit_screen.geometry("600x500")

    Label(deposit_screen, text="").pack()
    Label(deposit_screen, text="Please fill the details", bg="red", font=("Calibri", 13)).pack()

    # Name input
    Label(deposit_screen, text="Name", font=("Calibri", 13)).pack()
    name_entry = Entry(deposit_screen, textvariable=name)
    name_entry.pack()

    # Account Number input
    Label(deposit_screen, text="Account Number", font=("Calibri", 13)).pack()
    account_number_entry = Entry(deposit_screen, textvariable=account_number)
    account_number_entry.pack()

    # Amount input
    Label(deposit_screen, text="Amount", font=('Calibri', 13)).pack()
    amount_entry = Entry(deposit_screen, textvariable=amount)
    amount_entry.pack()

    # Deposit button
    Button(deposit_screen, text="Deposit", bg="green", font=("Calibri", 13), width=13, height=1, command=deposit_verify).pack()

def deposit_verify():
    conn = connect()
    cur = conn.cursor()

    name_info = name.get()
    account_number_info = account_number.get()
    amount_info = amount.get()

    # Validation for amount being a numeric value
    if not amount_info.isdigit():
        msg.showerror("Error", "Amount must be a numeric value")
        return
    
    email_info = email.get()

    # Check if user exists
    cur.execute(
        """
        SELECT user_id FROM user_acct WHERE email = %s
        """, (email_info,)
    )
    user = cur.fetchone()
    if user is None:
        msg.showerror('Error', 'User not found')
        conn.close()
        return

    user_id = user[0]

    # Insert transaction details into the transactions table
    cur.execute(
        """
        INSERT INTO transactions(name, account_number, amount, user_id)
        VALUES(%s, %s, %s, %s)
        """, (name_info, account_number_info, amount_info, user_id)
    )
    
    # Update the user's account balance
    cur.execute(
        """
        UPDATE user_acct SET balance = balance + %s WHERE email = %s
        """, (amount_info, email_info)
    )
    
    conn.commit()
    cur.close()
    conn.close()

    msg.showinfo('Saved', f'Amount of ${amount_info} deposited successfully')

def withdraw():
    global withdraw_screen
    global withdraw_name_entry
    global withdraw_account_no_entry
    global withdraw_amount_entry
    global withdraw_name
    global withdraw_account_no
    global withdraw_amount

    withdraw_screen = Toplevel(menu_screen)
    withdraw_screen.title("Withdraw Screen")
    withdraw_screen.geometry("600x500")

    withdraw_name = StringVar()
    withdraw_account_no = StringVar()
    withdraw_amount = StringVar()

    Label(withdraw_screen, text='').pack()
    Label(withdraw_screen, text="Please fill the details", bg="red", font=("Calibri", 13)).pack()
    Label(withdraw_screen, text="Name", font=("Calibri", 13)).pack()
    withdraw_name_entry = Entry(withdraw_screen, textvariable=withdraw_name)
    withdraw_name_entry.pack()
    
    Label(withdraw_screen, text="Account Number", font=("Calibri", 13)).pack()
    withdraw_account_no_entry = Entry(withdraw_screen, textvariable=withdraw_account_no)
    withdraw_account_no_entry.pack()
    
    Label(withdraw_screen, text="Amount", font=('Calibri', 13)).pack()
    withdraw_amount_entry = Entry(withdraw_screen, textvariable=withdraw_amount)
    withdraw_amount_entry.pack()

    Button(withdraw_screen, text="Withdraw", bg="green", font=("Calibri", 13), width=13, height=1, command=withdraw_verify).pack()

def withdraw_verify():
    conn = connect()
    cur = conn.cursor()

    withdraw_name_info = withdraw_name.get()
    withdraw_account_no_info = withdraw_account_no.get()
    withdraw_amount_info = withdraw_amount.get()
    withdraw_email_info = email_entry.get()

    try:
        cur.execute(
            """
            SELECT id, balance FROM user_acct WHERE email = %s
            """, (withdraw_email_info,)
        )
        user = cur.fetchone()
        if user is None:
            msg.showerror('Error', 'User not found')
            return
        
        user_id = user[0]
        current_balance = user[1]

        if float(withdraw_amount_info) > current_balance:
            msg.showerror('Error', 'Insufficient Funds')
            return

        new_balance = current_balance - float(withdraw_amount_info)

        cur.execute(
            """
            UPDATE user_acct SET balance = %s WHERE id = %s
            """, (new_balance, user_id)
        )

        cur.execute(
            """
            INSERT INTO transactions(name, account_number, amount, transaction_type, user_id)
            VALUES(%s, %s, %s, %s, %s)
            """, (
                withdraw_name_info,
                withdraw_account_no_info,
                withdraw_amount_info,
                "withdraw",
                user_id
            )
        )
        
        conn.commit()
        msg.showinfo('Saved', f'Amount of ${withdraw_amount_info} withdrawn successfully')
        
    except Exception as e:
        msg.showerror("Error", f"An error occurred: {str(e)}")
    finally:
        cur.close()
        conn.close()

def transfer_fund():
    global transfer_screen
    global sender_account_entry
    global recipient_account_entry
    global transfer_amount_entry
    global sender_account
    global recipient_account
    global transfer_amount

    sender_account = StringVar()
    recipient_account = StringVar()
    transfer_amount = StringVar()

    transfer_screen = Toplevel(menu_screen)
    transfer_screen.title("Transfer Fund")
    transfer_screen.geometry("600x500")

    Label(transfer_screen, text ='').pack()
    Label(transfer_screen, text="sender account").pack()
    sender_account_entry = Entry(transfer_screen, textvariable=sender_account)
    recipient_account_entry = Entry(transfer_screen, textvariable=recipient_account).pack()
    Label = Label(transfer_screen, text= "Account number", font =("Calibri", 13)).pack()
    Label = Label(transfer_screen, text="Amount", font= ('Calibri', 13)).pack()
    transfer_amount_entry =  Entry(transfer_screen, textvariable=transfer_amount).pack()
    Button(transfer_screen, text= "Transfer", bg = "green", font=("Calibri", 13), width = 13, height=1, command =transfer_verify).pack()

def transfer_verify():
    conn = connect()
    cur = conn.cursor()

    sender_acct_Info = sender_account.get()
    recipient_acct_info = recipient_account.get()
    transfer_amount_info = transfer_amount.get()

    cur.execute(
        """
        SELECT u.id, u.balance
        FROM user_acct u
        JOIN transactions t ON u.id = t.user_id
        WHERE t.account_numer = %s
        """, (sender_acct_Info,)
    )
    sender = cur.fetchone()
    if sender is None:
        msg.showerror('Error', 'Sender account not found')
    sender_id = sender[0]
    sender_balance = float(sender[1])

    if float(transfer_amount_info) > sender_balance:
        msg.showerror('Error', f'Insufficient Fund, Your Balance Is ${sender_balance}.00')
        return
    cur.execute(
        """
        SELECT u.id, u.balance
        FROM user_acct u
        JOIN transactions t ON u.id = t.user_id
        WHERE t.account_numer = %s
        """, (recipient_acct_info,)
    )
    recipient = cur.fetchone()
    if recipient is None:
        msg.showerror('Error', 'Recipient not found')

    recipient_id = recipient[0]
    recipient_balance = float(recipient[1])
    new_sender_balance = sender_balance - float(transfer_amount_info)
    new_recipient_balance = recipient_balance + float(transfer_amount_info)

    cur.execute(
        """
        UPDATE user_acct SET balance = %s
        """, (new_sender_balance, sender_id)
    )
    cur.execute(
        """
        UPDATE user_acct SET balance = %s WHERE id = %s
        """, (new_recipient_balance, recipient_id)
    )
    cur.execute(
        """
        INSERT INTO transactions(name, account number, amount, transaction_id, user_id)
        """, (
            'sender',
            sender_acct_Info,
            transfer_amount_info,
            sender_id
        )
    )
    cur.execute(
        """
        INSERT INTO transactions(name, account_number, amount, transaction_id,user_id)
        VALUES (%s, %s, %s, 'traansfer_received', %s)
        """,(
            'recipient',
            recipient_acct_info,
            transfer_amount_info,
            recipient_id
        )
    )
    conn.commit()
    conn.close()
    cur.close()
    msg.showinfo('Sved', f'Amount of ${transfer_amount_info} transferred successfully to {recipient_acct_info}')

def check_balance():
    global balance_screen
    global acct_entry 
    global acct_number
    
    balance_screen = Toplevel(menu_screen)
    balance_screen.title("Check Your Balance")
    balance_screen.geometry("600x500")

    acct_number = StringVar()
    Label(balance_screen, text= 'Enter Your Account Number').pack()
    acct_entry = Entry(balance_screen, textvariable= acct_number).pack()
    Button(balance_screen, text = 'Check Balance', bg = "green", font = ("Calibri", 13), width = 13, height =1, command = check_balance_verify).pack()

def check_balance_verify():
    conn = connect()
    cur = conn.cursor()

    acct_entry_info = acct_number.get()
    check_balance_email_verify = email_entry.get()

    cur.execute(
        """
        SELECT u.balance 
        FROM user_acct u
        WHERE email = %s
        """, (check_balance_email_verify,)
    )
    current_user = cur.fetchone()
    if current_user is None:
        msg.showerror('Error', 'Account number not found')
        return
    current_user_id = current_user[0]
    cur.execute(
        """
        SELECT u.id, u.balance
        FROM user_acct u
        JOIN transaction t ON u.id = t.user_id
        WHERE t.account_number = %s
        """, (acct_entry_info,)
    )
    acct = cur.fetchone()
    if acct is None:
        msg.showerror('Error' 'Account number not found')
    else:
        user_id = acct[0]
        balance = acct[1]

    if user_id != current_user_id:
        msg.showerror('Error', 'You are not authorised to view this account')
    else:
        msg.showerror('Success', f"your balance is {balance}")

def menu():
    global menu_screen
    menu_screen = Toplevel(main_screen)
    menu_screen.title("Menu")
    menu_screen.geometry("600x400")  # Adjusted to a more manageable size

    Button(menu_screen, text='Deposit', bg='violet', fg='black', width='30', height="", font=("Arial Bold", 10), command=deposit).pack()
    Button(menu_screen, text="Withdraw", bg='red', fg='black', width="30", height="2", font=("Arial Bold", 10), command=withdraw).pack()
    Button(menu_screen, text="Balance", bg='red', fg='black', width="30", height="2", font=("Arial Bold", 10)).pack()
    Button(menu_screen, text="Transfer", bg='red', fg='black', width="30", height="2", font=("Arial Bold", 10)).pack()
    Label(menu_screen, text='').pack(side=LEFT)

def main_action_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("600x400")  # Adjusted to fit most screen sizes
    main_screen.title("User Account Login/Register")
    main_screen.protocol("WM_DELETE_WINDOW", on_closing)

    Label(text="Select your choice", bg="green", width="300", height="2", font=("Calibri", 13)).pack()

    Button(text="Register", bg="red", width="30", height="2", font=("Arial Bold", 10), command=signup).pack()
    Button(text="Login", bg="green", width="30", height="2", font=("Arial Bold", 10), command=login).pack()

    main_screen.mainloop()

main_action_screen()
