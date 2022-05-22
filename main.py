import requests
import sys
import time
from datetime import datetime
from bs4 import BeautifulSoup

wallets = {}
wallet_backup = {}

exit = False

def main():
    choice = input("What would you like to do? \n(C)reate a Wallet -Create an empty wallet \n(E)dit a Wallet - Add/Remove cryptocurrencies from a wallet \n(D)elete a Wallet - Remove a wallet \n(V)iew all Wallets - View Wallets and their balances in USD courtesy of crypto.com exchange\n(R)estore - Recover a wallet \nE(x)it - Exit and stop program\n")
    
    if choice == 'C' or choice == 'c':
        create()
    elif choice == 'E' or choice == 'e':
        edit()
    elif choice == 'D' or choice == 'd':
        delete() 
    elif choice == 'V' or choice == 'v':
        view()
    elif choice.upper() == 'R':
        restore()
    elif choice.upper() == 'X':
        exit()
    else:
        print("Invalid Selection. Please input: C, E, D, V, or X\n")
        
        
def is_float(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

def getPrices():
    url = 'https://crypto.com/price'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    crypto = soup.findAll('span', {'class' : 'chakra-text css-ft1qn5'})
    price = soup.findAll('div', {'class' : 'css-b1ilzc'})

    getPrices.crypto_prices = {}

    crypto = str(crypto)
    crypto = crypto.lstrip("[").rstrip("]")
    crypto = crypto.split(', ')
    getPrices.crypto_list = []

    price = str(price)
    price = price.lstrip("[").rstrip("]")
    price = price.split(', ')
    getPrices.price_list = []

    for string in crypto:
        string = string.replace('<span class="chakra-text css-ft1qn5">','')
        string = string.replace('</span>', '')
        getPrices.crypto_list.append(string)

    for string in price:
        string = string.replace('<div class="css-b1ilzc">','')
        string = string.replace('</div>','')
        string = string.replace('$', '')
        string = string.replace(',','')
        getPrices.price_list.append(string)

    for x in range(len(getPrices.price_list)):
        getPrices.crypto_prices[getPrices.crypto_list[x]] = getPrices.price_list[x]

def create():
    name = input("Wallet Name: ")
    if name in wallets:
        print("Wallet already exists.\n")
    else:
        wallets[name] = {}
        print("Wallet Created.\n")

def edit():
    if len(wallets) < 1:
        print("No Wallets available to edit.")
    else:
        print("List of Wallets: "+ str(list(wallets.keys())))
        name = input("Name of wallet you would like to edit: ")
        if name not in wallets:
            print("Wallet not found.\n")
        else:
            add_or_remove = input("(A)dd or (R)emove cryptocurrency: ")
            if add_or_remove == 'A' or add_or_remove == 'a':
                getPrices()
                print(getPrices.crypto_list)
                crypto_choice = input("Which crypto would you like to add: ")
                if crypto_choice.upper() not in getPrices.crypto_list:
                    print("Invalid choice.")
                else:
                    print("How much " + crypto_choice.upper() + " would you like to add: ")
                    amount = input("")
                    if is_float(amount):
                        amount = float(amount)
                        if amount > 0:
                            if crypto_choice.upper() in wallets[name]:
                                wallets[name][crypto_choice.upper()] += amount
                            else:
                                wallets[name][crypto_choice.upper()] = amount
                            print("Wallet Updated. " + str(amount) + " " + crypto_choice.upper() + " added to " + name)
                    else:
                        print("Invalid amount.")
            elif add_or_remove == 'R' or add_or_remove == 'r':
                if len(wallets[name]) > 0:
                    print(wallets[name])
                    crypto_choice = input("Which crypto would you like to remove: ")
                    getPrices()
                    if crypto_choice.upper() not in getPrices.crypto_list or crypto_choice.upper() not in wallets[name]:
                        print("Invalid choice.")
                    else:
                        print("How much " + crypto_choice.upper() + " would you like to remove: ")
                        amount = input("")
                        if is_float(amount):
                            amount = float(amount)
                            if amount > wallets[name][crypto_choice.upper()]:
                                print("Invalid amount. You are trying to remove more than what is in the wallet.")
                            else:
                                wallets[name][crypto_choice.upper()] -= amount
                                if wallets[name][crypto_choice.upper()] == 0:
                                    del wallets[name][crypto_choice.upper()]
                                print("Wallet Updated. " + str(amount) + " " + crypto_choice.upper() + " removed from " + name)
                        else:
                            print("Invalid Amount.")
                else:
                    print("Empty wallet, nothing can be removed.")

def delete():
    if len(wallets) < 1:
        print("No Wallets available to delete.")
    else:
        print(list(wallets.keys()))
        name = input("Name of wallet you would like to delete: ")
        if name in wallets:
            comment = input("Comments for deletion: ")
            wallet_backup[name] = (wallets[name],comment)
            del wallets[name]
        else:
            print("Deletion Failed. Wallet does not exist.")

def view():
    if len(wallets) < 1:
        print("No Wallets available to view.")
    else:
        getPrices()
        now = datetime.now()
        date = now.strftime("%m/%d/%y")
        current_time = now.strftime("%H:%M:%S")

        for name in wallets:
            print("Date: ", date)
            balance = 0
            print(name + "\'s Cryptocurrency Portfolio:")
            print(wallets[name])
            for crypto in wallets[name]:
                balance += wallets[name][crypto] * float(getPrices.crypto_prices[crypto])
            print("\nPortfolio Value of " + name + " in USD as of", current_time,"is: $%0.2f\n" %balance)

def restore():
    if len(wallet_backup) < 1:
        print("No wallets available to restore.")
    else:
        print(wallet_backup)
        name = input("Which wallet would you like to restore?: ")
        if name not in wallet_backup:
            print("Inputted wallet not available for recovery")
        else:
            if name in wallets:
                new_name = input("Wallet with same name already exists, please rename this wallet: ")
                if new_name in wallets:
                    print("Wallet Name exists, start over.")
                else:
                    wallets[new_name] = wallet_backup[name][0]
                    del wallet_backup[name]
                    print("Wallet restored as " + new_name)
            else:
                wallets[name] = wallet_backup[name][0]
                del wallet_backup[name]
                print("Wallet restored as " + name)
            
def exit():
    sys.exit("User Has Exited")

getPrices()
    
while True:
    main()


