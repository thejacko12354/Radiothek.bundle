import sets

NAME = 'Radiothek'

ART = 'art-default.jpg'
ICON = 'icon-default.jpg'

STATIONS = 'stations.json'

####################################################################################################

def Start():
	Plugin.AddPrefixHandler('/music/radiothek', MainMenu, NAME, ICON, ART)
	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
	Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
	MediaContainer.title1 = NAME
	MediaContainer.viewGroup = "List"
	MediaContainer.art = R(ART)

def LoadData():
	userdata = Resource.Load(STATIONS)
	return JSON.ObjectFromString(userdata)
		
def MainMenu():
	Dict['stations'] = LoadData()
	stations = Dict['stations']
	stations.sort()
	dir = MediaContainer(viewGroup="List", noCache=True)
	dir.Append(Function(DirectoryItem(ListStations, 'Alle auflisten', thumb=R(ICON)), stations=stations))
	dir.Append(Function(DirectoryItem(ListStationsSub, 'Nach Land auflisten', thumb=R(ICON)), stations=stations, listStationsBy='country'))
	dir.Append(Function(DirectoryItem(ListStationsSub, 'Nach Genre auflisten', thumb=R(ICON)), stations=stations, listStationsBy='genre'))
	return dir

def ListStationsSub(sender, stations, listStationsBy=''):
	dir = MediaContainer(viewGroup="List", noCache=True)
	Log('listStationsBy: '+listStationsBy)
	listStationsByItemList = []
	for station in stations:
		for listStationsByItem in station[listStationsBy]:
			listStationsByItemList.append(listStationsByItem)
	listStationsByItemList = list(set(listStationsByItemList))
	listStationsByItemList.sort()
	for listStationsByItemS in listStationsByItemList:
		dir.Append(Function(DirectoryItem(ListStations, listStationsByItemS, thumb=R(ICON)), stations=stations, listStationsBy=listStationsBy, listStationsTerm=listStationsByItemS))
	return dir

def ListStations(sender, stations, listStationsBy='', listStationsTerm=''):
	dir = MediaContainer(viewGroup="List", noCache=True)
	for station in stations:
		Log('title: '+station['title']+' | icon: '+station['icon']+' | art: '+station['art'])
		if listStationsTerm != '':
			if listStationsTerm in station[listStationsBy]:
				if len(station['link']) > 1:
					dir.Append(Function(DirectoryItem(StationSub, station['title'], thumb=R(station['icon']), art=R(station['art'])), station=station))
				else:
					dir.Append(TrackItem(key=station['link'][0], title=station['title'], thumb=R(station['icon']), art=R(station['art'])))
		else:
			if len(station['link']) > 1:
				dir.Append(Function(DirectoryItem(StationSub, station['title'], thumb=R(station['icon']), art=R(station['art'])), station=station))
			else:
				dir.Append(TrackItem(key=station['link'][0], title=station['title'], thumb=R(station['icon']), art=R(station['art'])))
	return dir

def StationSub(sender, station):
	dir = MediaContainer(title2=station['title'], viewGroup="List", noCache=True)
	for url in station['link']:
		dir.Append(TrackItem(key=url[1], title=url[0], thumb=R(station['icon']), art=R(station['art'])))
	return dir
	