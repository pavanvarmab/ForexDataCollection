import threading 
import requests
import pymongo
from datetime import datetime
from multiprocessing import Process

seconds=7200
EURUSDCounter = 0
GBPEURCounter = 0
USDCHFCounter = 0
clientObject = pymongo.MongoClient("mongodb://localhost:27017/")
databaseObject = clientObject["tradingdata"]
EURUSDOb = databaseObject["EURUSD"]
GBPEUROb = databaseObject["GBPEUR"]
USDCHFOb = databaseObject["USDCHF"]


#to get the current FX rate of EURUSD and insert into MongoDB collection
def EURUSD():
    response = requests.get('https://api.polygon.io/v1/conversion/EUR/USD?precision=2&apiKey=')
    if response.ok:
        josnObject=response.json()
        jsonDocument = {"FXrate": josnObject["last"]["bid"], "timestamp":datetime.fromtimestamp(josnObject["last"]["timestamp"]//1000),"insertedtimestamp":datetime.now() }
        response = EURUSDOb.insert_one(jsonDocument)
        #print(EURUSDCounter,"EURUSD",datetime.fromtimestamp(josnObject["last"]["timestamp"]/1000))

#to get the current FX rate of GBPEUR and insert into MongoDB collection
def GBPEUR():
    response = requests.get('https://api.polygon.io/v1/conversion/GBP/EUR?precision=2&apiKey=')
    if response.ok:
        josnObject=response.json()
        jsonDocument = {"FXrate": josnObject["last"]["bid"], "timestamp":datetime.fromtimestamp(josnObject["last"]["timestamp"]//1000),"insertedtimestamp":datetime.now() }
        response = GBPEUROb.insert_one(jsonDocument)
        #print(GBPEURCounter,"GBPEUR",datetime.fromtimestamp(josnObject["last"]["timestamp"]/1000))

#to get the current FX rate of USDCHF and insert into MongoDB collection
def USDCHF():
    response = requests.get('https://api.polygon.io/v1/conversion/USD/CHF?precision=2&apiKey=')
    if response.ok:
        josnObject=response.json()
        jsonDocument = {"FXrate": josnObject["last"]["bid"], "timestamp":datetime.fromtimestamp(josnObject["last"]["timestamp"]//1000),"insertedtimestamp":datetime.now() }
        response = USDCHFOb.insert_one(jsonDocument)
        #print(USDCHFCounter,"USDCHF",datetime.fromtimestamp(josnObject["last"]["timestamp"]/1000))

#4 the below three functions creates a new process every time to call the above the functions respectively. 
#5 these don't wait for the above functions execution, they just call and their task is completed.
#multiprocessing 
def EURUSDrun():
    Process(target=EURUSD).start()

def GBPEURrun():
    Process(target=GBPEUR).start()

def USDCHFrun():
    Process(target=USDCHF).start()

#3 the sheduler creates a new thread every second to call the respective currency pair run functions above.
#multithreading
def shedulerFunction (interval, helperFunction,iterations):
    if iterations != 1:
        threading.Timer(1,shedulerFunction,[interval, helperFunction,0 if iterations == 0 else iterations-1]).start()
    helperFunction()

#1 The main function creates three different processes each for one currency pair. #multiprocessing 
#2 each process call's shedulerFunction that starts a sheduer.     
if __name__ == '__main__':
    Process(target=shedulerFunction, args=(1,EURUSDrun,seconds)).start()
    Process(target=shedulerFunction, args=(1,GBPEURrun,seconds)).start()
    Process(target=shedulerFunction, args=(1,USDCHFrun,seconds)).start()
