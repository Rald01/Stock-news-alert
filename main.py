import requests
import datetime
from twilio.rest import Client

ACCOUNT_SID = " " # your twilio account sid
AUTH_TOKEN = " " # your twilio auth token

VIRTUAL_NUMBER = " " # your virtual number from twilio
VERIFIED_NUMBER = " " # your verified number

STOCK = "TSLA" # stock name
COMPANY_NAME = "Tesla Inc" # company name

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

api_key = " " #API key from alphavantage.co
api_key2 = " " #API key from newsapi.org

date = datetime.datetime.now()
today = (date.strftime("%d"))
month = (date.strftime("%m"))
yesterday = int(today)-1
day_before_yesterday = yesterday - 1
yesterday = str(yesterday)
day_before_yesterday = str(day_before_yesterday)

# Getting the closing price for yesterday and the day before yesterday;
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


if abs(percentage_change) > 1:
    response2 = requests.get(url=f"https://newsapi.org/v2/everything?q=tesla&from=2022-{month}-1&"
                                 f"to=&apiKey={api_key2}")
    news_data = response2.json()
    first_three_articles = news_data["articles"][0:3]


    ## Use twilio.com/docs/sms/quickstart/python
    # Sending a separate message with each article's title and description to your phone number.


    # Download the helper library from https://www.twilio.com/docs/python/install


    # Find your Account SID and Auth Token in Account Info and set the environment variables.
    # See http://twil.io/secure
    account_sid = ACCOUNT_SID
    auth_token = AUTH_TOKEN
    
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

