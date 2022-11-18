from http import client
from unicodedata import decomposition
import requests
import json
import csv
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd
from api import api_key,secret_key

binance='https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "123",
    "content-type": "application/json",
    "Host": "p2p.binance.com",
    "Origin": "https://p2p.binance.com",
    "Pragma": "no-cache",
    "TE": "Trailers",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0"
}


def data(asset="USDT",fiat="RUB",payTypes="TinkoffNew",tradeType="BUY",transAmount="500"):
    dt={
        "asset": asset,
        "fiat": fiat,
        "merchantCheck": False,
        "page": 1,
        "payTypes": [payTypes],
        "publisherType": None,
        "rows": 1,
        "tradeType": tradeType,
        "transAmount":  transAmount
        }
    return dt

def Zapros(asset,fiat,payTypes,tradeType,transAmount):
    r = requests.post(binance, headers=headers, json=data(asset=asset,fiat=fiat,payTypes=payTypes,tradeType=tradeType,transAmount=transAmount))
    val = r.json()["data"][0]["adv"]["price"]
    return val

def mz(asset,payTypes,price):
    val1=Zapros(asset=asset,fiat="RUB",payTypes=payTypes,tradeType="BUY",transAmount="500")
    val2=Zapros(asset=asset,fiat="RUB",payTypes=payTypes,tradeType="SELL",transAmount="500")
    val=round(((float(val1)/float(val2))-1)*100,2)
    dt=[]
    dt.append(f"{payTypes} {asset}")
    dt.append(price)    
    dt.append(val1)
    dt.append(val2)
    dt.append(val)
    return dt

asset_data=["USDT","BTC","BUSD","BNB","ETH"]
#payTypes_data=["TinkoffNew","QIWI","YandexMoneyNew","RaiffeisenBank","PostBankNew"]
payTypes_data=["TinkoffNew","QIWI","RaiffeisenBank"]
#payTypes_data=["TinkoffNew"]


def resPr(deposit,var1,var2,priceSPOT):    
    res1=deposit/var1    
    dollar=res1*priceSPOT            
    #dollar=res1/priceSPOT            
    res2=dollar*var2    
    res3=round(((res2/deposit)-1)*100,2)
    
    return res3

def aresPr(deposit,var1,var2,priceSPOT):    
    res1=deposit/var1    
    
    dollar=res1/priceSPOT            
    res2=dollar*var2    
    res3=round(((res2/deposit)-1)*100,2)
    
    return res3

def main():    
    deposit1=5000
    deposit2=1000
    pribil=1
    pribil_all=0

    P2P_BUYpricerub1=\
        {
            'TinkoffNewUSDT':Zapros("USDT","RUB","TinkoffNew","BUY",deposit1),
            'TinkoffNewBTC':Zapros("BTC","RUB","TinkoffNew","BUY",deposit1),
            'TinkoffNewBUSD':Zapros("BUSD","RUB","TinkoffNew","BUY",deposit1),
            'TinkoffNewBNB':Zapros("BNB","RUB","TinkoffNew","BUY",deposit1),
            'TinkoffNewETH':Zapros("ETH","RUB","TinkoffNew","BUY",deposit1),
            'QIWIUSDT':Zapros("USDT","RUB","QIWI","BUY",deposit1),
            'QIWIBTC':Zapros("BTC","RUB","QIWI","BUY",deposit1),
            'QIWIBUSD':Zapros("BUSD","RUB","QIWI","BUY",deposit1),
            'QIWIBNB':Zapros("BNB","RUB","QIWI","BUY",deposit1),
            'QIWIETH':Zapros("ETH","RUB","QIWI","BUY",deposit1),
            # 'YandexMoneyNewUSDT':Zapros("USDT","RUB","YandexMoneyNew","BUY",deposit1), 
            # 'YandexMoneyNewBTC':Zapros("BTC","RUB","YandexMoneyNew","BUY",deposit1),
            # 'YandexMoneyNewBUSD':Zapros("BUSD","RUB","YandexMoneyNew","BUY",deposit1),
            # 'YandexMoneyNewBNB':Zapros("BNB","RUB","YandexMoneyNew","BUY",deposit1),
            # 'YandexMoneyNewETH':Zapros("ETH","RUB","YandexMoneyNew","BUY",deposit1),
            'RaiffeisenBankUSDT':Zapros("USDT","RUB","RaiffeisenBank","BUY",deposit1), 
            'RaiffeisenBankBTC':Zapros("BTC","RUB","RaiffeisenBank","BUY",deposit1),
            'RaiffeisenBankBUSD':Zapros("BUSD","RUB","RaiffeisenBank","BUY",deposit1),
            'RaiffeisenBankBNB':Zapros("BNB","RUB","RaiffeisenBank","BUY",deposit1),
            'RaiffeisenBankETH':Zapros("ETH","RUB","RaiffeisenBank","BUY",deposit1),            
            # 'PostBankNewUSDT':Zapros("USDT","RUB","PostBankNew","BUY",deposit1), 
            # 'PostBankNewBTC':Zapros("BTC","RUB","PostBankNew","BUY",deposit1),
            # 'PostBankNewBUSD':Zapros("BUSD","RUB","PostBankNew","BUY",deposit1),
            # 'PostBankNewBNB':Zapros("BNB","RUB","PostBankNew","BUY",deposit1),
            # 'PostBankNewETH':Zapros("ETH","RUB","PostBankNew","BUY",deposit1),                        
        }

    P2P_BUYpricerub2=\
        {
            'TinkoffNewUSDT':Zapros("USDT","RUB","TinkoffNew","BUY",deposit2),
            'TinkoffNewBTC':Zapros("BTC","RUB","TinkoffNew","BUY",deposit2),
            'TinkoffNewBUSD':Zapros("BUSD","RUB","TinkoffNew","BUY",deposit2),
            'TinkoffNewBNB':Zapros("BNB","RUB","TinkoffNew","BUY",deposit2),
            'TinkoffNewETH':Zapros("ETH","RUB","TinkoffNew","BUY",deposit2),
            'QIWIUSDT':Zapros("USDT","RUB","QIWI","BUY",deposit2),
            'QIWIBTC':Zapros("BTC","RUB","QIWI","BUY",deposit2),
            'QIWIBUSD':Zapros("BUSD","RUB","QIWI","BUY",deposit2),
            'QIWIBNB':Zapros("BNB","RUB","QIWI","BUY",deposit2),
            'QIWIETH':Zapros("ETH","RUB","QIWI","BUY",deposit2),
            # 'YandexMoneyNewUSDT':Zapros("USDT","RUB","YandexMoneyNew","BUY",deposit2), 
            # 'YandexMoneyNewBTC':Zapros("BTC","RUB","YandexMoneyNew","BUY",deposit2),
            # 'YandexMoneyNewBUSD':Zapros("BUSD","RUB","YandexMoneyNew","BUY",deposit2),
            # 'YandexMoneyNewBNB':Zapros("BNB","RUB","YandexMoneyNew","BUY",deposit2),
            # 'YandexMoneyNewETH':Zapros("ETH","RUB","YandexMoneyNew","BUY",deposit2),
            'RaiffeisenBankUSDT':Zapros("USDT","RUB","RaiffeisenBank","BUY",deposit2), 
            'RaiffeisenBankBTC':Zapros("BTC","RUB","RaiffeisenBank","BUY",deposit2),
            'RaiffeisenBankBUSD':Zapros("BUSD","RUB","RaiffeisenBank","BUY",deposit2),
            'RaiffeisenBankBNB':Zapros("BNB","RUB","RaiffeisenBank","BUY",deposit2),
            'RaiffeisenBankETH':Zapros("ETH","RUB","RaiffeisenBank","BUY",deposit2),            
            # 'PostBankNewUSDT':Zapros("USDT","RUB","PostBankNew","BUY",deposit2), 
            # 'PostBankNewBTC':Zapros("BTC","RUB","PostBankNew","BUY",deposit2),
            # 'PostBankNewBUSD':Zapros("BUSD","RUB","PostBankNew","BUY",deposit2),
            # 'PostBankNewBNB':Zapros("BNB","RUB","PostBankNew","BUY",deposit2),
            # 'PostBankNewETH':Zapros("ETH","RUB","PostBankNew","BUY",deposit2),                        
        }

    
    minUSDT=float(P2P_BUYpricerub1[f"{payTypes_data[0]}USDT"])
    for i in range(1,len(payTypes_data)):
        if minUSDT>float(P2P_BUYpricerub1[f"{payTypes_data[i]}USDT"]):
            minUSDT=float(P2P_BUYpricerub1[f"{payTypes_data[i]}USDT"])
        if minUSDT>float(P2P_BUYpricerub2[f"{payTypes_data[i]}USDT"]):
            minUSDT=float(P2P_BUYpricerub2[f"{payTypes_data[i]}USDT"])

    minBTC=float(P2P_BUYpricerub1[f"{payTypes_data[0]}BTC"])
    for i in range(1,len(payTypes_data)):
        if minBTC>float(P2P_BUYpricerub1[f"{payTypes_data[i]}BTC"]):
            minBTC=float(P2P_BUYpricerub1[f"{payTypes_data[i]}BTC"])
        if minBTC>float(P2P_BUYpricerub2[f"{payTypes_data[i]}BTC"]):
            minBTC=float(P2P_BUYpricerub2[f"{payTypes_data[i]}BTC"])

    minBUSD=float(P2P_BUYpricerub1[f"{payTypes_data[0]}BUSD"])
    for i in range(1,len(payTypes_data)):
        if minBUSD>float(P2P_BUYpricerub1[f"{payTypes_data[i]}BUSD"]):
            minBUSD=float(P2P_BUYpricerub1[f"{payTypes_data[i]}BUSD"])
        if minBUSD>float(P2P_BUYpricerub2[f"{payTypes_data[i]}BUSD"]):
            minBUSD=float(P2P_BUYpricerub2[f"{payTypes_data[i]}BUSD"])

    minBNB=float(P2P_BUYpricerub1[f"{payTypes_data[0]}BNB"])
    for i in range(1,len(payTypes_data)):
        if minBNB>float(P2P_BUYpricerub1[f"{payTypes_data[i]}BNB"]):
            minBNB=float(P2P_BUYpricerub1[f"{payTypes_data[i]}BNB"])
        if minBNB>float(P2P_BUYpricerub2[f"{payTypes_data[i]}BNB"]):
            minBNB=float(P2P_BUYpricerub2[f"{payTypes_data[i]}BNB"])

    minETH=float(P2P_BUYpricerub1[f"{payTypes_data[0]}ETH"])    
    for i in range(1,len(payTypes_data)):
        if minETH>float(P2P_BUYpricerub1[f"{payTypes_data[i]}ETH"]):            
            minETH=float(P2P_BUYpricerub1[f"{payTypes_data[i]}ETH"])
        if minETH>float(P2P_BUYpricerub2[f"{payTypes_data[i]}ETH"]):            
            minETH=float(P2P_BUYpricerub2[f"{payTypes_data[i]}ETH"])
    
    client=Client(api_key,secret_key)
    tickers=client.get_all_tickers()
    ticker_df=pd.DataFrame(tickers)
    ticker_df.set_index('symbol',inplace=True)
   
    print("Taker+Maker")    

    for i in range(0,len(payTypes_data)):
        for ii in range(0,len(payTypes_data)):            
            print("***************************************************")
            print(f"{payTypes_data[i]}->{payTypes_data[ii]}")
            var1=float(P2P_BUYpricerub1[f"{payTypes_data[i]}BTC"])
            var2=float(P2P_BUYpricerub2[f"{payTypes_data[ii]}USDT"])
            var3=float(ticker_df.loc['BTCUSDT']['price'])
            res=resPr(deposit2,var1,var2,var3)    
            res1=resPr(deposit2,minBTC,minUSDT,var3)    
            if res>=pribil and res1>pribil_all:
                print(f"{payTypes_data[i]}(P2P BTC:{var1}|{minBTC})->BTCUSDT(SPOT:{var3})->{payTypes_data[ii]}(P2P USDT:{var2}|{minUSDT})={res}|{res1}")

            var1=float(P2P_BUYpricerub1[f"{payTypes_data[i]}BTC"])
            var2=float(P2P_BUYpricerub2[f"{payTypes_data[ii]}BUSD"])
            var3=float(ticker_df.loc['BTCBUSD']['price'])
            res=resPr(deposit2,var1,var2,var3)    
            res1=resPr(deposit2,minBTC,minBUSD,var3)    
            if res>=pribil and res1>pribil_all:
                print(f"{payTypes_data[i]}(P2P BTC:{var1}|{minBTC})->BTCBUSD(SPOT:{var3})->{payTypes_data[ii]}(P2P BUSD:{var2}|{minBUSD})={res}|{res1}")

    
            var1=float(P2P_BUYpricerub1[f"{payTypes_data[i]}BTC"])
            var2=float(P2P_BUYpricerub2[f"{payTypes_data[ii]}ETH"])
            var3=float(ticker_df.loc['ETHBTC']['price'])
            res=aresPr(deposit2,var1,var2,var3)    
            res1=aresPr(deposit2,minBTC,minETH,var3)    
            if res>=pribil and res1>pribil_all:
                print(f"{payTypes_data[i]}(P2P BTC:{var1}|{minBTC})->ETHBTC(SPOT:{var3})->{payTypes_data[ii]}(P2P ETH:{var2}|{minETH})={res}|{res1}")

            var1=float(P2P_BUYpricerub1[f"{payTypes_data[i]}BTC"])
            var2=float(P2P_BUYpricerub2[f"{payTypes_data[ii]}BNB"])
            var3=float(ticker_df.loc['BNBBTC']['price'])
            res=aresPr(deposit2,var1,var2,var3)    
            res1=aresPr(deposit2,minBTC,minBNB,var3)    
            if res>=pribil and res1>pribil_all:
                print(f"{payTypes_data[i]}(P2P BTC:{var1}|{minBTC})->BNBBTC(SPOT:{var3})->{payTypes_data[ii]}(P2P BNB:{var2}|{minBNB})={res}|{res1}")

            var1=float(P2P_BUYpricerub1[f"{payTypes_data[i]}USDT"])
            var2=float(P2P_BUYpricerub2[f"{payTypes_data[ii]}BUSD"])
            var3=float(ticker_df.loc['BUSDUSDT']['price'])
            res=aresPr(deposit2,var1,var2,var3)    
            res1=aresPr(deposit2,minUSDT,minBUSD,var3)    
            if res>=pribil and res1>pribil_all:
                print(f"{payTypes_data[i]}(P2P USDT:{var1}|{minUSDT})->BUSDUSDT(SPOT:{var3})->{payTypes_data[ii]}(P2P BUSD:{var2}|{minBUSD})={res}|{res1}")

            var1=float(P2P_BUYpricerub1[f"{payTypes_data[i]}USDT"])
            var2=float(P2P_BUYpricerub2[f"{payTypes_data[ii]}BNB"])
            var3=float(ticker_df.loc['BNBUSDT']['price'])
            res=aresPr(deposit2,var1,var2,var3)    
            res1=aresPr(deposit2,minUSDT,minBNB,var3)    
            if res>=pribil and res1>pribil_all:
                print(f"{payTypes_data[i]}(P2P USDT:{var1}|{minUSDT})->BNBUSDT(SPOT:{var3})->{payTypes_data[ii]}(P2P BNB:{var2}|{minBNB})={res}|{res1}")

            var1=float(P2P_BUYpricerub1[f"{payTypes_data[i]}USDT"])
            var2=float(P2P_BUYpricerub2[f"{payTypes_data[ii]}ETH"])
            var3=float(ticker_df.loc['ETHUSDT']['price'])
            res=aresPr(deposit2,var1,var2,var3)    
            res1=aresPr(deposit2,minUSDT,minETH,var3)    
            if res>=pribil and res1>pribil_all:
                print(f"{payTypes_data[i]}(P2P USDT:{var1}|{minUSDT})->ETHUSDT(SPOT:{var3})->{payTypes_data[ii]}(P2P ETH:{var2}|{minETH})={res}|{res1}")

            var1=float(P2P_BUYpricerub1[f"{payTypes_data[i]}BNB"])
            var2=float(P2P_BUYpricerub2[f"{payTypes_data[ii]}BUSD"])
            var3=float(ticker_df.loc['BNBUSDT']['price'])
            res=resPr(deposit2,var1,var2,var3)    
            res1=resPr(deposit2,minBNB,minBUSD,var3)    
            
            if res>=pribil and res1>pribil_all:
                print(f"{payTypes_data[i]}(P2P BNB:{var1}|{minBNB})->BNBUSDT(SPOT:{var3})->{payTypes_data[ii]}(P2P BUSD:{var2}|{minBUSD})={res}|{res1}")

            var1=float(P2P_BUYpricerub1[f"{payTypes_data[i]}ETH"])
            var2=float(P2P_BUYpricerub2[f"{payTypes_data[ii]}BUSD"])
            var3=float(ticker_df.loc['ETHBUSD']['price'])
            res=resPr(deposit2,var1,var2,var3)    
            res1=resPr(deposit2,minETH,minBUSD,var3)    
            if res>=pribil and res1>pribil_all:
                print(f"{payTypes_data[i]}(P2P ETH:{var1}|{minETH})->ETHBUSD(SPOT:{var3})->{payTypes_data[ii]}(P2P BUSD:{var2}|{minBUSD})={res}|{res1}")

            var1=float(P2P_BUYpricerub1[f"{payTypes_data[i]}ETH"])
            var2=float(P2P_BUYpricerub2[f"{payTypes_data[ii]}BNB"])
            var3=float(ticker_df.loc['BNBETH']['price'])
            res=aresPr(deposit2,var1,var2,var3)    
            res1=aresPr(deposit2,minETH,minBNB,var3)    
            if res>=pribil and res1>pribil_all:
                print(f"{payTypes_data[i]}(P2P ETH:{var1}|{minETH})->ETHBNB(SPOT:{var3})->{payTypes_data[ii]}(P2P BNB:{var2}|{minBNB})={res}|{res1}")


    # print("Загрузка идет.....")
    # with open("data.csv","w") as file:
    #     writer=csv.writer(file)
    #     writer.writerow(["BANK","RUB","BUY","SELL","%"])
                        
    #     for i in range(0,len(asset_data)):
    #         for ii in range(0,len(payTypes_data)):
    #             dt=mz(asset_data[i],payTypes_data[ii],ticker_df.loc[f'{asset_data[i]}RUB']['price'])
    #             writer.writerow(dt)
    
    # print("Файл data.csv сформирован")



    
if __name__ == '__main__':
    main()
