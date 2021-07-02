from nylas import APIClient

CLIENT_ID = "1c755lkyldpave6ljt6xg6pxn"
CLIENT_SECRET = "7bdc46kyhny542va6e59pv65v"
ACCESS_TOKEN = "Apujz8Iaq5FvTeuFINijOzh9wpDInF"

nylas = APIClient(
    CLIENT_ID,
    CLIENT_SECRET,
    ACCESS_TOKEN
)

messages = nylas.messages.all(limit=10)
print(len(messages))

for message in messages:
    print(message.body)
