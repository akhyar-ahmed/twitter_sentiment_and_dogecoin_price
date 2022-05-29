''' 
to run it:
python -m data_analysis.scraper
'''

import src.twint.twint as twint
import logging
import time
import nest_asyncio
import datetime as dt
import pandas as pd

from util import init_experiments, read_args
from twitterscraper import query_tweets
from twitterscraper.query import query_tweets_from_user

nest_asyncio.apply()

# set configuration for twint scrapper
def get_twint_config(args, log_dir):
    config = twint.Config()
    config.Username = "elonmask"
    config.Search = ["DOGE", "dogecoin", "DOGECOIN", "Dogecoin", "Crypto", "crypto"]
    config.Limit = args.scraper_limit
    config.Lang = "en"
    config.Since = "2019-01-01"
    config.Until = "2022-04-01"
    config.Store_json = True
    config.Output = f"{log_dir}/twint_dogecoin.json"
    return config    


# set configuration for twitterscraper
def get_twitterscraper_config(args):
    config = {
        "b_date": dt.date(2019,1,1),
        "e_date": dt.date(2022,1,1),
        "limit": args.scraper_limit,
        "language": "english"
    }
    return config


def main():
    try:
        starttime = time.time()
        args = read_args()
        if args.scraper == "twint":
            logging.info(f"Twitter scrapping with twint is starting...")
            log_dir = init_experiments(args, "..twint_scraping_experiment")
            config = get_twint_config(args, log_dir)
            twint.run.Search(config)
        elif args.scraper == "twitterscraper":
            logging.info(f"Twitter scrapping with twitterscraper is starting...")
            log_dir = init_experiments(args, "..twitterscraping_experiment")
            config = get_twitterscraper_config(args)
            
            query = "DOGE"
            user = "elonmask"
            # tweets = query_tweets_from_user(user)
            tweets = query_tweets(query)

            df = pd.DataFrame(t.__dict__ for t in tweets)
            df.to_csv(f"{log_dir}/twitterscraper_dogecoin.csv")
        elif args.scraper == "tweepy":
            logging.info(f"Twitter scrapping with tweepy is starting...")
            log_dir = init_experiments(args, "..tweepy_experiment")
            config = get_tweepy_config(args)

            df = pd.DataFrame(t.__dict__ for t in tweets)
            df.to_csv(f"{log_dir}/twitterscraper_dogecoin.csv")

        duration = (time.time()-starttime) / 60
        logging.info(f"finished in {duration:.2f} minutes")

    except Exception as e:
        logging.exception(e)


if __name__ == '__main__':
    main()



