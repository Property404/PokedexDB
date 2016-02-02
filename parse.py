#########################################
#              database.py              #
#   Contains parse-specific functions   #
#########################################


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
		return value[0:value.find("|")]
	else:
		return None
