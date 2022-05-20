''' 
to run it:
python -m data_analysis.scraper
'''

import twint
import logging
import time

from util import init_experiments, read_args


# set configuration for twint scrapper
def get_twint_config(args):
    config = twint.Config()
    config.Search = "dogecoin"
    config.Lang = "en"
    config.Limit = args.scraper_limit
    config.Since = "2019-04-29"
    config.Until = "2022-04-29"
    config.Store_json = True
    config.Output = f"{args.output_dir}/twint_dogecoin.json"
    return config    


def main():
    try:
        starttime = time.time()
        args = read_args()
        if args.scraper == "twint":
            logging.info(f"Twitter scrapping with twint is starting...")
            log_dir = init_experiments(args, "..twint_scrapping_experiment")
            config = get_twint_config(args)
            twint.run.Search(config)
        duration = (time.time()-starttime) / 60
        logging.info(f"finished in {duration:.2f} minutes")

    except Exception as e:
        logging.exception(e)


if __name__ == '__main__':
    main()



