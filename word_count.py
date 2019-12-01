#==============================================================================
# Importing
# runfile('word_count.py', args='test.txt')

import argparse
import requests
import string
import re
import matplotlib.pyplot as plt
import numpy as np
import time

#==============================================================================  

class artist_obj:
    """
    Object to represent artist and associated lyric data gather through MusicBrainz and lyrics.ovh APIs
    INs: Name, the name of the artist. This will be used to search MusicBrainz for the artist's songs
    """
    def __init__(self, name):
        self.name = name     
        
    def get_mb_id(self):
        """
        Function for finding the MusicBrainz ID for the artist. Ensures only relavent songs are retrieved
        INs: None (uses self.name)
        """
        mb_url = 'http://musicbrainz.org/ws/2/artist/?query='+self.name+'&fmt=json' #uses artist name to search MusicBrainz
        self.id = requests.get(mb_url).json()['artists'][0]['id'] # gets artist ID to prevent ambiguity
        return self.id
    
    def get_song_names(self, num):
        """
        Function for finding songs by the artist on MusicBrainz
        INs: num, number of songs to retrieve in multiples of 50
        """
        artist_id = self.get_mb_id() # gets music brainz ID
        self.titles = []
        for i in range(num): # iterates through 50s to retrieve user specified number of songs.
            time.sleep(1) # prevents MusicBrainz denying query due to too many queries per second
            mb_url = 'https://musicbrainz.org/ws/2/recording/?artist='+ artist_id +'&offset='+str(50*i)+'&limit=50&fmt=json' #API url
            self.releases = requests.get(mb_url).json() # retrieve data from music brainz
            for i, release in enumerate(self.releases['recordings']):
                self.titles.append(release['title'].lower()) # iterates through releases and saves titles
            self.titles = list(set(self.titles)) #removes duplicate titles
        self.mb_url = mb_url
        print('Found ',len(self.titles), ' songs on MusicBrainz by ', self.name, '\nQuerying lyrics on lyrics.ovh... ')
        return self.titles
    
    def get_lyrics_from_titles(self, num):
        """
        Function for finding lyrics for retrieved song titles
        INs: num, number of songs to retrieve in multiples of 50 (only used if self.get_song_names hasn't been run yet)
        """
        if not(hasattr(self, 'titles')):
            self.titles = self.get_song_names(num) # checks song titles have been retrieved
        base_url = 'https://api.lyrics.ovh/v1/'+self.name+'/'
        self.lyrics_data = []
        for i, song in enumerate(self.titles):
            ovh_url = base_url+song # assembles url for API
            try:
                lyrics = requests.get(ovh_url).json() # retrieves lyrics for that song.
                self.lyrics_data.append(lyrics)
            except:
                pass
        if len(self.lyrics_data) == 0:
            print('Lyrics.ovh had none of these songs listed')
        return self.lyrics_data
    
    def process_lyric_data(self):
        """
        Function for processing retrieved lyrics into word counts
        INs:none
        """
        self.word_counts = []
        for i, song in enumerate(self.lyrics_data):
            try:
                if len(song['lyrics']) > 3:
                    lyrics = song['lyrics'].translate(str.maketrans('', '', string.punctuation + '’')).lower()
                    re.sub("[\(\[].*?[\)\]]", "", lyrics)
                    lyrics = ' '.join(lyrics).split()
                    self.word_counts.append(len(lyrics))
            except:
                pass # This occurs if retrieved song from musicbrainz is not in lyric database so song is ignored
        print('Lyrics.ovh had lyrics for ', len(self.word_counts),' of those songs')
        self.word_counts = np.asarray(self.word_counts)
        return self.word_counts
    
#==============================================================================
            
if __name__ == '__main__':
    #==========================================================================
    #========  parse command line arguments 
    parser = argparse.ArgumentParser(description='Compress text')
    parser.add_argument('infile')
    parser.add_argument('-num')
    args = parser.parse_args()
    path = args.infile
    num = int(args.num)
    #==========================================================================
    #========  Import queries

    with open(path) as input_file:
        artists = input_file.read().splitlines()
    #==========================================================================
    #========  Execute queries       
    for i, artist in enumerate(artists):
        artist = artist_obj(artist)
        lyrics = artist.get_lyrics_from_titles(num)
        counts = artist.process_lyric_data()
        #==========================================================================
        #========  Plot data  
        plt.ion()
        plt.figure()
        result = plt.hist(counts, bins=20, color='c', edgecolor='k', alpha=0.65)
        plt.title('Word counts for songs by artist: '+ artist.name)
        plt.axvline(counts.mean(), color='k', linestyle='dashed', linewidth=1)
        min_ylim, max_ylim = plt.ylim()
        plt.text(counts.mean()+0.1, max_ylim*0.9, 'Mean: {:.2f}'.format(counts.mean()))
        plt.text(counts.mean()+0.1, max_ylim*0.8, 'Std. Dev.: {:.2f}'.format(counts.std()))
        
        plt.axvline(counts.max(), color='k', linestyle='dashed', linewidth=1)
        plt.text(counts.max()-0.4, max_ylim*0.7, 'Max: {:.2f}'.format(counts.max()))
        
        plt.axvline(counts.min(), color='k', linestyle='dashed', linewidth=1)
        plt.text(counts.min()+0.1, max_ylim*0.7, 'Min: {:.2f}'.format(counts.min()))
        
        
        
    
  