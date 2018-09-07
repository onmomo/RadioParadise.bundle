import re
from loader import PlaylistReloader

ART = 'art-default.jpg'
ICON = 'icon-default.png'
NAME = 'Radio-Paradise'
STREAM_META = 'https://api.radioparadise.com/api/get_block?bitrate=4&info=true'
PREFIX = '/music/' + NAME.lower()





####################################################################################################
def Start():

	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME
	TrackObject.thumb = R(ICON)
	# only called once
	Log.Debug("loading radio paradise channel")
	Dict['last_played_event'] = ""



####################################################################################################     
@handler(PREFIX, NAME, thumb=ICON, art=ART)
def MainMenu():
	# executed every time the channel is openend
	meta = JSON.ObjectFromURL(url = STREAM_META)
	#artUrl = 'https:'+ meta['image_base'] + meta['song']['0']['cover']
	#Log.Debug("Loading art work from: %s", artUrl)
	#ObjectContainer.art = artUrl
	Log.Debug("Streaming RP flac from %s", meta['url'])
	oc = ObjectContainer()
	artist = meta['artist']
	album = meta['album']
	oc.add(CreateTrackObject(url=meta['url'] + '?src=alexa', length=meta['length'], title=NAME, artist=artist, album=album))
	
	Dict['stream_length'] = int(float(meta['length']) * 1000)
	#Dict['stream_total_songs'] = 2
	#Dict['stream_last_song'] = 0
	
	PlaylistReloader()
	
	#Thread.Create(Stupid())
	return oc

####################################################################################################
		


####################################################################################################
@route(PREFIX + '/createTrackObject', include_container = bool)
def CreateTrackObject(url, length, title, artist, album, include_container=False, **kwargs):

	track_object = TrackObject(
		artist = artist,
		album = album,
		key = Callback(CreateTrackObject, url=url, length=length, title=title, artist=artist, album=album, include_container=True),
		rating_key = url,			
		items = [
			MediaObject(
				parts = [
					PartObject(key=Callback(PlayAudio, url=url, ext='flac'))
				],
				duration = int(float(length) * 1000),			
				container = Container.FLAC,
				audio_codec = AudioCodec.FLAC,
				audio_channels = 2
			)
		]
	)

	if include_container:
		return ObjectContainer(objects=[track_object])
	else:
		return track_object


####################################################################################################
@route(PREFIX + '/playAudio')
def PlayAudio(url):

	return Redirect(url)
