import musicbrainzngs

def musibrains(string):
    # If you plan to submit data, authenticate
    #musicbrainzngs.auth("user", "password")
    
    # Tell musicbrainz what your app is, and how to contact you
    # (this step is required, as per the webservice access rules
    # at http://wiki.musicbrainz.org/XML_Web_Service/Rate_Limiting ) 
    musicbrainzngs.set_useragent("geosong", "0.1", "pycamp-es2022")
    
    # If you are connecting to a different server
    #musicbrainzngs.set_hostname("beta.musicbrainz.org")
    
    #_song = "I used @Shazam to discover Strange And Beautiful (I'll Put A Spell On You) by Aqualung."
    #_song = "I used Shazam to discover As It Was by Harry Styles."
    _song = string
    
    # clean string
    _song = _song.replace("I used Shazam to discover ","")
    _song = _song.replace("I used @Shazam to discover ","")
    
    # split string
    _song = _song.split(" by ")
    _song_name = _song[0]
    _composer = _song[1]
    _artist_id = None
    _work_id = None
    _genre = []
    
    # search and test artist name
    if _composer[-1:] == ".":
        _composer = _composer[:-1]
    
    #print (f"Searching for artist {_composer}")
    _result = musicbrainzngs.search_artists(_composer)
    
    _artists = _result['artist-list']
    for _artist in _artists:
        if _artist['name'] == _composer:
            _artist_id = _artist['id']
            #print ("ID: " + _artist['id'])
            #print ("Name: " + _artist['name'])
            #print (_artist)
            #print ("-------------------------")
    
            # get genre
            _tag_list = _artist['tag-list']
            for _tag in _tag_list:
                _genre.append(_tag['name'])
    
    #print ("***********************************")
    # search and test song name
    #print (f"Searching for work/song {_song_name}")
    _result = musicbrainzngs.search_works(_song_name)
    
    _works = _result['work-list']
    for _work in _works:
        if _work['title'] == _song_name:
            _artists = _work['artist-relation-list']
            for _artist in _artists:
                if _artist['artist']['id'] == _artist_id and _artist_id != None:
                    _work_id = _work['id']
                    #print ("ID: " + _work['id'])
                    #print ("Title: " + _work['title'])  
                    #print (_work)
                    #print ("-------------------------")
    
    
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
    
    # TODO search through it
    #print ("RAMSTEIN")
    #_recording = "3fad33de-9748-4b97-9506-3c1ab2f67529"
    
    return _data

# how to use this function (uncomment for testing)
#_song = "I used @Shazam to discover Strange And Beautiful (I'll Put A Spell On You) by Aqualung."
#_song = "I used Shazam to discover As It Was by Harry Styles."
#_output = musibrains(_song)
#print (_output)
