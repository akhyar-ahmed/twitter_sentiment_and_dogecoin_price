''' 
to run it:
python -m data_analysis.scraper
'''

import logging
import json
import time
import nest_asyncio
import datetime as dt
import pandas as pd
import os
import tweepy as tw

from util import init_experiments, read_args

nest_asyncio.apply()

# set configuration for tweepy
def get_tweepy_config(args):
    token_file = "twitter_api_tokens.json"
    path = os.path.join(args.asset_path, token_file)
    asset_file = open(path)
    asset_dict = json.load(asset_file) 
    config = {
        "api_key": asset_dict["Consumer Keys"]["API Key"],
        "api_key_secret": asset_dict["Consumer Keys"]["API Key Secret"],
        "access_token": asset_dict["Authentication Tokens"]["Access Token"],
        "access_token_secret": asset_dict["Authentication Tokens"]["Access Token Secret"],
        "bearer_token": asset_dict["Authentication Tokens"]["Bearer Token"]

    }
    return config


# fetch all tweets using tweepy
def fecth_all_tweepy_tweets(args, api, query):
    # get tweets from the API
    tweets = tw.Cursor(api.search_tweets,
                q=query,
                lang="en").items(200)
    return tweets


# return a dataframe from fetched tweets
def create_tweepy_df(tweepy_tweet_ls, api, log_dir = None, query = None):
    text_ls = []
    created_at = []
    month_ls = []
    year_ls = []
    day_ls = []
    tweet_id_ls = []
    data_src_ls = []
    author_id_ls = []
    author_name_ls = []
    coun = 1
    split = 0
    for tweet in tweepy_tweet_ls:
        text_ls.append(tweet.text)
        year_ls.append(str(tweet.created_at.strftime("%Y")))
        month_ls.append(str(tweet.created_at.strftime("%m")))
        day_ls.append(str(tweet.created_at.strftime("%d")))
        created_at.append(str(tweet.created_at.strftime("%H:%M:%S")))
        tweet_id_ls.append(str(tweet.id))
        data_src_ls.append(str(tweet.source))
        author_id_ls.append(str(tweet.author_id))
        
        # gets the author name
        # if author_id_ls[-1] == None:
        #     user_name = ""
        # else:
        #     user = api.get_user(id = author_id_ls[-1])
        #     user_name = user.name
        user_name = "Nobody"
        author_name_ls.append(user_name)
        print(split, coun)
        if coun%100 == 0:
            time.sleep(40)
        if coun == 500:
            coun = 1
            tweets_dict = {
                "tweet_id": tweet_id_ls,
                "user_id": author_id_ls,
                "user_name": author_name_ls,
                "original_tweet": text_ls,
                "year": year_ls,
                "month": month_ls,
                "day": day_ls,
                "time": created_at,
                "source": data_src_ls
            }
            text_ls = []
            created_at = []
            month_ls = []
            year_ls = []
            day_ls = []
            tweet_id_ls = []
            data_src_ls = []
            author_id_ls = []
            author_name_ls = []
            tweets_df = pd.DataFrame(tweets_dict)
            tweets_df = tweets_df.reset_index(drop=True)
            tweets_df.to_csv(f"{log_dir}/tweepy_tweets_{query.split()[0]}_{split}.csv")
            split += 1
        else:
            coun += 1
    tweets_dict = {
        "tweet_id": tweet_id_ls,
        "user_id": author_id_ls,
        "user_name": author_name_ls,
        "original_tweet": text_ls,
        "year": year_ls,
        "month": month_ls,
        "day": day_ls,
        "time": created_at,
        "source": data_src_ls
    }
    tweets_df = pd.DataFrame(tweets_dict)
    tweets_df = tweets_df.reset_index(drop=True)
    tweets_df.to_csv(f"{log_dir}/tweepy_tweets_{query.split()[0]}_{split}.csv")
    # # show the dataframe
    # print(tweets_df.head())
    return


# authenticate twitter api 
def config_twitter(args):
    twitter_api_config = get_tweepy_config(args)
    # print(json.dumps(api_config, indent = 4))
    try:
        # Authenticate to Twitter
        auth = tw.OAuthHandler(twitter_api_config["api_key"], twitter_api_config["api_key_secret"])
        auth.set_access_token(twitter_api_config["access_token"], twitter_api_config["access_token_secret"])
        client = tw.Client(twitter_api_config["bearer_token"])
        
        # api = tw.API(auth, wait_on_rate_limit = True)
        api = tw.API(auth)
        logging.info(f"Twitter API connected successfully!")
    except Exception as e:
        logging.exception(e)
    return api, client


# the main method
def main():
    try:
        starttime = time.time()
        args = read_args()
        if args.scraper == "tweepy":
            logging.info(f"Twitter scrapping with tweepy is starting...")
            log_dir = init_experiments(args, "..tweepy_experiment")
            api, client = config_twitter(args)
            
            # query = "#covid19 -filter:retweets"
            query = 'from:elonmusk -is:retweet lang:en'
            limit = 100000
            start_time = '2019-01-01T00:00:00Z'
            end_time = '2020-01-01T00:00:00Z
            try:
                # tweets = fecth_all_tweepy_tweets(args, api, query)
                # tweepy_tweet_ls = [i for i in tweets]
                # tweets_df = create_tweepy_df(tweepy_tweet_ls, api)
                # tweets_df.to_csv(f"{log_dir}/tweepy_tweets_{query}.csv")
'
                tweets = tw.Paginator(client.search_all_tweets, query=query,
                                            tweet_fields=['context_annotations', 'created_at', "text", "author_id", "source", "entities"], start_time=start_time, end_time=end_time, max_results=100, ).flatten(limit=limit)
                
                # tweet_df = create_tweepy_df(tweets, api)
                # tweet_df.to_csv(f"{log_dir}/tweepy_tweets_{query.split()[0]}.csv")
                create_tweepy_df(tweets, api, log_dir, query)

                logging.info(f"Tweet scraping using tweepy completed successfully!")
                logging.info(f"All tweets are written into {log_dir}/tweepy_tweets_{query.split()[0]}.csv file!!")
            except Exception as e:
                logging.exception(e)

        duration = (time.time()-starttime) / 60
        logging.info(f"finished in {duration:.2f} minutes")

    except Exception as e:
        logging.exception(e)


# call the main method
if __name__ == '__main__':
    main()



