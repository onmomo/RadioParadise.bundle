ART = 'art-default.jpg'
ICON = 'icon-default.png'
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
	artUrl = 'https:'+ meta['image_base'] + meta['song']['0']['cover']
	Log.Debug("Loading art work from: %s", artUrl)
	ObjectContainer.art = artUrl
	Log.Debug("Streaming RP flac from %s", meta['url'])
	oc = ObjectContainer()
	oc.add(CreateTrackObject(url=meta['url'] + '?src=alexa', length=(meta['length']), title=NAME))
	

	return oc

####################################################################################################
def CreateTrackObject(url, length, title, include_container=False, **kwargs):

	track_object = TrackObject(
		key = Callback(CreateTrackObject, url=url, length=length, title=title, include_container=True),
		rating_key = url,
		title = title,			
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
def PlayAudio(url):

	return Redirect(url)
