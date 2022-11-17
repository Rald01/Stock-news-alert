import requests
import datetime
import os
from twilio.rest import Client

VIRTUAL_NUMBER = "+17174936759"
VERIFIED_NUMBER = "+2349067112294"

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
api_key = " 8NLAMVKS52CZSDZS"
api_key2 = "0fcc01c020be4418a31cca5a094a3f77"

parameters = {
    "function": "TIME_SERIES_INTRADAY",
    "SYMBOL": STOCK,
    "apikey": api_key,
    "interval": "60min"
}
date = datetime.datetime.now()
today = (date.strftime("%d"))
month = (date.strftime("%m"))
yesterday = int(today)-1
day_before_yesterday = yesterday - 1
yesterday = str(yesterday)
day_before_yesterday = str(day_before_yesterday)

## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# HINT 1: Get the closing price for yesterday and the day before yesterday;
# Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
# HINT 2: Work out the value of 5% of yerstday's closing stock price.
response = requests.get(url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={STOCK}&'
                              f'apikey={api_key}')
print(response.status_code)
data = response.json()
# print(data)

yesterday_close = float(data["Time Series (Daily)"][f"2022-11-{yesterday}"]["4. close"])
day_before_yesterday_close = float(data["Time Series (Daily)"][f"2022-11-{day_before_yesterday}"]["4. close"])

change_in_closing_price = (float(yesterday_close) - float(day_before_yesterday_close))
percentage_change = round((change_in_closing_price/float(yesterday_close)) * 100)
print(percentage_change)
up_down = None
if change_in_closing_price > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
# HINT 1: Think about using the Python Slice Operator
if abs(percentage_change) > 1:
    response2 = requests.get(url=f"https://newsapi.org/v2/everything?q=tesla&from=2022-{month}-1&"
                                 f"to=&apiKey={api_key2}")
    news_data = response2.json()
    first_three_articles = news_data["articles"][0:3]


    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    # Send a separate message with each article's title and description to your phone number.
    #HINT 1: Consider using a List Comprehension.

    # Download the helper library from https://www.twilio.com/docs/python/install


    # Find your Account SID and Auth Token in Account Info and set the environment variables.
    # See http://twil.io/secure
#    account_sid = os.environ['AC89fe1bf807eb3f383fcba629da306504']
#    auth_token = os.environ['690f1ebb7cb2d7d365e26d4ac9af1f28']
    account_sid = 'AC89fe1bf807eb3f383fcba629da306504'
    auth_token = '690f1ebb7cb2d7d365e26d4ac9af1f28'
    client = Client(account_sid, auth_token)
    formatted_articles = [
        f"{STOCK}: {up_down}{percentage_change}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for
        article in first_three_articles]

    print(formatted_articles)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_NUMBER,
            to=VERIFIED_NUMBER
        )

        print(message.sid)

#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

