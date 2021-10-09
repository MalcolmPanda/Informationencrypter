#!/usr/bin/env python3
import re
import os
import sys
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, kdf
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

#generate our key
def write_key():
	key = Fernet.generate_key()
	with open("key.key", "wb") as key_file:
		key_file.write(key)
		
def check_key(): # check if our key exists on start
	if os.path.exists('key.key') == False:
		write_key()
		
check_key()

def load_key(): # load our key
	return open("key.key", "rb").read()

curr_key = load_key()




def encrypt(message: bytes, curr_key: bytes) -> bytes: # encrypts our message
	return Fernet(curr_key).encrypt(message)
	


def decrypt(token: bytes, curr_key: bytes) -> bytes: # decrypts our message!
    return Fernet(curr_key).decrypt(token)


f = Fernet(curr_key)

def view():
		with open('encrypted.txt', 'rb') as nf:
			for line in nf.readlines():
				data = line.rstrip()
				user, passw = data.split(b'|')
				ruser = f.decrypt(user).decode("utf-8")
				rpassw = f.decrypt(passw).decode("utf-8")

				print("User: ", ruser,"|", "Password:",rpassw)



def add():
	name = input("Account Name: ")
	pattern = re.match("^[a-zA-Z0-9!@#$]*$", name)
	error_char = "Error only letters, numbers, and the symbols !@#$ are allowed!"
	error_len = "Error only 15 characters are allowed!"
	if not pattern:
		print(error_char)
		sys.exit()
	elif len(name) > 15:
		print(error_len)
		sys.exit()
	pwd = input("password: ")
	if not pattern:
		print(error_char)
		sys.exit()
	elif len(pwd) > 15:
		print(error_len)
		sys.exit()

	name =bytes(name, 'utf-8')
	pwd =bytes(pwd, 'utf-8')
	encrypted_name = f.encrypt(name)
	encrypted_pwd = f.encrypt(pwd)
	file = open("encrypted.txt", "ab")
	file.write(encrypted_name + b'|' +encrypted_pwd + b'\n')
	file.close()

	


while True:
	mode = input("Hello! Would you like to add a new Account or view existing ones? (View, Add) press q to quit. ").lower()
	if mode == "q":
 		break
	if mode == "view":
		view()
	elif mode == "add":
		add()
	else:
		print("Invalid mode.")
	continue
