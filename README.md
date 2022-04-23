# GeoSong

[TBC]

## Future

Example of geolocated search:

```python
client.search_all_tweets(
    # 'Shazam place:"Madrid"',
    'Shazam point_radius:[-3.704089099384552 40.426892971504195 25km]',
    max_results=100,
    tweet_fields=["author_id", "created_at", "geo"],
    user_fields=["username"],
    place_fields=["geo", "name", "country"],
    expansions=["author_id", "geo.place_id"],
    start_time="2019-01-01T00:00:00Z",
    end_time="2019-06-01T00:00:00Z",  # Needed to retrieve old tweets!
    # next_token=next_token,
)
```

## Development

To install the dependencies:

```
(.venv) $ pip install -r requirements.txt
```

To add a new dependency:

```
(.venv) $ pip install pip-tools
(.venv) $ echo "pandas" >> requirements.in
(.venv) $ pip-compile
```

