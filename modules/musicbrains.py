import musicbrainzngs

def musibrains(string):
    # TODO First revision of the function, that uses search_artists and search_works, could be interesting to get data from recording that have the genres of the song
    # Some interesting/useful links:
    # - https://musicbrainz.org/recording/3fad33de-9748-4b97-9506-3c1ab2f67529
    # - https://wiki.musicbrainz.org/MusicBrainz_API
    # - https://pypi.org/project/musicbrainzngs/
    # - https://python-musicbrainzngs.readthedocs.io/en/v0.7.1/usage/
    # - https://jsonformatter.curiousconcept.com/

    # If you plan to submit data, authenticate
    #musicbrainzngs.auth("user", "password")
    musicbrainzngs.auth("blackhold", "qHu6JXtYzAmia4QvE2zndpjgg")
    
    # Tell musicbrainz what your app is, and how to contact you
    # (this step is required, as per the webservice access rules
    # at http://wiki.musicbrainz.org/XML_Web_Service/Rate_Limiting ) 
    #musicbrainzngs.set_useragent("geosong", "0.1", "pycamp-es2022")
    musicbrainzngs.set_useragent("geosong", "2", "pycamp-es2022")
    
    # If you are connecting to a different server
    #musicbrainzngs.set_hostname("beta.musicbrainz.org")
    
    # clean string
    _song = string
    _song = _song.replace("I used Shazam to discover ","")
    _song = _song.replace("I used @Shazam to discover ","")
    
    # split string
    _song = _song.split(" by ")
    _song_name = _song[0]
    _composer = _song[1]

    # define variables
    _artist_id = None
    _work_id = None
    _genre = []
    
    # search and test artist name
    if _composer[-1:] == ".":
        _composer = _composer[:-1]
   
    #print (f"Searching for artist {_composer}")
    _result = musicbrainzngs.search_artists(artist=_composer, type="group")
    for _artist in _result['artist-list']:
        if _artist['name'] == _composer:
            _artist_id = _artist['id']

            # get artist genres
            _tag_list = _artist['tag-list']
            for _tag in _tag_list:
                _genre.append(_tag['name'])

    # search and test song name
    #print (f"Searching for work/song {_song_name}")
    _result = musicbrainzngs.search_works(_song_name)
    
    for _work in _result['work-list']:
        if _work['title'] == _song_name:
            _artists = _work['artist-relation-list']
            for _artist in _artists:
                if _artist['artist']['id'] == _artist_id and _artist_id != None:
                    _work_id = _work['id']
                    #print ("ID: " + _work['id'])
                    #print ("Title: " + _work['title'])  
                    #print (_work)
                    #print ("-------------------------")
            _recordings = _work['recording-relation-list']
            #for _recording in _recordings:
                #print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                #print (_recording['recording']['id'])
                #_recording = musicbrainzngs.get_recording_by_id(_recording['recording']['id'])
                #print (_recording)
                #print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")


    if _work_id != None:
        #print ("***********************************")
        #_result = musicbrainzngs.get_work_by_id(_work_id)
        #print (_result)
        #print ("*********** GENRES ****************")
        #print (_genre)
        #print ("***********************************")
        _data = {'artist': _composer, 'song': _song_name, 'genre': _genre}
    else:
        _data = None
    
    return _data

# how to use this function (uncomment for testing)
#_song = "I used @Shazam to discover Strange And Beautiful (I'll Put A Spell On You) by Aqualung."
_song = "I used Shazam to discover As It Was by Harry Styles."
_output = musibrains(_song)
print (_output)
