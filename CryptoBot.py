import ccxt
from tradingview_ta import TA_Handler, Interval, Exchange, Compute
import requests

def arbitraj(pair):
    send_message = pair + " prices are searched for you on all exchanges.\nPlease wait..."
    requests.post(url=send_url, data={'chat_id': chat_id, 'text': send_message}).json()

    account = []
    account.append(ccxt.binance())
    account.append(ccxt.bitbay())
    account.append(ccxt.bitfinex())
    account.append(ccxt.bitforex())
    account.append(ccxt.bithumb())
    account.append(ccxt.bitmex())
    account.append(ccxt.bitpanda())
    account.append(ccxt.coinbase())
    account.append(ccxt.coinegg())
    account.append(ccxt.ftx())
    account.append(ccxt.gemini())
    account.append(ccxt.hitbtc())
    account.append(ccxt.huobipro())
    account.append(ccxt.idex())
    account.append(ccxt.kraken())
    account.append(ccxt.kucoin())
    account.append(ccxt.liquid())
    account.append(ccxt.okcoin())
    account.append(ccxt.okex())
    account.append(ccxt.poloniex())

    minAsk = float(account[0].fetch_ticker(pair + '/USDT')['ask'])
    maxBid = float(account[0].fetch_ticker(pair + '/USDT')['bid'])
    askName = ""
    bidName = ""


    for i in range(0, len(account)):
        markets = account[i].load_markets()

        if pair + '/USDT' in markets:
            if minAsk > float(account[i].fetch_ticker(pair + '/USDT')['ask']): 
                minAsk = float(account[i].fetch_ticker(pair + '/USDT')['ask']) 
                askName = account[i]                                           
            if maxBid < float(account[i].fetch_ticker(pair + '/USDT')['bid']): 
                maxBid = float(account[i].fetch_ticker(pair + '/USDT')['bid']) 
                bidName = account[i]                                           
        elif pair + '/USD' in markets:
            if minAsk > float(account[i].fetch_ticker(pair + '/USD')['ask']):
                minAsk = float(account[i].fetch_ticker(pair + '/USD')['ask'])
                askName = account[i]
            if maxBid < float(account[i].fetch_ticker(pair + '/USD')['bid']):
                maxBid = float(account[i].fetch_ticker(pair + '/USD')['bid'])
                bidName = account[i]
        else:
            continue

    send_message = " Exchanges with the most price difference:\n\n" + str(askName) + " - Buying: " + str(minAsk) + "$\n" + str(bidName) + " - Sales: " + str(maxBid) + "$"
    requests.post(url=send_url, data={'chat_id': chat_id, 'text': send_message}).json()

    
    send_message = pair + " is selected...\nChoose the action you want to take below:\n/ARB - Arbitrage Research\n/GENERAL - General Analysis Advice\n/PSAR - Parabolic SAR Analysis Advice\n/OSC - Oscillators Average\n/RSI - RSI Indicator Analysis Advice\n/MACD - MACD Indicator Analysis Advice\n/CCI - CCI Indicator Analysis Advice\n\nTo change your chosen coin and return to the beginning, /Change"
    requests.post(url=send_url, data={'chat_id': chat_id, 'text': send_message}).json()

def analysis(pair, chosen): 
    crypto = TA_Handler(
        symbol=pair + "USDT",
        screener="CRYPTO",
        exchange="BINANCE",
        interval=Interval.INTERVAL_1_DAY
    )
    
    if (chosen=="GENERAL"): 
        send_message = "\"" + pair + "\" The General Analysis Recommendation is as follows:\n" + str(crypto.get_analysis().summary["RECOMMENDATION"]) + "\nBUY: " + str(crypto.get_analysis().summary["BUY"]) + "\nNEUTRAL: " + str(crypto.get_analysis().summary["NEUTRAL"]) + "\nSELL: " + str(crypto.get_analysis().summary["SELL"])
    elif (chosen=="PSAR"):
        send_message = "\"" + pair + "\" Parabolic SAR Analysis Advice is as follows:\n" + Compute.PSAR(crypto.get_analysis().indicators["P.SAR"], crypto.get_analysis().indicators["open"])
    elif (chosen=="OSC"):
        send_message = "\"" + pair + "\" The Oscillators Average is as follows:\n" + crypto.get_analysis().oscillators["RECOMMENDATION"]
    elif (chosen=="RSI"): 
        send_message = "\"" + pair + "\" RSI Oscillator Analysis Advice is as follows:\n" + Compute.RSI(crypto.get_analysis().indicators["RSI"], crypto.get_analysis().indicators["RSI[1]"])
    elif (chosen=="MACD"): 
        send_message = "\"" + pair + "\" MACD Oscillator Analysis Advice is as follows:\n" + Compute.MACD(crypto.get_analysis().indicators["MACD.macd"], crypto.get_analysis().indicators["MACD.signal"])
    elif (chosen=="CCI"):
        send_message = "\"" + pair + "\" CCI Oscillator Analysis Advice is as follows:\n" + Compute.CCI20(crypto.get_analysis().indicators["CCI20"], crypto.get_analysis().indicators["CCI20[1]"])

    requests.post(url=send_url, data={'chat_id': chat_id, 'text': send_message}).json()

    
    send_message = pair + " is selected.\nSelect the action you want to take below:\n/ARB - Arbitrage Research\n/GENERAL - General Analysis Advice\n/PSAR - Parabolic SAR Analysis Advice\n/OSC - Oscillators Average\n/RSI - RSI Oscillator Analysis Advice\n/MACD - MACD Oscillator Analysis Advice\n/CCI - CCI Oscillator Analysis Advice\n\nTo change your chosen coin and return to the beginning, /Change"
    requests.post(url=send_url, data={'chat_id': chat_id, 'text': send_message}).json()

send_url = "https://api.telegram.org/<YOUR BOT API TOKEN>/sendMessage"
prev_date = "11111"
pair = ""

chs_text = "Select the action you want to take below:\n/ARB - Arbitrage Research\n/GENERAL - General Analysis Advice\n/PSAR - Parabolic SAR Analysis Advice\n/OSC - Oscillators Average\n/RSI - RSI Oscillator Analysis Advice\n/MACD - MACD Oscillator Analysis Advice\n/CCI - CCI Oscillator Analysis Advice\n\nTo change your chosen coin and return to the beginning, /Change"
while True:
    
    tlg = requests.get("https://api.telegram.org/<YOUR BOT API TOKEN>/getupdates").json()
    last_object = tlg['result'][-1]
    new_date = last_object["message"]["date"]

    if(str(new_date) != str(prev_date)):
        prev_date = new_date
        chat_id = last_object['message']['chat']['id']

        if 'first_name' in last_object['message']['from']:
            first_name = last_object['message']['from']['first_name']
        else: first_name = ""
        if 'last_name' in last_object['message']['from']:
            last_name = last_object['message']['from']['last_name']
        else: last_name = ""

        message_text = last_object['message']['text']

        send_message = ""

        if (message_text.upper() == "/START" or message_text.upper() == "/CHANGE"):
            send_message = "Hi " + first_name + " " + last_name + ",\nPlease select a cryptocurrency to get started:\n/BTC - Bitcoin\n/ETH - Ethereum\n/DOGE - Dogecoin\n/XRP - Ripple\n/ADA - Cardano\n/AVAX - Avalance\n/HOT - HoloCoin \n/DOT - Polkadot\n/LINK - Chainlink\n/XLM - Stellar"
        elif (message_text.upper() == "/BTC"):
            pair = "BTC"
            send_message = "BTC - Bitcoin is selected.\n" + chs_text
        elif (message_text.upper() == "/ETH"):
            pair = "ETH"
            send_message = "ETH - Ethereum is selected.\n" + chs_text
        elif (message_text.upper() == "/DOGE"):
            pair = "DOGE"
            send_message = "DOGE - Dogecoin is selected.\n" + chs_text
        elif (message_text.upper() == "/XRP"):
            pair = "XRP"
            send_message = "XRP - Ripple is selected.\n" + chs_text
        elif (message_text.upper() == "/ADA"):
            pair = "ADA"
            send_message = "ADA - Cardano is selected.\n" + chs_text
        elif (message_text.upper() == "/AVAX"):
            pair = "AVAX"
            send_message = "AVAX - Avalance is selected.\n" + chs_text
        elif (message_text.upper() == "/HOT"):
            pair = "HOT"
            send_message = "HOT - HoloCoin is selected.\n" + chs_text
        elif (message_text.upper() == "/DOT"):
            pair = "DOT"
            send_message = "DOT - Polkadot is selected.\n" + chs_text
        elif (message_text.upper() == "/LINK"):
            pair = "LINK"
            send_message = "LINK - Chainlink is selected.\n" + chs_text
        elif (message_text.upper() == "/XLM"):
            pair = "XLM"
            send_message = "XLM - Stellar is selected.\n" + chs_text
        elif (pair != "" and message_text.upper() == "/ARB"):
            arbitraj(pair)
        elif (pair != "" and message_text.upper() == "/GENERAL"):
            analysis(pair, "GENERAL")
        elif (pair != "" and message_text.upper() == "/PSAR"):
            analysis(pair, "PSAR")
        elif (pair != "" and message_text.upper() == "/OSC"):
            analysis(pair, "OSC")
        elif (pair != "" and message_text.upper() == "/RSI"):
            analysis(pair, "RSI")
        elif (pair != "" and message_text.upper() == "/MACD"):
            analysis(pair, "MACD")
        elif (pair != "" and message_text.upper() == "/CCI"):
            analysis(pair, "CCI")
        else:
            send_message = "Your request is not understood. You can start with\n/Start."

        requests.post(url=send_url, data={'chat_id': chat_id, 'text': send_message}).json()
