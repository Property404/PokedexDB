#########################################
#              database.py              #
#   Contains parse-specific functions   #
#########################################

import urllib.request
import re  # Regular Expressions

# Separated infobox from html
def get_infobox(html):
	infobox = html[html.find("mon Infobox|" if "mon Infobox|" in html else
							 "mon Infobox |" if "mon Infobox |" in html else "mon Infobox\n|")::]
	return infobox[0:infobox.find("\n}}")].replace("\n", "").replace(" |", "|")


# Get an attribute from an infobox
def get_from_infobox(attribute, infobox):
	attribute += "="
	if attribute in infobox:
		value = infobox[infobox.find(attribute)+len(attribute)::]
		if value[0] == "{":
			value=value[value.find("|")+1::]
		if value[0:8]=="&lt;!--{":
			value="&lt;"+value[value.find("|")+1::]
		return value[0:value.find("|")]
	else:
		return None
		
# Undo URL encoding, and replace '-'s with spaces
def format_pokemon_name(name):
	return urllib.request.unquote(name.replace("_", " "))


# Split with spaces where capitalized or there are numbers, and deal with special cases (Roarof, Lightof)
def format_move_name(name):
	return re.sub(r'([a-z]*)([A-Z,0-9])', r'\1 \2', name).replace("- ", "-")[1::].replace("Roarof", "Roar of").\
		replace("Lightof", "Light of")

