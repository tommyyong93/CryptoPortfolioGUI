import matplotlib.pyplot as plt
import json
import os
import requests
from tkinter import *
os.system('cls')

# Creating a Tkinter Window
window = Tk()
window.title("Crypto Currency Portfolio")

# Add labels

# Create Header
header_nm = Label(window,text="Name")
header_nm.grid(row = 0, column = 0, sticky = N+S+E+W)

header_rk = Label(window,text="Rank")
header_rk.grid(row = 0, column = 1, sticky = N+S+E+W)

header_price = Label(window,text="Current Price")
header_price.grid(row = 0, column = 2, sticky = N+S+E+W)

header_pricepaid = Label(window,text="Price paid")
header_pricepaid.grid(row = 0, column = 3, sticky = N+S+E+W)

header_profit = Label(window,text="Profit/Loss")
header_profit.grid(row = 0, column = 4, sticky = N+S+E+W)

header_chg1= Label(window,text="1-hour Change")
header_chg1.grid(row = 0, column = 5, sticky = N+S+E+W)

header_chg24 = Label(window,text="24-hour Change")
header_chg24.grid(row = 0, column = 6, sticky = N+S+E+W)

header_chg7 = Label(window,text="7-day Change")
header_chg7.grid(row = 0, column = 7, sticky = N+S+E+W)

header_hold = Label(window,text="Total Hodlings")
header_hold.grid(row = 0, column = 8, sticky = N+S+E+W)

header_val = Label(window,text="Total Value")
header_val.grid(row = 0, column = 9, sticky = N+S+E+W)

def profitloss(value):
    if value >= 0:
        return "green"
    else:
        return "red"

def getData():
    #Coinmarketcap api
    coinmarketcap_api = requests.get("https://api.coinmarketcap.com/v1/ticker/")
    cmc = json.loads(coinmarketcap_api.content)

    # Portfolio
    portfolio = [{"sym":"LINK","owned":3000,"price":0.2},
             {"sym":"ETH","owned":80,"price":200},
             {"sym":"LSK","owned":1700,"price":1.2},
             {"sym":"XRP","owned":560,"price":0.5},
             {"sym":"BTC","owned":0.4,"price":10000}]

    # Variables for plotting
    coins = []
    size = []

    # Variable instantiation to calculate total changes
    total_difference = 0
    total_value = 0
    counter_row = 1

    # Loop over each dictionary in the cmc content each dict is a coin
    for value in cmc:
        for coin in portfolio:
            if coin["sym"] == value["symbol"]:

                amountpaid = coin["owned"] * coin["price"]
                currrentValue = coin["owned"] * (float(value["price_usd"]))
                difference = currrentValue - amountpaid
                total_difference += difference
                total_value += currrentValue
                coins.append(value["name"])
                size.append(currrentValue)

                name = Label(window,text=value["name"])
                name.grid(row = counter_row, column = 0, sticky = N+S+E+W)

                rk = Label(window,text=value["rank"])
                rk.grid(row = counter_row, column = 1, sticky = N+S+E+W)

                price = Label(window,text="${0:.2f}".format(float(value["price_usd"])))
                price.grid(row = counter_row, column = 2, sticky = N+S+E+W)

                pricepaid = Label(window,text="${0:.2f}".format(float(amountpaid)))
                pricepaid.grid(row = counter_row, column = 3, sticky = N+S+E+W)

                profit = Label(window,text="${0:.2f}".format(float(difference)), fg=profitloss(difference))
                profit.grid(row = counter_row, column = 4, sticky = N+S+E+W)

                change1= Label(window,text=value["percent_change_1h"], fg = profitloss(float(value["percent_change_1h"])))
                change1.grid(row = counter_row, column = 5, sticky = N+S+E+W)

                change24 = Label(window,text=value["percent_change_24h"],fg = profitloss(float(value["percent_change_24h"])))
                change24.grid(row = counter_row, column = 6, sticky = N+S+E+W)

                change7 = Label(window,text=value["percent_change_7d"],fg = profitloss(float(value["percent_change_7d"])))
                change7.grid(row = counter_row, column = 7, sticky = N+S+E+W)

                hold = Label(window,text=coin["owned"])
                hold.grid(row = counter_row, column = 8, sticky = N+S+E+W)

                val = Label(window,text="${0:.2f}".format(currrentValue))
                val.grid(row = counter_row, column = 9, sticky = N+S+E+W)

                counter_row += 1


    header_totalchange = Label(window,text="Total Proftit/Loss: ${0:.2f}".format(total_difference),fg = profitloss(total_difference))
    header_totalchange.grid(row = counter_row, column = 0, sticky = N+S+E+W,padx=10, pady=5)

    header_total = Label(window,text="Portfolio Value: ${0:.2f}".format(total_value))
    header_total.grid(row = counter_row + 1, column = 0, sticky = N+S+E+W, padx=10, pady=5)

    cmc = ""

    b1 = Button(window,text='Update',width = 12, command = getData)
    b1.grid(row=counter_row+1,column=9,sticky=E+S,padx=10, pady=10)

    def plot(labels,size):
        labels = labels;
        size = size;
        fig1, ax1 = plt.subplots()
        ax1.pie(size, labels=labels, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
        plt.show()


    b2 = Button(window,text='Plot',width = 12, command = lambda:plot(coins,size))
    b2.grid(row=counter_row,column=9,sticky=E+S,padx=10, pady=10)

getData()

window.mainloop()
