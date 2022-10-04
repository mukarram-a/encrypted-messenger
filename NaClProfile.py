'''

Handles functions for encrypting messages, posts, and files.
Overrides methods from 'Profile.py' for encryption and receives
user input from 'a5.py' to encrpyt/decrypt.

'''


# Mukarram A.
# NaClProfile.py

# An encrypted version of the Profile class provided by the Profile.py module, partial code by Mark S. Baldwin


from curses import KEY_A1, keyname
from re import L
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from profile import Profile, DsuFileError, DsuProfileError, Post
from NaClDSEncoder import NaClDSEncoder
from pathlib import Path
import json, time, os

na_class = NaClDSEncoder()

class NaClProfile(Profile):
    def __init__(self):
        """
        public_key:str
        private_key:str
        keypair:str

        """
        super().__init__()
        self.public_key = ''
        self.private_key = ''
        self.keypair = ''


    def generate_keypair(self) -> str:
        """
        Generates a new public encryption key using NaClDSEncoder.

        :return: str 

        """
        na_class.generate()
        self.public_key = na_class.public_key
        self.private_key = na_class.private_key
        self.keypair = na_class.keypair
        
        return self.keypair
        

    def import_keypair(self, keypair: str):
        """
        Imports an existing keypair. Useful when keeping encryption keys in a location other than the
        dsu file created by this class.

        """

        self.public_key = keypair[0:44]
        self.private_key = keypair[44:]
        self.keypair = keypair


    def add_post(self, post):
        """
        Overrides the add_post method to encrypt post entries.

        """

        post = post['entry']
        box = na_class.create_box(na_class.encode_private_key(self.private_key), na_class.encode_public_key(self.public_key))
        encrypted_msg = na_class.encrypt_message(box, post)
        super().add_post(Post(encrypted_msg))
        

    def get_posts(self) -> list[Post]:
        """
        Overrides the get_posts method to decrypt post entries.

        :return: Post
        """

        box = na_class.create_box(na_class.encode_private_key(self.private_key), na_class.encode_public_key(self.public_key))        
        post_list = super().get_posts()
        decrypted_list = []

        for i in post_list:
            x = i.entry
            msg = na_class.decrypt_message(box, x)
            decrypted_list.append(Post(msg, i.timestamp))


        
        return decrypted_list
        
    def load_profile(self, path: str) -> None:
        """
        Overrides the load_profile method to add support for storing a keypair.
        
        """

        p = Path(path)

        if os.path.exists(p) and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                self.public_key = obj['public_key']
                self.private_key = obj['private_key']
                self.keypair = obj['keypair']
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()



    def encrypt_entry(self, entry:str, public_key:str) -> bytes:
        """
        Encrypt messages using a 3rd party public key, such as the one that
        the DS server provides.

        :return: bytes 
        """

        box = na_class.create_box(na_class.encode_private_key(self.private_key), na_class.encode_public_key(public_key))
        public_encrypted_msg = na_class.encrypt_message(box, entry)

        return public_encrypted_msg
