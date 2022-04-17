from copy import deepcopy
from collections import Counter
import logging
import os
import json

import musicbrainzngs

logger = logging.getLogger(__name__)


def search_all_recordings(song_title, max_num=1_000):
    recordings = []
    offset = 0

    while len(recordings) < max_num:
        res = musicbrainzngs.search_recordings(
            f'"{song_title}"', limit=100, offset=offset
        )
        if res["recording-list"]:
            recordings.extend(res["recording-list"])
            offset += 100
        else:
            break

    return recordings


def filter_recordings_by_artist(recordings, artist_id):
    for recording in recordings:
        for artist in recording["artist-credit"]:
            try:
                if artist["artist"]["id"] == artist_id:
                    yield recording
                    break
            except TypeError:
                # Needed to avoid some weird parsing errors
                continue


def get_earliest_recording_and_year(recordings):
    possible_earliest_recording = min(
        recordings, key=lambda r: int(r.get("first-release-date", "9999")[:4])
    )
    min_year = int(possible_earliest_recording["first-release-date"][:4])

    # There might be several records with the same year,
    # but we want to retrieve the one with the highest score
    # or the most information
    min_year_recordings = [
        r
        for r in recordings
        if int(r.get("first-release-date", "9999")[:4]) == min_year
    ]

    earliest_recording = max(
        min_year_recordings, key=lambda r: (int(r["ext:score"]), len(r["release-list"]))
    )

    return earliest_recording, min_year


def get_most_likely_genre(recording):
    tags = Counter()
    for tag_dict in recording.get("tag-list", []):
        tags[tag_dict["name"]] += int(tag_dict["count"])

    most_common = tags.most_common()
    if most_common:
        return most_common[0][0]
    else:
        return "unknown"


def get_metadata(song_title, artist_name):
    musicbrainzngs.set_useragent("geosong", "2", "pycamp-es2022")

    logger.debug("Searching artists...")
    related_artists = musicbrainzngs.search_artists(artist=artist_name, type="group")
    chosen_artist = max(
        related_artists["artist-list"], key=lambda a: int(a["ext:score"])
    )

    logger.debug("Searching recordings...")
    recordings = search_all_recordings(song_title)

    # Store in list because I will use them twice
    logger.debug("Filtering recordings...")
    possible_recordings = list(
        filter_recordings_by_artist(recordings, chosen_artist["id"])
    )

    logger.debug("Getting earliest recording...")
    recording, year = get_earliest_recording_and_year(possible_recordings)

    logger.debug("Getting most likely genre...")
    genre = get_most_likely_genre(recording)

    return {
        "artist": chosen_artist["name"],
        "title": recording["title"],
        "year": year,
        "genre": genre,
    }
