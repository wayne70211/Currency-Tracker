from IPython.display import display
import pandas as pd
import numpy as np
import requests
import time
import sys


# 台新銀行爬蟲
def taishinbank(name=None):

    url ="https://www.taishinbank.com.tw/TS/TS06/TS0605/TS060502/index.htm?urlPath1=TS02&urlPath2=TS0202"
    df = pd.read_html(url)[11]
    df = df.drop([0])
    df.columns=['幣別','即期匯率-本行買入','即期匯率-本行賣出','現金匯率-本行買入','現金匯率-本行賣出']
    df.insert(0, '銀行', ['台新銀行' for _ in range(len(df))], True)
    df['幣別']=df['幣別'].str[-3:]

    if any(df['幣別'] == name):
        return df[df['幣別'] == name]
    else:
        return df

# 台灣銀行爬蟲
def taiwanbank(name=None):
    url="http://rate.bot.com.tw/xrt?Lang=zh-TW"
    df = pd.read_html(url)[0]
    df = df.iloc[:,[0,3,4,1,2]]
    df.columns=['幣別','即期匯率-本行買入','即期匯率-本行賣出','現金匯率-本行買入','現金匯率-本行賣出']
    df.insert(0, '銀行', ['台灣銀行' for _ in range(len(df))], True)
    df['幣別']=df['幣別'].str.extract('\((\w+)\)')

    if any(df['幣別'] == name):
        return df[df['幣別'] == name]
    else:
        return df


def search(name=None):
    df = taiwanbank(name)
    df = df.append(taishinbank(name),True)
    try:
        df = df.iloc[:,[2,3,4,5]].astype(float)
        df.insert(0, '銀行', ['台灣銀行','台新銀行'], True)
        #display(df)
        return df
    except ValueError:
        print('幣別不存在')
        return None


# Line 推播
def lineNotifyMessage(token, msg):
    headers = {
          "Authorization": "Bearer " + token,
          "Content-Type" : "application/x-www-form-urlencoded"
      }
    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code


def run(currency,target,token=None):
    tracker = True
    while tracker:
        df = search(currency)
        if df is None:
            break
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                      +'\t目標賣出價:'+str(target[0])
                      +'\t賣出價:'+str(max(df.iloc[:,1]))
                      +'\t目標買入價:'+str(target[1])
                      +'\t買入價:'+str(min(df.iloc[:,2])))

        if any(df['即期匯率-本行買入'] >= target[0]):
            message = ('\n即期 '+currency+' 賣出匯率達標'+
                       '\n賣出價大於 '+str(target[0])+
                       '\n台灣銀行賣出價 : '+df.iloc[0,1].astype(str)+
                       '\n台新銀行賣出價 : '+df.iloc[1,1].astype(str))
            if (token != None):
                lineNotifyMessage(token, message)
            print(message)
            tracker=False
            break

        if any(df['即期匯率-本行賣出'] <= target[1]):
            message = ('\n即期 '+currency+' 買入匯率達標'+
                       '\n買入價小於 '+str(target[1])+
                       '\n台灣銀行買入價 : '+df.iloc[0,2].astype(str)+
                       '\n台新銀行買入價 : '+df.iloc[1,2].astype(str))
            if (token != None):
                lineNotifyMessage(token, message)
            print(message)
            tracker=False
            break

        time.sleep(300)


if __name__=="__main__":
    #currency='AUD'
    currency=input('追蹤匯率幣別:')
    print('幣別:'+currency)
    target = []
    #target = [21.05,21.0]  #賣出價,買入價
    try:
        sell = float(input('目標賣出價:'))
        buy  = float(input('目標買入價:'))
        target.append(sell)
        target.append(buy)
        token = ''  # Line Notify ID
        run(currency,target,token)

    except ValueError:
        print('輸入錯誤，請再試一次')
