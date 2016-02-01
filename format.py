import urllib.request
import re

def format_pokemon_name(name):
	return urllib.request.unquote(name.replace("_"," "))
def format_move_name(name):
	return re.sub(r'([a-z]*)([A-Z,0-9])',r'\1 \2',name).replace("- ","-")[1::]