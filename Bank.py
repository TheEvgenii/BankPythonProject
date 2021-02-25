#
# EvgenGoBank.py
# Evgenii_Litvinov_BankProject
# Purpouse for this project: Learn how to use GUI "tkinter" library.
# Code was written in Python 3.0 language.
#


#imports
from tkinter import *
import os
from PIL import ImageTk, Image


#Main Screen
window = Tk()
window.title("Evgengo bank")

#Functions
def register():
    #Vars
    #available for antire program
    global temp_name
    global temp_age
    global temp_gender
    global temp_password
    global notif
    temp_name = StringVar()
    temp_age = StringVar()
    temp_gender = StringVar()
    temp_password = StringVar()
    #Register Screen
    register_screen = Toplevel(window)
    register_screen.title("Register")

    #Labels
    Label(register_screen, text="Please enter your details below to register your account ", font=("Calibri",14)).grid(row=0,sticky=N,pady=10)
    Label(register_screen, text="Name ", font=("Calibri",12)).grid(row=1,sticky=W)
    Label(register_screen, text="Age ", font=("Calibri",12)).grid(row=2,sticky=W)
    Label(register_screen, text="Gender ", font=("Calibri",12)).grid(row=3,sticky=W)
    Label(register_screen, text="Password ", font=("Calibri",12)).grid(row=4,sticky=W)
    notif = Label(register_screen, font=("Calibri",12))
    notif.grid(row=6,sticky=W,pady=10)

    #Entries
    Entry(register_screen,textvariable = temp_name).grid(row=1,column=0)
    Entry(register_screen,textvariable = temp_age).grid(row=2,column=0)
    Entry(register_screen,textvariable = temp_gender).grid(row=3,column=0)
    Entry(register_screen,textvariable = temp_password,show="*").grid(row=4,column=0)

    #Buttons
    Button(register_screen,text="Register",  command = finish_reg, font=("Calibri",12),fg="#FFA14D").grid(row=5,sticky=N,pady=10)

def finish_reg():
    name = temp_name.get()
    age = temp_age.get()
    gender = temp_gender.get()
    password = temp_password.get()
    all_accounts = os.listdir()

    if name =="" or age == "" or gender == "" or password =="":
        notif.config(fg="red",text = "All fields requried *")
        return
    for name_check in all_accounts:
        if name == name_check:
            notif.config(fg="red",text="Account already exists")
            return
        else:
            new_file = open(name,"w")
            new_file.write(name+'\n')
            new_file.write(password+'\n')
            new_file.write(age+'\n')
            new_file.write(gender+'\n')
            new_file.write('0')
            new_file.close()
            notif.config(fg="green", text = "Account has been created")           
      
def login_session():
    global login_name
    all_accounts = os.listdir() #reading all files
    login_name = temp_login_name.get()
    login_password = temp_login_password.get()

    for name in all_accounts:
        if name == login_name:
            file = open(name,"r")
            file_data = file.read()
            file_data = file_data.split('\n') #each value in a difernt line in a list
            password = file_data[1]
            #Account Dashboard
            if login_password == password:
                login_screen.destroy()
                account_dashboard = Toplevel(window)
                account_dashboard.title("Dashboard")
                
                #Labels
                Label(account_dashboard,text = "Account in EvgenGObank",font=("Calibri",14)).grid(row=0,sticky=N,pady=10)
                Label(account_dashboard,text = "Welcome "+name,font=("Calibri",14)).grid(row=1,sticky=N,pady=5)
                
                #Buttons
                Button(account_dashboard,text="Personal Details",font=("Calibri",13),fg="#FFA14D",width=30, command=personal_details).grid(row=2,sticky=N,padx=10)
                Button(account_dashboard,text="Deposit",font=("Calibri",12),fg="#FFA14D",width=30,command=deposit).grid(row=3,sticky=N,padx=10)
                Button(account_dashboard,text="Withdraw",font=("Calibri",12),fg="#FFA14D",width=30,command=withdraw).grid(row=4,sticky=N,padx=10)
                Label(account_dashboard).grid(row=5,sticky=N,pady=10)
                return
            else:
                login_notif.config(fg="red", text="Password incorrect!")
                return
    login_notif.config(fg="red", text="Account does not exist!")

def deposit():  
    #vars
    global amount
    global deposit_notif
    global current_balance_label
    amount = StringVar()
    file = open(login_name,"r")
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[4]
    
    #Deposit Screen
    deposit_screen = Toplevel(window)
    deposit_screen.title("Deposit")
    
    #Label
    Label(deposit_screen, text="Deposit",font=("Calibri",12)).grid(row=0,sticky=N,pady=10)
    current_balance_label = Label(deposit_screen, text="Current Balance :  $"+details_balance,font=("Calibri",12))
    current_balance_label.grid(row= 1,sticky=W)
    Label(deposit_screen, text="Amount  :",font=("Calibri",12)).grid(row=2,sticky=W)
    deposit_notif = Label(deposit_screen, font = ("Calibri",12))
    deposit_notif.grid(row=4,sticky=N,pady=5)

    #Entry
    Entry(deposit_screen, textvariable = amount).grid(row=2,column=1)
    #Button
    Button(deposit_screen,text="Finish",font=("Calibri",12),fg="#FFA14D",command = finish_deposit).grid(row=3,sticky=W,pady=5)
    Button(deposit_screen,text="Go Back",font=("Calibri",12),fg="#FFA14D",command = login_session).grid(row=4,sticky=W,pady=5)
    
    
def finish_deposit():    
    if amount.get() == "":
        deposit_notif.config(text="Amount is required!",fg="red")
        return
    if float(amount.get())<=0:
        deposit_notif.config(text="Nagtive value is not accepted",fg="red")
        return

    file = open(login_name,'r+')
    file_data = file.read()
    details = file_data.split('\n')
    current_balance = details[4]
    updated_balance = current_balance
    updated_balance = float(updated_balance) + float(amount.get())
    file_data = file_data.replace(current_balance, str(updated_balance))
    file.seek(0)
    file.truncate(0)
    file.write(file_data)
    file.close()
    current_balance_label.config(text="Current Balance : $"+str(updated_balance),fg="green")
    deposit_notif.config(text="Balance Updated",fg="green")
    
def withdraw():    
    #vars
    global withdraw_amount
    global withdraw_notif
    global current_balance_label
    withdraw_amount = StringVar()
    file = open(login_name,"r")
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[4]
    
    #Deposit Screen
    withdraw_screen = Toplevel(window)
    withdraw_screen.title("Deposit")
    
    #Label
    Label(withdraw_screen, text="Deposit",font=("Calibri",12)).grid(row=0,sticky=N,pady=10)
    current_balance_label = Label(withdraw_screen, text="Current Balance :  $"+details_balance,font=("Calibri",12))
    current_balance_label.grid(row= 1,sticky=W)
    Label(withdraw_screen, text="Amount  :",font=("Calibri",12)).grid(row=2,sticky=W)
    withdraw_notif = Label(withdraw_screen, font = ("Calibri",12))
    withdraw_notif.grid(row=4,sticky=N,pady=5)

    #Entry
    Entry(withdraw_screen, textvariable = withdraw_amount).grid(row=2,column=1)
    
    #Button
    Button(withdraw_screen,text="Finish",font=("Calibri",12),fg="#FFA14D",command = finish_withdraw).grid(row=3,sticky=W,pady=5)
    Button(withdraw_screen,text="Go Back",font=("Calibri",12),fg="#FFA14D",command = login_session).grid(row=4,sticky=W,pady=5)
    
def finish_withdraw():    
    if withdraw_amount.get() == "":
        withdraw_notif.config(text="Amount is required!",fg="red")
        return
    if float(amount.get())<=0:
        withdraw_notif.config(text="Nagtive value is not accepted",fg="red")
        return

    file = open(login_name,'r+')
    file_data = file.read()
    details = file_data.split('\n')
    current_balance = details[4]
    
    if float(withdraw_amount.get()) > float(current_balance):
        withdraw_notif.config(text = "Error value!", fg= "red")
        return
    
    updated_balance = current_balance
    updated_balance = float(updated_balance) - float(withdraw_amount.get())
    file_data = file_data.replace(current_balance, str(updated_balance))
    file.seek(0)
    file.truncate(0)
    file.write(file_data)
    file.close()
    current_balance_label.config(text="Current Balance : $"+str(updated_balance),fg="green")
    withdraw_notif.config(text="Balance Updated",fg="green")

                               
def change_personal_info():    
    #vars   
    global name_change
    global name_notif
    global current_name_label
    global age_change
    global age_notif
    global current_age_label
    global gender_change
    global gender_notif
    global current_gender_label
    
    name_change = StringVar()
    age_change = StringVar()
    gender_change = StringVar()
    file = open(login_name,"r")
    file_data = file.read()
    user_details = file_data.split('\n')
    details_name = user_details[0]
    details_age = user_details[2]
    details_gender = user_details[3]
    details_balance = user_details[4]
    
    #Deposit Screen
    change_info_screen = Toplevel(window)
    change_info_screen.title("Change INFO")
    
    #Label
    Label(change_info_screen, text="Change INFO",font=("Calibri",12)).grid(row=0,sticky=N,pady=10)
    current_name_label = Label(change_info_screen, text="Current INFO :  ",font=("Calibri",12))
    current_name_label.grid(row= 1,sticky=W)
    Label(change_info_screen, text="New name  :",font=("Calibri",12)).grid(row=2,sticky=W)
    name_notif = Label(change_info_screen, font = ("Calibri",12))
    name_notif.grid(row=7,sticky=N,pady=5)
    Label(change_info_screen, text="New age  :",font=("Calibri",12)).grid(row=3,sticky=W)
    Label(change_info_screen, text="New gender  :",font=("Calibri",12)).grid(row=4,sticky=W)
 
    #Entry
    Entry(change_info_screen, textvariable = name_change).grid(row=2,column=1)
    Entry(change_info_screen, textvariable = age_change).grid(row=3,column=1)
    Entry(change_info_screen, textvariable = gender_change).grid(row=4,column=1)
    #Button
    Button(change_info_screen,text="Change INFO",font=("Calibri",12),fg="#FFA14D",command = finish_change_info).grid(row=10,sticky=N,pady=5)
    Button(change_info_screen,text="Go Back",font=("Calibri",12),fg="#FFA14D",command = login_session).grid(row=6,sticky=11,pady=5)
    
def finish_change_info():   
    if name_change.get() == "":
        name_notif.config(text="Name is required!",fg="red")
        return
    if age_change.get() == "":
        name_notif.config(text="Age is required!",fg="red")
        return
    if gender_change.get() == "":
        name_notif.config(text="Gender is required!",fg="red")
        return
    
    if float(age_change.get())<=0:
        name_notif.config(text="Incorrect age",fg="red")
        return

    file = open(login_name,'r+')
    file_data = file.read()
    details = file_data.split('\n')
    current_name = details[0]
    current_age = details[2]
    current_gender = details[3]

    updated_gender = current_gender
    updated_gender = gender_change.get()
    file_data = file_data.replace(current_gender,(updated_gender))
    file.seek(0)
    file.truncate(0)
    file.write(file_data)
  
    updated_name = current_name
    updated_name = name_change.get()
    file_data = file_data.replace(current_name,(updated_name))
    file.seek(0)
    file.truncate(0)
    file.write(file_data)

    current_name_label.config(text="Current Name : "+str(updated_name),fg="green")
    name_notif.config(text="Name Updated",fg="green")

    updated_age = current_age
    updated_name = age_change.get()
    file_data = file_data.replace(current_age,(updated_age))
    file.seek(0)
    file.truncate(0)
    file.write(file_data)
    file.close()

def personal_details():
    #vars
    file = open(login_name,'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    details_name = user_details[0]
    details_age = user_details[2]
    details_gender = user_details[3]
    details_balance = user_details[4]
    personal_details_screen = Toplevel(window)
    personal_details_screen.title("Personal Details")
    
    #Labels
    Label(personal_details_screen,text = "Personal details:    ",font=("Calibri",12),fg="#FFA14D").grid(row=0,sticky=N,pady=10)
    Label(personal_details_screen,text = "Name  :  "+details_name,font=("Calibri",12)).grid(row=1,sticky=W)
    Label(personal_details_screen,text = "Age   :  "+details_age,font=("Calibri",12)).grid(row=2,sticky=W)
    Label(personal_details_screen,text = "Gender  :  "+details_gender,font=("Calibri",12)).grid(row=3,sticky=W)
    Label(personal_details_screen,text = "Balance :  "+details_balance,font=("Calibri",12)).grid(row=4,sticky=W)

    #Buttons
    Button(personal_details_screen,text="Change INFO",font=("Calibri",12),fg="#FFA14D",command = change_personal_info).grid(row=5,sticky=W,pady=5)
    Button(personal_details_screen,text="Go Back",font=("Calibri",12),fg="#FFA14D",command = login_session).grid(row=6,sticky=W,pady=5)
    
def login():    
    #Vars
    global temp_login_name
    global temp_login_password
    global temp_login_notif
    global temp_login_screen
    global login_screen
    global login_notif
    temp_login_name = StringVar()
    temp_login_password = StringVar()
    
    #Login Screen
    login_screen = Toplevel(window)
    login_screen.title("Login")
    
    #Labels
    Label(login_screen, text="Login to your account",font=("Calibri",12)).grid(row=0,sticky=N,pady=10)
    Label(login_screen, text="Username:",font=("Calibri",12)).grid(row=1,sticky=W)
    Label(login_screen, text="Password:",font=("Calibri",12)).grid(row=2,sticky=W)
    login_notif = Label(login_screen,font=("Calibri",12))
    login_notif.grid(row=4,sticky = N)
    
    #Entry
    Entry(login_screen, textvariable = temp_login_name,fg="blue").grid(row=1,column=1,padx=5)
    Entry(login_screen, textvariable = temp_login_password,show="*").grid(row=2,column=1,padx=5)
    
    #Buttons
    Button(login_screen, text="Login", command=login_session,width=15,font=("Calibri",12),fg="#FFA14D").grid(row=3,sticky=W,pady=5,padx=5)
    

    
  

#image import
img = Image.open("BankLOGO.jpg")
img = img.resize((200,200))
img = ImageTk.PhotoImage(img)

#Labels
Label(window, text = "EvgenGo Bank", font = ("Roman",20),fg="#4ff0ff").grid(row=0,sticky=N,pady=10)
Label(window, text = "Good evening!", font = ("Bold",16),fg="#FFC64D").grid(row=1,sticky=N)
Label(window, image = img).grid(row=2,sticky=N,pady=15)

#Buttons
Button(window, text = "Register", font = ("Calibri", 14),bg="#A8BFFF",fg="#FFA14D",width = 10,command=register).grid(row = 3, sticky=N)
Button(window, text = "Login", font = ("Calibri", 14),fg="#FFA14D",bg="#A8BFFF",width = 10,command=login).grid(row = 4, sticky=N,pady= 20)

#GUI can stay in a loop
window.mainloop() 
