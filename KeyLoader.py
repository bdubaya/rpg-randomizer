from Crypto.Cipher import AES
from Crypto import Random
import json, hashlib

class KeyLoader(object):
    def pad(self, phrase):
        remainder = len(phrase) % 16
        if remainder == 0:
            return phrase

        length = 16-remainder
        return phrase + bytes([length])*length

    def hashPhrase(self, phrase, type):
        hashed = type()
        hashed.update(phrase)
        return hashed.digest()

    def lockWithPassword(self, password, locked_content):
        cipher = self.getCipher(password)
        return cipher.encrypt(self.pad(locked_content))

    def unlockWithPassword(self, password, encrypted):
        cipher = self.getCipher(password)
        decrypted = cipher.decrypt(encrypted)
        decrypted = decrypted.decode('utf-8')
        end_of_json = decrypted.rfind('}')

        return json.loads(decrypted[:(1+end_of_json)].strip())

    def getCipher(self, password):
        hashed = self.hashPhrase(password.encode('utf-8'), hashlib.sha256)
        aes_iv = self.hashPhrase(hashed, hashlib.sha1)
        return AES.new(hashed, AES.MODE_CBC, aes_iv[:AES.block_size])
