'''
Contains all class methods for interacting with posts and profiles

'''


# profile.py
#
# Author Mark S. Baldwin
#
# v0.1.8

import json, time, os
from pathlib import Path


"""
DsuFileError is a custom exception handler. It
is raised when attempting to load or save Profile objects to file the system.

"""
class DsuFileError(Exception):
    pass

"""
DsuProfileError is a custom exception handler. It
is raised when attempting to deserialize a dsu file to a Profile object.

"""
class DsuProfileError(Exception):
    pass


class Post(dict):
    """ 

    The Post class is responsible for working with individual user posts. It currently supports two features: 
    A timestamp property that is set upon instantiation and when the entry object is set and an 
    entry property that stores the post message.

    """
    def __init__(self, entry:str = None, timestamp:float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)
    
    def set_entry(self, entry):
        self._entry = entry 
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        return self._entry
    
    def set_time(self, time:float):
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)
    
    def get_time(self):
        return self._timestamp

    """

    The property method is used to support get and set capability for entry and time values.
    When the value for entry is changed, or set, the timestamp field is updated to the
    current time.

    """ 
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)
    
    
class Profile:
    """
    The Profile class shows the properties required to join an DSU server.

    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver # REQUIRED
        self.username = username # REQUIRED
        self.password = password # REQUIRED
        self.bio = ''            # OPTIONAL
        self._posts = []         # OPTIONAL
    
    """

    add_post accepts a Post object as parameter and appends it to the posts list. Posts are stored in a 
    list object in the order they are added. So if multiple Posts objects are created, but added to the 
    Profile in a different order, it is possible for the list to not be sorted by the Post.timestamp property. 

    """

    def add_post(self, post: Post) -> None:
        self._posts.append(post)

    """

    del_post removes a Post at a given index and returns True if successful and False if an invalid 
    index was supplied. 

    """

    def del_post(self, index: int) -> bool:
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False
        
    """
    
    get_posts returns the list object containing all posts that have been added to the Profile object

    """
    def get_posts(self) -> list[Post]:
        return self._posts

    """

    save_profile accepts an existing dsu file to save the current instance of Profile to the file system.

    Example usage:

    profile = Profile()
    profile.save_profile('/path/to/file.dsu')

    Raises DsuFileError

    """
    def save_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("An error occurred while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")

    """

    load_profile will populate the current instance of Profile with data stored in a DSU file.

    Example usage: 

    profile = Profile()
    profile.load_profile('/path/to/file.dsu')

    Raises DsuProfileError, DsuFileError

    """
    def load_profile(self, path: str) -> None:
        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
