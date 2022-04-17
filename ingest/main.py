import logging
import os

import tweepy

from twitter import serialize_tweet, get_tweet_info
from metadata import get_metadata

logger = logging.getLogger(__name__)


def main(bearer_token, maxiter):
    client = tweepy.Client(bearer_token=bearer_token)

    geo_tweets, users, places = get_tweet_info(maxiter=maxiter, client=client)

    for tweet in geo_tweets:
        logger.debug("Serializing tweet")
        t_json = serialize_tweet(tweet, users=users, places=places)
        try:
            t_json["song_metadata"] = get_metadata(
                t_json["song_metadata"]["title"], t_json["song_metadata"]["artist"]
            )
        except:
            # Ignore tweet
            logger.exception(
                "Song metadata retrieval failed, ignoring tweet: %s", tweet
            )
            continue
        else:
            logger.info("Completed: %s", t_json)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logging.getLogger(name="musicbrainzngs").setLevel(level=logging.WARNING)

    bearer_token = os.environ["TWITTER_BEARER_TOKEN"]
    maxiter = 10

    main(bearer_token, maxiter)
