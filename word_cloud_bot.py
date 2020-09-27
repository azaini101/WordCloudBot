import praw
import pandas as pd
from PIL import Image
from os import path
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from imgurpython import ImgurClient

client_id = 'IMGUR_CLIENT_ID'
client_secret = 'IMGUR_SECRET'
client = ImgurClient(client_id, client_secret)
def createWordCloud(text, id, background_color="white", max_words=1000, mask=np.array(Image.open("reddit_logo.png")), width=1000, height=600):
    wc = WordCloud(background_color = background_color, max_words = max_words, mask=mask, width=width, height=height)
    wc.generate(text)
    plt.imshow(wc)
    wc.to_file(id + "cloud.png")
    x = client.upload_from_path(id+'cloud.png')
    return "https://i.imgur.com/{}.png".format(x["id"])

reddit = praw.Reddit(client_id='REDDIT_ID',
                     client_secret='REDDIT_SECRET',
                     user_agent='my user agent',
                     username="USERNAME",
                     password="PASSWORD")

subreddit = reddit.subreddit("wordcloudbot")
for comment in subreddit.stream.comments(skip_existing=True):
    print("received")
    if(comment.body[0:13] == "!wordcloudbot"):
        author = comment.author
        text = ""
        for i in author.comments.new(limit=10000):
            text += " " + i.body
        res = createWordCloud(text, author.name)
        comment.reply("Here is your [wordcloud!]({})".format(res))
    print("done")