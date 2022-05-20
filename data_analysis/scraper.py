''' 
to run it:
python -m data_analysis.scraper
'''

import src.twint.twint as twint
import logging
import time
import nest_asyncio

from util import init_experiments, read_args


# set configuration for twint scrapper
def get_twint_config(args, log_dir):
    nest_asyncio.apply()
    config = twint.Config()
    config.Username = "elonmask"
    config.Search = ["dogecoin", "crypto", "DOGECOIN", "Dogecoin", "Crypto", "btc"]
    config.Limit = args.scraper_limit
    config.Lang = "en"
    config.Since = "2020-01-01"
    # config.Until = "2022-04-29"
    config.Store_json = True
    config.Output = f"{log_dir}/twint_dogecoin.json"
    return config    


def main():
    try:
        starttime = time.time()
        args = read_args()
        if args.scraper == "twint":
            logging.info(f"Twitter scrapping with twint is starting...")
            log_dir = init_experiments(args, "..twint_scrapping_experiment")
            config = get_twint_config(args, log_dir)
            twint.run.Search(config)
        duration = (time.time()-starttime) / 60
        logging.info(f"finished in {duration:.2f} minutes")

    except Exception as e:
        logging.exception(e)


if __name__ == '__main__':
    main()



