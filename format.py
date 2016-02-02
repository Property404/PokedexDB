#########################################
#				format.py				#
# Module for formatting certain strings #
#########################################
import urllib.request
import re # Regular Expressions

# Undo URL encoding, and replace '-'s with spaces
def format_pokemon_name(name):
	return urllib.request.unquote(name.replace("_"," "))
	
# Split with spaces where capitalized or there are numbers, and deal with special cases (Roarof, Lightof)
def format_move_name(name):
	return re.sub(r'([a-z]*)([A-Z,0-9])',r'\1 \2',name).replace("- ","-")[1::].replace("Roarof","Roar of").replace("Lightof","Light of")