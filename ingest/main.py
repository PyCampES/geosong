import logging
import os
import requests

import tweepy

from twitter import serialize_tweet, get_tweet_info
from metadata import get_metadata

logger = logging.getLogger(__name__)


def main(api_url, bearer_token, maxiter):
    client = tweepy.Client(bearer_token=bearer_token)

    for geo_tweets, users, places in get_tweet_info(maxiter=maxiter, client=client):
        for tweet in geo_tweets:
            logger.debug("Serializing tweet")
            try:
                t_json = serialize_tweet(tweet, users=users, places=places)
            except:
                logger.exception(
                    "Cannot extract song properties, ignoring: %s", tweet.text
                )
                continue

            try:
                t_json["song_metadata"] = get_metadata(
                    t_json["song_metadata"]["title"], t_json["song_metadata"]["artist"]
                )
            except:
                logger.exception(
                    "Song metadata retrieval failed, setting to unknown: %s", tweet
                )
                t_json["song_metadata"]["year"] = -1
                t_json["song_metadata"]["genre"] = "unknown"
            else:
                logger.info("Completed: %s", t_json)

            response = requests.post(api_url + "/geosong/", json=t_json)
            if response.ok:
                logger.info("Post to geosong successful: %s", response.status_code)
            else:
                logger.error("Post to geosong failed: %s", response.status_code)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logging.getLogger(name="musicbrainzngs").setLevel(level=logging.WARNING)

    api_url = os.environ["GEOSONGS_API_URL"].rstrip("/")
    bearer_token = os.environ["TWITTER_BEARER_TOKEN"]
    maxiter = 1_000

    main(api_url, bearer_token, maxiter)
