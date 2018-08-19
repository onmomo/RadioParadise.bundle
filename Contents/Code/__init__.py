ART = 'art-default.jpg'
ICON = 'icon-default.jpg'
NAME = 'Radio Paradise'
STREAM_META = 'https://api.radioparadise.com/api/get_block?bitrate=4&info=true'

####################################################################################################
def Start():

	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME
	TrackObject.thumb = R(ICON)

####################################################################################################     
@handler('/music/radioparadise', NAME, thumb=ICON, art=ART)
def MainMenu():

	meta = JSON.ObjectFromURL(url = STREAM_META)
	Log.Debug(meta['url'])
	oc = ObjectContainer()
	oc.add(CreateTrackObject(url=meta['url'] + '?src=alexa', parts = meta['song'], title=NAME))

	return oc

####################################################################################################
def CreateTrackObject(url, parts, title, include_container=False, **kwargs):

	track_object = TrackObject(
		key = Callback(CreateTrackObject, url=url, parts = parts, title=title, include_container=True),
		rating_key = url,
		title = title,
		items = [
			MediaObject(
				parts = getParts(parts),
				container = Container.FLAC,
				bitrate = 900,
				audio_codec = AudioCodec.FLAC,
				audio_channels = 2
			)
		]
	)

	if include_container:
		return ObjectContainer(objects=[track_object])
	else:
		return track_object


def getParts(songs):
	def toPartObject(songJson):
  		songsPart = PartObject(key='https://apps.radioparadise.com/blocks/chan/0/4/' + songJson['event'] + '.flac', duration = songJson['duration'])
		Log.Debug(songsPart.key)
		Log.Debug(songsPart.duration)
		return songsPart

	parts = map(toPartObject, songs.values())
	Log.Debug(parts)
	return parts[0]

####################################################################################################
def PlayAudio(url):

	return Redirect(url)
