import tweepy
# the below import is for calculating date. Not needed for you but I needed it.
from datetime import date
import shutil, pathlib, os
import yaml

# Load keys from YAML file
with open("Project/keys_2.yaml", 'r') as file:
    config = yaml.safe_load(file)

# Access keys
twitter_config = config['twitter']

# Assign the keys
BEARER_TOKEN = twitter_config['Bearer-Token']
CONSUMER_KEY = twitter_config['API-Key']
CONSUMER_SECRET = twitter_config['API-Key-Secret']
ACCESS_KEY = twitter_config['Access-Token']
ACCESS_SECRET = twitter_config['Access-Token-Secret']

# Since I started the event for 30daysofJS on Nov 6 and I wanted to include this is day X in my tweet dynamically, 
# I am setting up the date logic part. This is totally optional.
startdate = date(2024, 9, 28)
today = date.today()
mydays = (today - startdate).days + 1
# End of optional part

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(
    ACCESS_KEY,
    ACCESS_SECRET,
)
# this is the syntax for twitter API 2.0. It uses the client credentials that we created
newapi = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    access_token=ACCESS_KEY,
    access_token_secret=ACCESS_SECRET,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
)

# Create API object using the old twitter APIv1.1
api = tweepy.API(auth)

# adding the tweet content in a multiline string. The {mydays} part is updated dynamically as the number of days from 6th Nov, 2023
sampletweet = f""" It's the first one
MDF!!!
"""

# I add the screenshot in the same directory as the code and add only one image. Since it is a screenshot taken using windows Snip, it is in png
for images in os.listdir(os.path.abspath(os.path.dirname(__file__))):
    # check if the image ends with png and take the first image that you find
    if images.endswith(".png"):
        img = images
        break

# upload the media using the old api
media = api.media_upload(os.path.join(os.path.abspath(os.path.dirname(__file__)), img))
# create the tweet using the new api. Mention the image uploaded via the old api
post_result = newapi.create_tweet(text=sampletweet, media_ids=[media.media_id])
# the following line prints the response that you receive from the API. You can save it or process it in anyway u want. I am just printing it.
print(post_result)
# get the file extension. This would be png by default but I was experimenting with different images. Will update this if required
file_extension = pathlib.Path(img).suffix
# Move the image to archives folder and rename it as per the date it was uploaded. I am only adding one post per day so this makes more sense
shutil.move(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), img),
    os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "Archives",
        today.strftime("%Y%m%d") + file_extension,
    ),
)