import tweepy

d = {}
with open('twitter.properties', mode='r') as my_file:
    for line in my_file:
        (key, value) = line.split('=')
        value = value.strip('\n')
        d[key] = value

auth = tweepy.OAuthHandler(d['consumer_key'], d['consumer_secret'])
auth.set_access_token(d['access_token'], d['access_token_secret'])

api = tweepy.API(auth)
user = api.me()
print(user.name)
