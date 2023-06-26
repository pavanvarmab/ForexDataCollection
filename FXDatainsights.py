import pymongo
from pandas import DataFrame

clientObject = pymongo.MongoClient("mongodb://localhost:27017/")
databaseObject = clientObject["tradingdata"]
EURUSDOb = databaseObject["EURUSD"]
GBPEUROb = databaseObject["GBPEUR"]
USDCHFOb = databaseObject["USDCHF"]

EURUSDdf = DataFrame(list(EURUSDOb.find()))
GBPEURdf = DataFrame(list(GBPEUROb.find()))
USDCHFdf = DataFrame(list(USDCHFOb.find()))

print("EURUSD average FX rate :","{0:.6f}".format(EURUSDdf["FXrate"].mean()))
print("GBPEUR average FX rate :","{0:.6f}".format(GBPEURdf["FXrate"].mean()))
print("USDCHF average FX rate :","{0:.6f}".format(USDCHFdf["FXrate"].mean()))