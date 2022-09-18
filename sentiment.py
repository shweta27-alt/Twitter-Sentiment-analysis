import os


import tweepy
import csv
import re
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from flask import Blueprint, render_template, request



second = Blueprint("second", __name__, static_folder="static", template_folder="template")


@second.route("/tweet")
def sentiment_analyzer():
    return render_template("twitter.html")


class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    # This function first connects to the Tweepy API using API keys
    def DownloadData(self, keyword, tweets):

        # authenticating

        consumerKey = 'Enter the consumer key'
        consumerSecret = 'Enter the secret key'
        accessToken = 'Enter the access token '
        accessTokenSecret = 'Enter the access token secret'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth, wait_on_rate_limit=True)


        # input
        # keyword = input("Enter keyword/tag to search about")
        # tweets = input("Enter how many tweets to search: ")
        tweets = int(tweets)

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=keyword, lang="en").items(tweets)

        # Open/create a file to append data to
        csvFile = open('result.csv', 'a')

        # Use csv writer
        csvWriter = csv.writer(csvFile)

        # creating some variables to store info
        polarity = 0
        positive = 0
        negative = 0
        neutral = 0


        # iterating through tweets fetched
        for tweet in self.tweets:
            # Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            # print (tweet.text.translate(non_bmp_map))    #print tweet's text
            analysis = TextBlob(tweet.text)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 1):
                positive += 1
            elif (analysis.sentiment.polarity < 0 and analysis.sentiment.polarity >-1):
                negative += 1

        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, tweets)
        negative = self.percentage(negative, tweets)
        neutral = self.percentage(neutral, tweets)

        # finding average reaction
        polarity = polarity / tweets

        # printing out data
        #  print("How people are reacting on " + keyword + " by analyzing " + str(tweets) + " tweets.")
        #  print()
        #  print("General Report: ")

        if (polarity == 0):
            htmlpolarity = "Neutral"
        elif (polarity > 0 and polarity < 1):
            htmlpolarity = "Positive"
        elif (polarity > -1 and polarity < 0):
            htmlpolarity = "Negative"

        self.plotPieChart(positive, negative, neutral, keyword, tweets)
        #print(polarity, htmlpolarity)
        return polarity, htmlpolarity, positive,  negative,  neutral, keyword, tweets

    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

        # function to calculate percentage

    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive,  negative, neutral, keyword, tweets):
        fig = plt.figure()
        labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]']
        sizes = [positive,  neutral, negative]
        colors = ['gold', 'red', 'darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')
        plt.tight_layout()
        strFile = r"C:\Users\HP\PycharmProjects\Twitter_sentiment\static\images\plot1.png"
        if os.path.isfile(strFile):
            os.remove(strFile)  # Opt.: os.system("rm "+strFile)
        plt.savefig(strFile)
        plt.show()


@second.route('/sentiment_logic', methods=['POST', 'GET'])
def sentiment_logic():
    keyword = request.form.get('keyword')
    tweets = request.form.get('tweets')
    sa = SentimentAnalysis()
    polarity, htmlpolarity, positive, negative, neutral, keyword1, tweet1 = sa.DownloadData(keyword, tweets)
    return render_template('twitter.html', polarity=polarity, htmlpolarity=htmlpolarity, positive=positive,
                           negative=negative, neutral=neutral, keyword=keyword1, tweets=tweet1)




