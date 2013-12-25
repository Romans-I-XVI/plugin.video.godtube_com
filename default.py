import urllib,urllib2,re,xbmcplugin,xbmcgui,os,xbmcaddon,sys,xbmcvfs
dbg = True
try:
	import StorageServer
	cache = StorageServer.StorageServer("GodTube")
except:
	import storageserverdummy as StorageServer
	cache = StorageServer.StorageServer("GodTube")

settings = xbmcaddon.Addon( id = 'plugin.video.itbn_org' )
next_thumb = os.path.join( settings.getAddonInfo( 'path' ), 'resources', 'media', 'nextpage.png' )
previous_thumb = os.path.join( settings.getAddonInfo( 'path' ), 'resources', 'media', 'previouspage.png' )
search_thumb = os.path.join( settings.getAddonInfo( 'path' ), 'resources', 'media', 'search.png' )
main_menu_thumb = os.path.join( settings.getAddonInfo( 'path' ), 'resources', 'media', 'main_menu.png' )
live_thumb = os.path.join( settings.getAddonInfo( 'path' ), 'resources', 'media', 'live.png' )
movies_thumb = os.path.join( settings.getAddonInfo( 'path' ), 'resources', 'media', 'movies.png' )
base_url='http://www.godtube.com'

##################################################################################################################################

def MAIN():
	addDir('Explore GodTube',base_url,3, search_thumb)
        addDir('Search',base_url,2, search_thumb)
	if 1==1:
                xbmc.executebuiltin('Container.SetViewMode(50)')

##################################################################################################################################
        
def ADDLINKS(url):
	if search_function == 1:
        	keyboard = xbmc.Keyboard('', '')
        	keyboard.doModal()
        if search_function == 0 or keyboard.isConfirmed() and keyboard.getText():
		if search_function == 1:
			search_list=[]
			search_hist = cache.get('Search')
			try:
                		search_list = eval(search_hist)
			except:
				search_list.insert(0, search_hist)
			search_string = keyboard.getText().replace(" ","+")
                	content = url+search_string
			try:			
				if search_string not in search_list:
					search_list.insert(0, search_string)
				if len(search_list) > 12:
                			del search_list[12]
        			cache.set('Search', str(search_list))
			except:
				pass
		else:
			content = url
                req = urllib2.Request(content)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
#		match=re.compile('<img src="http://cdn.salemweb.net/godtube/.+?/.+?/.+?/(.+?).jpg".+?mediakey=').findall(link)
		name=re.compile('<a class="image" title="(.+?)"').findall(link)
		try:
			name[0]
			name=unique(name)
		except:
			name=re.compile('class="name".+?>(.+?)</a>').findall(link)
#		date=re.compile('<span class="links relativeTimespan">(.+?)T').findall(link)
#		description=re.compile('<span class="description">(.+?)</span>').findall(link)
		thumbnail=re.compile('<img src="(.+?)".+?mediakey=').findall(link)
		thumbnail=unique(thumbnail)
		nextpage=re.compile('</ul></div><a href="(.+?)".+?<span>Next</span>').findall(link)
		xbmc.log('blah'+str(thumbnail))
		try:
			nextpage=nextpage[0]
			nextpage=nextpage.replace('&amp;','&')
			nextpage=nextpage.replace(' ','+')
		except:
			pass
		mylist=zip((name),(thumbnail))
		for name,thumbnail in mylist:
			if "_" in thumbnail:
				url = re.compile('(.+?_.+?)_').findall(thumbnail)
			if "-" in thumbnail:
				url = re.compile('(.+?)-').findall(thumbnail)
			url = url[0]				
			try:
  				urllib2.urlopen(urllib2.Request(url+'.mp4'))
				url = url+'.mp4'
			except:
				url=url+'.flv'
			if "/resource/user/profile" not in thumbnail:
                        	addLink(name,url,thumbnail)
                if nextpage:
                        addDir('More',nextpage,1,next_thumb)
		if settings.getSetting("thumbnailviewmode") == 'true':        
			if 1==1:
                		xbmc.executebuiltin('Container.SetViewMode(500)')
		if settings.getSetting("thumbnailviewmode") == 'false':
			if 1==1:
				xbmc.executebuiltin('Container.SetViewMode(50)')
        else:
		PREVIOUS()


##############################################################################################################

def Search(url):
	search_list=[]
	search_hist = cache.get('Search')
	try:
                search_list = eval(search_hist)
	except:
		search_list.insert(0, search_hist)	
        addDir('Search...',base_url+'/search/?q=',1, search_thumb, search_function=1)
	try:
		for name in search_list:
			title = name.replace('+',' ')
			addDir(title,base_url+'/search/?q='+str(name),1, search_thumb, search_function=0)
	except:
		pass		
	if 1==1:
                xbmc.executebuiltin('Container.SetViewMode(50)')	

##############################################################################################################

def Categories(url):
	addDir('Artist Directory',base_url+'/artists-directory/',4,'')
	addDir('Music Videos',base_url+'/music-videos/',1,'')	
	addDir('Ministry Videos',base_url+'/ministry-videos/',1,'')
	addDir('Inspirational Videos',base_url+'/inspirational-videos/',1,'')
	addDir('Comedy Videos',base_url+'/comedy-videos/',1,'')
	addDir('Cutes Videos',base_url+'/cute-videos/',1,'')
	addDir('Movies',base_url+'/movies/',1,'')
	addDir('Sermons',base_url+'/sermon-videos/',1,'')
	addDir('Spanish',base_url+'/espa%C3%B1ol-videos/',1,'')
	if 1==1:
                xbmc.executebuiltin('Container.SetViewMode(50)')

def ArtistDirectory(url):
	req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	match=re.compile('<a href="http://www.godtube.com/artist/(.+?)">').findall(link)
	for artist in match:
		title=artist.replace('-',' ')
		title=title.replace('/','')
		addDir(title,base_url+'/artist/'+artist,1,'')
	

##############################################################################################################

def unique(a):
    seen = set()
    return [seen.add(x) or x for x in a if x not in seen]
               
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

##################################################################################################################################

def PREVIOUS():
	xbmc.executebuiltin('Action(Back)')

##################################################################################################################################
	

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

##################################################################################################################################

def addDir(name,url,mode,iconimage,search_function=0):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&search_function="+urllib.quote_plus(str(search_function))
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

##################################################################################################################################
        
              
params=get_params()
url=None
name=None
mode=None
search_function=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        search_function=int(params["search_function"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        MAIN()
       
elif mode==1:
        print ""+url
        ADDLINKS(url)
        
elif mode==2:
        print ""+url
        Search(url)

elif mode==3:
        print ""+url
        Categories(url)

elif mode==4:
        print ""+url
        ArtistDirectory(url)

elif mode==5:
        print ""+url
        PROGRAMS(url)

elif mode==6:
        print ""+url
        RECENT(url)

elif mode==7:
        print ""+url
        LIVE(url)

elif mode==8:
        print ""+url
        SEARCH(url)

elif mode==9:
        print ""+url
        AIRDATE(url)

elif mode==10:
        print ""+url
        MOVIES(url)
elif mode==11:
        print ""+url
        PREVIOUS()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
