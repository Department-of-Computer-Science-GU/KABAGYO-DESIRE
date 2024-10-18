import tweepy
import time

# Twitter API Credentials
consumer_key = "your_consumer_key_here"
consumer_secret = "your_consumer_secret_here"
access_token = "your_access_token_here"
access_token_secret = "your_access_token_secret_here"

# Authenticate with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create the API object
api = tweepy.API(auth)

# List of hashtags to track
hashtags = ["#Python", "#MachineLearning", "#DataScience"]

def get_tweets(query, count=100):
    # Retrieve tweets based on the query
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", tweet_mode='extended').items(count)
    return [tweet.full_text for tweet in tweets]

def retweet_tweets(query, count=50):
    # Retweet tweets matching the query
    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en").items(count)
    for tweet in tweets:
        try:
            api.retweet(tweet.id)
            print(f"Retweeted: {tweet.full_text[:50]}...")
        except tweepy.TweepyException as e:
            print(f"Error retweeting: {e}")

def main():
    log_message = f"\nProcessing hashtags: {', '.join(hashtags)}"
    print(log_message)
    
    while True:
        for hashtag in hashtags:
            recent_tweets = get_tweets(hashtag)
            
            print(f"\nHashtag: {hashtag}")
            print(f"Tweets found: {len(recent_tweets)}")
            
            retweet_tweets(hashtag)
        
        print("\nWaiting for next cycle...")
        time.sleep(60 * 60)  # Wait for 1 hour

if __name__ == "__main__":
    main()
