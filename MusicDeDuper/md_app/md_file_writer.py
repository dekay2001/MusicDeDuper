import os
import json


class musicStorageOutPut(object):
    def __init__(self):
        self.default_write_directory = os.path.dirname(__file__)
        self.default_name = 'music_data.js'

    def load_music_data_from_file(self, music_file=None):
        """Returns a dictionary from the music file
        specified.  Defaults to music_data.js if not."""
        if music_file is None:
            music_file =  os.path.join(self.default_write_directory, self.default_name )
        with open(music_file) as mf:
            d = json.load(mf) 
        return d   

    def write_to_file(self, music_storage):
        """From the list we will generate some json
        that will be stored in a file.
        music_storage is a dict."""
        music_data_file = os.path.join(self.default_write_directory, self.default_name )
        if os.path.isfile(music_data_file):
            print('File path already exists {}'.format(music_data_file))
        else:
            print( 'Writing File:  {}'.format(music_data_file) )
            #json.loads(music_storage)
            with open(music_data_file, 'w') as outfile:
                json.dump(music_storage, outfile, separators=(',\n', ':'))
