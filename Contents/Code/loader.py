import os

####################################################################################################
STREAM_META = 'https://api.radioparadise.com/api/get_block?bitrate=4&info=true'
####################################################################################################

def PlaylistReloader():    
    global scanthread

    Log.Debug("receiving metadata from url %s ...", STREAM_META)
    meta = JSON.ObjectFromURL(url = STREAM_META)
    event = meta['event']
    # check if event metadata is not already set
    if (Dict['last_played_event'] != event):
        songs = meta['song']
        for songIdx in songs:
            song = songs[str(songIdx)]
            # find the currently playing event / song and set its metadata
            if (song['event'] == event):                
                Log.Debug("loading new metadata for song / event %s ...", event)
                artUrl = 'https:'+ meta['image_base'] + song['cover']
                Log.Debug("Loading new song art work from: %s", artUrl)
                ObjectContainer.art = artUrl
                ObjectContainer.title1 = song['title'] + ' - ' + song['artist']
                #ObjectContainer.title2 = 'test'
                TrackObject.thumb = artUrl
                TrackObject.album = song['album']
                TrackObject.title = song['title']                
                TrackObject.source_title = 'Radio Paradise'
                TrackObject.artist = song['artist']
                TrackObject.rating = str(song['rating'])
                TrackObject.duration = str(song['duration'])

                Dict['last_played_event'] = event
                
                #Thread.Sleep(int(meta['song'][str(songIdx)]['duration']) / 1000)        
    else:
        Log.Debug("No need to reload song metadata, event: '%s' is still playing", event)
    # Wait with metadata reload untill song end has reached
    scanthread = Thread.CreateTimer(float(10), PlaylistReloader)


####################################################################################################
try:
    any
except NameError:
    def any(s):
        for v in s:
            if v:
                return True
        return False