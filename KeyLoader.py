from Crypto.Cipher import AES
from Crypto import Random
import json, hashlib

class KeyLoader(object):
    '''Used to lock down pyna files with a password'''

    def pad(self, phrase):
        '''Pads a phrase to 16b'''
        remainder = len(phrase) % 16
        if remainder == 0:
            return phrase

        length = 16-remainder
        return phrase + bytes([length])*length

    def hash_phrase(self, phrase, type):
        '''Hash a phrase with a given type (such as hashlib.sha256)'''
        hashed = type()
        hashed.update(phrase)
        return hashed.digest()

    def lock_with_password(self, password, content_to_lock):
        '''Use a cipher to lock down content with a password'''
        cipher = self.get_cipher(password)
        padded = self.pad(content_to_lock)
        return cipher.encrypt(padded)

    def unlock_with_password(self, password, encrypted):
        '''Use an AES cipher to unlock content with a password'''
        cipher = self.get_cipher(password)
        decrypted = cipher.decrypt(encrypted)
        decrypted = decrypted.decode('utf-8')
        end_of_json = decrypted.rfind('}')

        return json.loads(decrypted[:(1+end_of_json)].strip())

    def get_cipher(self, password):
        '''Create an AES cipher from a password. Work in Progress'''
        hashed = self.hash_phrase(password.encode('utf-8'), hashlib.sha256)
        aes_iv = self.hash_phrase(hashed, hashlib.sha1)
        return AES.new(hashed, AES.MODE_CBC, aes_iv[:AES.block_size])
