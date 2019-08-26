# Currency Tracker

追蹤匯率小幫手，可即時用``Line``通知<br>
目前提供台灣銀行與台新銀行外幣匯率

## Add LINE Notify ID

The LINE Notify ID can get from [Here](https://notify-bot.line.me/zh_TW/)

```python
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
```