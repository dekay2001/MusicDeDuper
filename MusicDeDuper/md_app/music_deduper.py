import sys
import os
import winsound
import shutil

from difflib import SequenceMatcher

import md_file_writer

def get_attention():
    winsound.Beep(250, 1000)
    winsound.Beep(1000, 750)
    winsound.Beep(500, 1000)

class similarNames(object):
    def __init__(self, name1, name2):
        self._name1 = name1
        self._name2 = name2

    def get_name1(self):
        return self._name1

    def get_name2(self):
        return self._name2

    def set_name1(self, name):
        self._name1 = name

    def set_name2(self, name):
        self._name2 = name

    def toDict(self):
        return {'Name1':self._name1,
        'Name2':self._name2}

    name1 = property(get_name1, set_name1)
    name2 = property(get_name2, set_name2)

class musicDeDuper(object):
    def __init__(self, default_music_folder= "c:\\users\\dan\\music"):
        self.music_folder = default_music_folder
        copy_counter = 1
        while os.path.exists('{}_copy({})'.format(default_music_folder, copy_counter)):
            copy_counter +=1
        self.target_music_folder = '{}_copy({})'.format(default_music_folder, copy_counter)

    def get_copy_to_mappings(self, target_folder=None):
        """Generates a mapping from music_data.js
        to the target folder, that contains all the
        files that will be copied and their final
        destination folder"""
        if target_folder is None:
            target_folder = self.target_music_folder
        all_music_files = self.get_all_files_from_folder()
        d = md.load_file_data_dict()
        similar_dirs = d['Similar_Directories']
        all_files_info = d['Similar_Files']
        artist_dir_override_count = 0
        current_artist_dir_count = 0
        skipped_files = []
        copy_info = [] # tuples with (source directory, target directory)
        new_artist_dirs = set()
        for sd in similar_dirs:
            current_artist_dir_count += len(sd['similar_paths'])
            for p in sd['similar_paths']:
                files_in_directory = self.get_all_files_from_folder(music_folder=p)
                # use_path_override is the artist folder.
                if sd['use_path_override'] is not None:
                    # Generate new paths for each of the files we want to copy,
                    # utilizing the override folder.
                    artist_dir_override_count +=1
                    for mf in files_in_directory:
                        if self.check_to_keep_file(mf,all_files_info):
                            new_artist_dirs.add(sd['use_path_override'])
                            left, right = os.path.split(sd['use_path_override'])
                            # TargetFolder + Override Folder Name + Remainder Path
                            # Example:  C:\TargetMusicPath\OverrideFolder\RemainingFilePath\file.mp3
                            new_path = '{}{}'.format(os.path.join(target_folder, right), mf[len(p):])
                            copy_info.append((mf,new_path))
                        else:
                            skipped_files.append(mf)
                            print('Not keeping file:  {}'.format(mf))
                else:
                    # Generate new paths for each of the files we want to copy.
                    # The artist folder in this circumstance will not be overriden.
                    new_artist_dirs.add(p)
                    for mf in files_in_directory:
                        if self.check_to_keep_file(mf,all_files_info):
                            new_path = '{}{}'.format(target_folder,mf[len(self.music_folder):])
                            copy_info.append((mf,new_path))
                        else:
                            skipped_files.append(mf)
                            print('Not keeping file:  {}'.format(mf))
        print ('********Files Will Be Skipped********\n{}'.format(skipped_files))
        print ('{} artist folders in current music folder'.format(current_artist_dir_count))
        print ('{} artist overrides specified in {} simlar groups. '.format(artist_dir_override_count,len(similar_dirs)))
        print ('{} artist directories will be created in {}.'.format(len(new_artist_dirs),target_folder))
        print ('{} music files will be copied.'.format(len(copy_info)))
        print ('{} files will be skipped.'.format(len(skipped_files)))
        # Continue?
        msg = 'Shall I?'
        get_attention()
        shall = input("%s (y/N) " % msg).lower() == 'y'
        if shall:
            print('Proceeding to copy, hang tight...')
        else:
            print('Process cancelled.')
            return
        # User is proceeding to do the work.
        for source_file, copy_to in copy_info:
            new_path, copy_name = os.path.split(copy_to)
            print('Moving {} to {}'.format(source_file,copy_to))
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            shutil.copyfile(source_file, copy_to)
        get_attention()

    def check_to_keep_file(self, music_file_path, all_files_info, default_not_specified=True ):
        """Returns True if the music_file_path should be kept.
        If exists in our all_files_info list, then we will check
        the info to see if it specifies whether or not to keep it.
        If it doesn't specify then it will use the default passed in.
        """
        if os.path.splitext(music_file_path)[1].lower() != '.mp3':
            print('non mp3 file {}'.format(music_file_path))
            raise Exception('Non-music file')
        keep_file_paths = []
        for file_info in all_files_info:
            for p in file_info['similar_files']:
                if p['path'] == music_file_path:
                    if p.get('keep', default_not_specified) is None:
                        return p.get('suggest_keep', default_not_specified)
        return default_not_specified

    def get_all_files_from_folder(self, music_folder=None):
        """Returns all the music full file path locations in the 
        specified folder.
        If no folder is specified it will use the default music folder
        defined in the class name."""
        print( "Getting files from folder:  {}".format(music_folder))
        if music_folder is None:
            music_folder = self.music_folder
        all_files = []
        all_full_file_names = []
        for dir_name, sub_dir_list, file_list in os.walk(music_folder):
            full_file_names = [os.path.join(dir_name,file_name) for file_name in file_list]
            all_files.extend(file_list)
            all_full_file_names.extend(full_file_names)
        return all_full_file_names

    def get_all_files_from_folders(self, music_folders):
        """Gets all the file in the folders specified."""
        all_files_all_folders = []
        for mf in music_folders:
            all_files_all_folders.extend(self.get_all_files_from_folder(mf))
        return all_files_all_folders

    def similar(self, a,b):
        return SequenceMatcher(None, a, b).ratio()

    def choose_file(self,f1, f2):
        """Logic to choose which of the two files to keep, assuming we think they are the same
        or similar based on file name and path.
        Assumes larger sized file is better quality."""
        stat1 = os.stat(f1)
        stat2 = os.stat(f2)
        if stat1.st_size > stat2.st_size:
            # print 'Keep File 1 {}'.format(stat1.st_size-stat2.st_size)
            return f1
        else:
            # print 'Keep File 2 {}'.format(stat2.st_size-stat1.st_size)
            return f2

    def get_similar_file_names(self, start_index=0):
        """Returns the duplicate count.
        Specify a start_index > 1000 to speed up tests."""
        sim_count = 0
        slice_index = 0
        sim_names = []
        all_full_file_names = self.get_all_files_from_folder()
        for y, f1 in enumerate(all_full_file_names[start_index:], start=start_index):
            f1_dir, f1_name = os.path.split(f1)
            slice_index = y + 1
            if slice_index < len(all_full_file_names):
                for f2 in all_full_file_names[slice_index:]:
                    if f1 != f2:
                        f2_dir, f2_name = os.path.split(f2)
                        if f2_dir != f1_dir:
                            if self.similar(f1_name,f2_name)>.8:
                                # Gets tuple of full paths
                                suggest = self.choose_file(f1, f2)
                                sim_names.append({"name1":f1, 
                                    "name2":f2,
                                    "suggest_keep":suggest})
        return sim_names

    def get_similar_parent_names(self, start_index=0):
        """Returns the duplicate count.
        Specify a start_index > 1000 to speed up tests."""
        sim_count = 0
        slice_index = 0
        sim_names = []
        all_full_file_names = self.get_all_files_from_folder()
        for y, f1 in enumerate(all_full_file_names[start_index:], start=start_index):
            f1_dir, f1_name = os.path.split(f1)
            slice_index = y + 1
            if slice_index < len(all_full_file_names):
                for f2 in all_full_file_names[slice_index:]:
                    if f1 != f2:
                        f2_dir, f2_name = os.path.split(f2)
                        if f2_dir != f1_dir:
                            if self.similar(f2_dir,f1_dir)>.8:
                                # Gets tuple of full paths
                                sim_names.append({"name1":f1, 
                                    "name2":f2})
                                # Gets tuple of names
                                # sim_names.append(similarNames(f1_name, f2_name))
                                
                                # if self.choose_file(f1, f2) == f1:
                                #     print( 'File 1: {}     <---'.format(f1) )
                                #     print( 'File 2: {}'.format(f2))
                                # else:
                                #     print( 'File 1: {}'.format(f1) )
                                #     print( 'File 2: {}     <---'.format(f2))
                                # sim_count += 1
        return sim_names

    def get_music_folder_dir_count(self, music_folder=None):
        """Returns the number of directories in the music folder"""
        if music_folder is None:
            music_folder = self.music_folder
        for dir_name, sub_dir_list, file_list in os.walk(music_folder):
            return len(sub_dir_list)

    def get_consolidation_directory_candidates(self, music_folder=None):
        """Get all the folder names that could potentially 
        be consolidated.
        It is assumed that the directories inside the music_folder is 
        derived from the artist name.  Example: (Eminem, Jay-Z)"""
        if music_folder is None:
            music_folder = self.music_folder
        sub_dirs = []
        similar_path_buckets = []
        for dir_name, sub_dir_list, file_list in os.walk(music_folder):
            sub_dirs.extend([os.path.join(dir_name,f) for f in sub_dir_list])
            # Only one iteration of OS.Walk
            break
        print('Splitting {} directories(s) into similarity buckets...'.format(len(sub_dirs)))
        # All subdirectories are either similar to a directory
        # in a bucket already, or it goes in its own new bucket.
        for s in sub_dirs:
            add_to_bucket = None
            for b in similar_path_buckets:
                # if not in the bucket already, is it similar to 
                # the lowest level directory in the bucket.  
                # If so then it belongs in that bucket so add it.
                if s not in b['similar_paths']:
                    paths_in_bucket = b['similar_paths']
                    for pib in paths_in_bucket:
                        if self.similar(
                            os.path.split(pib)[1],
                            os.path.split(s)[1]) > .7:
                                add_to_bucket = b['similar_paths']
                                b['had_similar'] = True
                                break
            # If didn't find a bucket make a new one with it in it.
            # Otherwise add it to the bucket that exists.
            if add_to_bucket is None:
                similar_path_buckets.append({'similar_paths':[s],
                    'use_path_override':None})
            else:
                add_to_bucket.append(s)
        print('Sub-Directories split into {} similarity buckets'.format(len(similar_path_buckets)))
        return similar_path_buckets

    def get_consolidation_file_candidates(self, music_folder=None):
        """Gets all the files and groups them into similarity buckets.
        Each file in the bucket will have a 'keep' option along with
        a suggested file to keep from the group."""
        
        if music_folder is None:
            music_folder = self.music_folder
        all_files = self.get_all_files_from_folder(music_folder)
        sub_dirs = []
        similar_path_buckets = []
        print('Grouping {} music files into similarity buckets...'.format(len(all_files)))
        # All subdirectories are either similar to a directory
        # in a bucket already, or it goes in its own new bucket.
        for f in all_files:
            add_to_bucket = None
            for b in similar_path_buckets:
                # if not in the bucket already, is it similar to 
                # a file name in the bucket already?  
                # If so then it belongs in that bucket so add it.
                if f not in b['similar_files']:
                    paths_in_bucket = b['similar_files']
                    for pib in paths_in_bucket:
                        if self.similar(
                            os.path.split(pib)[1],
                            os.path.split(f)[1]) > .8:
                                add_to_bucket = b['similar_files']
                                b['had_similar'] = True
                                break
            # If didn't find a bucket make a new one with it in it.
            # Otherwise add it to the bucket that exists.
            if add_to_bucket is None:
                similar_path_buckets.append({'similar_files':[f],
                    'use_path_override':None})
            else:
                add_to_bucket.append(f)
        # Attempt to mark a single file in the bucket as the one to keep.
        similar_paths_with_options = []
        for b in similar_path_buckets:
            file_options = []
            keep_file = None
            paths_in_bucket = b['similar_files']
            # First lets find the one to suggest.
            for pib in paths_in_bucket:
                if keep_file is None:
                    keep_file = pib 
                else:
                    if pib == self.choose_file(pib,keep_file):
                        keep_file = pib
            # Suggest it, and mark the others as options
            for pib in paths_in_bucket:
                if pib == keep_file:
                    suggest_keep = True
                else:
                    suggest_keep = False
                file_options.append({"path":pib,
                                "keep":None,
                                "suggest_keep":suggest_keep})
            # Add dict buckets
            pwo = {'similar_files':file_options}
            if b.get('had_similar'):
                pwo['had_similar'] = True
            similar_paths_with_options.append(pwo)
        print('Files split into {} similarity buckets'.format(len(similar_paths_with_options)))
        return similar_paths_with_options

    def get_similar_top_folder_names(self,music_folder=None, start_index=0):
        """Whatever the specified folder is, it will get 
        a count of all the directories in that folder that
        are similar but not the same."""
        if music_folder is None:
            music_folder = self.music_folder
        sim_names = []
        for dir_name, sub_dir_list, file_list in os.walk(music_folder):
            for y, sd1 in enumerate(sub_dir_list):
                #pdir1, sd_name1 = os.path.split(sd1)
                slice_index = y + 1
                if y < len(sub_dir_list):
                    for sd2 in sub_dir_list[slice_index:]:
                        #pdir2, sd_name2 = os.path.split(sd2)
                        #if self.similar(sd_name1,sd_name2)>.8:
                        if self.similar(sd1,sd2)>.7:
                            sim_names.append({"name1":os.path.join(dir_name,sd1),
                            "name2":os.path.join(dir_name,sd2)})
                            # sim_names.append(similarNames(sd1, sd2))
            # Only 1 iteration of os.walk
            break
        return sim_names

    def load_file_data_dict(self, file_path=None):
        """This function will load the file generated
        by write_all_files_to_keep() that may have been modified
        with some custom settings."""
        music_storage = md_file_writer.musicStorageOutPut()
        return music_storage.load_music_data_from_file()

    def write_music_data_js(self):
        """Generates a json file called music_data.js that contains
        a dictionary of similar 'artist' directories that could potentially
        be overridden.
        Keys Are:
            All_Files_Info:  used for checking if the file should be copied or not.
            Similar_Directories: groups of artists directories that are similar 
                enough to be consolidated into a single artist override folder.
        The file can be modified to specify a different artist folder by specifying
        the 'use_path_override' key, that will be used in place of the similar artist
        folders folders in the 'similar_paths' key within the 'Similar_Directories'.
        The file can be read in by get_copy_to_mappings(), which will
        take generate new paths for the files that we want to copy from to take
        to place them into the override folder."""
        #all_files = self.get_all_files_from_folder(self.music_folder)
        #similar_names = self.get_similar_file_names(start_index=0)
        #similar_parent_dirs = self.get_similar_top_folder_names()
        all_files_info = []
        music_dict = { "Similar_Directories":self.get_consolidation_directory_candidates(),
        "Similar_Files":self.get_consolidation_file_candidates()}
        # print( "File Count:  {}".format(len(all_files)))
        music_storage = md_file_writer.musicStorageOutPut()
        music_storage.write_to_file(music_dict)
        get_attention()

if __name__ == '__main__':
    md = musicDeDuper()
    msg = 'Do you want to create a new .json file?'
    shall = input("%s (y/N) " % msg).lower() == 'y'
    if shall:
        print('Proceeding to create new json, hang tight...')
        md.write_music_data_js()
    else:
        print('No json file will be created.')
    msg ='Do you want to copy from a .json file?'
    shall = input("%s (y/N) " % msg).lower() == 'y'
    if shall:
        print('Proceeding to copy from mappings, hang tight...')
        md.get_copy_to_mappings()
    else:
        print('No copies were made.')
    # 
    
    