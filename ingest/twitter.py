from copy import deepcopy
import logging
import os
import re
import json

import tweepy

logger = logging.getLogger(__name__)

shazam_pattern = re.compile(
    r".*I used [@#]?Shazam to discover (?P<title>.*) by (?P<artist>.*)\. https.*"
)


def get_geom(place_id, *, places):
    geom = deepcopy(places[place_id].geo)
    return geom


def get_username(user_id, *, users):
    user = users[user_id]
    return user.username


def get_song_attributes(text):
    match = shazam_pattern.search(text)
    if not match:
        raise ValueError("Cannot retrieve metadata")

    return match.groupdict()


def get_tweet_info(maxiter=100, query="I used Shazam", *, client):
    next_token = None

    for iteration in range(maxiter):
        geo_tweets = []

        users = {}
        places = {}

        resp = client.search_recent_tweets(
            query,
            max_results=100,  # Maximum allowed
            tweet_fields=["author_id", "created_at", "geo"],
            user_fields=["username"],
            place_fields=["geo", "name", "country"],
            expansions=["author_id", "geo.place_id"],
            next_token=next_token,
        )

        geo_tweets = [t for t in resp.data if t.geo]

        logger.info("Iteration: %d", iteration)
        logger.debug("Length of geo tweets: %d", len(geo_tweets))

        users = {u.id: u for u in resp.includes.get("users", [])}
        places = {p.id: p for p in resp.includes.get("places", [])}

        if "next_token" in resp.meta:
            next_token = resp.meta["next_token"]
        else:
            break

        yield geo_tweets, users, places


def serialize_tweet(tweet, *, users, places):
    username = f"@{get_username(tweet.author_id, users=users)}"
    geom = get_geom(tweet.geo["place_id"], places=places)
    song_metadata = get_song_attributes(tweet.text)

    tweet = {
        "date": tweet.created_at.isoformat(),
        "song_metadata": song_metadata,
        "username": username,
        "bbox": geom["bbox"],
    }
    if "geometry" in geom:
        tweet["point"] = geom["geometry"]

    return tweet
