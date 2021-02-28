import discord
import os
from nsetools import Nse
import pandas as pd
store = pd.HDFStore('store.h5')

data = {
        "username":[],
        "ticker":[],
        "buyPrice":[],
        "quantity":[]
        }
orders = pd.DataFrame(data)


x=''
user_message=[]
global game 
game = {}

nse = Nse()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    


@client.event   
    
async def on_message(message):
    global username
    username = message.author.name
    
    
    if message.author == client.user:
        return

    if message.content.startswith('$enter'):
        await addPlayer(message)
        await message.channel.send('Hi {}. You have successfully entered in the contest. Enter the ticker for a stock that you would like to add to your portfolio'.format(message.author.name))
        
    if message.content.startswith('$buy'):
        global user_message
        global x
        user_message = message.content.split()
        await message.channel.send(user_message[1])
        x = await getPrice(user_message[1],message)
        await message.channel.send('The current price is {}. Do you want me to confirm the order?'.format(x))
        


    if message.content.startswith('$yes'):
        await stockBuy(message, x, int(user_message[2]), orders)
        
    if message.content.startswith('$no'):
        await message.channel.send('Use $buy to enter a changed value of quantity or changing the ticker')
        
            
        
async def addPlayer(message):
    game[username]=100000  
    await message.channel.send(game)
    
    
    
async def getPrice(ticker,message):    
    try:
        stock = nse.get_quote(ticker)
        return stock['basePrice']
    except:
        await message.channel.send("No such ticker found on the NSE. Try entering a new one.")
        
        
    
async def stockBuy(message , cost , buyQuantity, orders):
    if(cost*buyQuantity>game[username]):
        await message.channel.send("You're broke. Try entering a quantity you can afford")
    
    else:
        game[username] = 100000- cost*buyQuantity
        await portfolio(message, cost, buyQuantity,orders)
        await message.channel.send(game[username])
        

async def portfolio(message, cost, buyQuantity, orders):
    newOrder={
    "username":username,
    "ticker":user_message[1],
    "buyPrice":cost,
    "quantity":buyQuantity
    }
    store['orders']
    orders = orders.append(newOrder, ignore_index=True)
    store['orders'] = orders
    await message.channel.send(orders.to_markdown())

client.run('ODE0ODc1OTg2MTc1ODUyNTc0.YDkOZg.k71p1MM1T1vG5KtbQvAQ8uHUR40')


