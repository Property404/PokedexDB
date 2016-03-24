#########################################
#               load.py                 #
#   Module for parsing Bulbapedia and   #
#       loading data into tables        #
#########################################
from pokedex import database, pokemon, parse, webcache

# Constants
BULBAPEDIA = "http://bulbapedia.bulbagarden.net/"
DESCRIPTION_LENGTH = 1280


# Load type table
def load_types(db):
	# Set up table
	type_table = database.Table("type")

	# Set up columns
	type_table.set_columns([
		database.Column("type_code", "smallint", pk=True),
		database.Column("type_name", "varchar(32)", not_null=True, unique=True)
		])

	# List types
	types = ["normal", "fire", "fighting", "water", "flying", "grass", "poison", "electric", "ground", "psychic",
			 "rock", "ice", "bug", "dragon", "ghost", "dark", "steel", "fairy", "???"]

	# Put types into rows
	for i in range(len(types)):
		type_table.add_row([str(i+1), types[i]])

	# Add to database
	db.add_table(type_table)


# Load moves (unassociated)
def load_moves(db):
	# Get the source page for list of moves
	move_page = webcache.get_page(BULBAPEDIA+"w/index.php?title=List_of_moves&action=edit")\
		.replace("\r", "").replace(" ", "")

	# Loop through to get info on moves
	i = 0
	moves = []
	while True:
		i += 1

		# Start and end of move box
		start_note = "|{0}\n|{{{{m|".format(i)
		end_note = "}\n|"

		# Check if move exists
		if start_note not in move_page:
			break

		# Get move information box
		move_box = move_page[move_page.find(start_note)+len(start_note)::]
		move_box = move_box[0:move_box.find(end_note)]

		# Create Move object
		move = pokemon.Move(name=parse.format_move_name(move_box[0:move_box.find("}")]))

		# Get type
		move.type = move_box[move_box.find("typetable|")+10::]
		move.type = move.type[0:move.type.find("}")]

		# Get category
		move.category = move_box[move_box.find("statustable|")+12::]
		move.category = move.category[0:move.category.find("}")]

		# Get condition
		move.condition = move_box[move_box.find("contesttable|")+13::]
		move.condition = move.condition[0:move.condition.find("}")]

		# Make type as foreign keys
		for j in range(len(db.get_table("type").rows)):
			if move.type.lower() == db.get_table("type").get_cell("type_name", j):
				move.type = str(db.get_table("type").get_cell("type_code", j))
				break

		# Append to move list
		moves.append(move)

	# Create table
	move_table = database.Table("move")
	move_table.set_columns(
		[database.Column("move_code", "smallint", pk=True),
			database.Column("move_name", "varchar(32)", not_null=True, unique=True),
			database.Column("move_category", "varchar(32)", not_null=True),
			database.Column("move_condition", "varchar(32)", not_null=True),
			database.Column("type_code", "smallint", fk=True, relation="type", not_null=True)])

	# Load rows
	for i in range(len(moves)):
		move_table.add_row([str(i+1), moves[i].name, moves[i].category, moves[i].condition, moves[i].type])

	# Add to database
	db.add_table(move_table)


# Load Pokemon table and associated pokemon moves
def load_pokemon(db, no_of_pokemon=721):
	# Set up table
	pkm_table = database.Table("pkm")
	learnset_table = database.Table("pokemove")
	poketype_table = database.Table("poketype")

	end_tag = "_(Pok%C3%A9mon)"
	start_tag = "/wiki/"

	# Get main pokemon page
	main_page = webcache.get_page(BULBAPEDIA+start_tag+"List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number")
	main_page = main_page[main_page.find("Bulbasaur")-50::]

	# Loop through list of pokemon
	pkm_list = []
	print("\tLooping through pokemon")
	while len(pkm_list) < no_of_pokemon:
		# First and last part of the URL
		last = main_page.find(end_tag)
		first = main_page[0:last].rfind(start_tag)

		# Get name
		pkm_name = main_page[first+len(start_tag):last]

		# Update page
		main_page = main_page[last+len(end_tag)::]

		# Add to list
		if len(pkm_list) == 0 or pkm_list[-1].name != parse.format_pokemon_name(pkm_name):
			pkm_list.append(pokemon.Pokemon(number=len(pkm_list)+1, name=parse.format_pokemon_name(pkm_name),
											page=BULBAPEDIA+"w/index.php?title="+pkm_name+end_tag+"&action=edit"))

	# Alt name lit
	altnames = [" Man"]

	# Gather information on pokemon
	print("\tGathering info on pokemon")
	for pkm in pkm_list:
		page = webcache.get_page(pkm.page)

		# Separate out info box
		infobox = parse.get_infobox(page)

		# Get types
		pkm.type1 = parse.get_from_infobox("type1", infobox)
		pkm.type2 = parse.get_from_infobox("type2", infobox)

		"""
		<hello>buddy<hello>
		buddy<hello>
		<hello>buddy
		"""

		# Get Category
		pkm.category = parse.get_from_infobox("category", infobox)
		if pkm.category is None:
			pkm.category = parse.get_from_infobox("species", infobox)
		if "&lt;" == pkm.category[0:4]:
			pkm.category = pkm.category[4::]
			if ">" in pkm.category:
				pkm.category = pkm.category[pkm.category.find(">")+1::]
		if "&lt;" in pkm.category:
			pkm.category = pkm.category[0:pkm.category.find("&lt;")]
		while pkm.category[0] == " ":
			pkm.category = pkm.category[1::]
		if pkm.name == "Boldore":  # Because I don't want to spend more time on this
			pkm.category = "Ore"

		# Get Fun name
		pkm.altname = pkm.category+" Man"
		if pkm.altname in altnames:
			pkm.altname = " Man"
			while pkm.altname in altnames:
				pkm.altname=pkm.altname[0].lower()+pkm.altname[1::]
				pkm.altname = parse.re.findall(r"[^aeiou]*[aeiou]+[^aiousy]*", pkm.name)[0].lower()+pkm.altname
				pkm.altname=pkm.altname[0].upper()+pkm.altname[1::]
		altnames.append(pkm.altname)

		# Get weight
		pkm.weight = parse.get_from_infobox("weight-kg", infobox)

		# Get description
		pkm.description = page[page.find("==Biology==")+12::]
		# Modify beginning
		pkm.description = parse.re.sub(r"\[\[File:.*?]][\s\n]*", r"", pkm.description, parse.re.MULTILINE)
		pkm.description = parse.re.sub(r"^\s*\n*\s*", r"", pkm.description)
		# End selection of description at double new lines or double equals
		if "=" in pkm.description:
			pkm.description = pkm.description[0:pkm.description.find("==")]
		if "\n\n" in pkm.description:
			pkm.description = pkm.description[0:pkm.description.find("\n\n")]
		# Replace references
		for n in range(2):
			pkm.description = parse.re.sub(r"\[\[File:.*?]][\s\n]*", r"", pkm.description)
			pkm.description = parse.re.sub(r"\[\[([^\]]*\|)*(.*?)]]", r"\2", pkm.description)
			pkm.description = parse.re.sub(r"\{\{([^\}]*\|)*(.*?)}}", r"\2", pkm.description)
			pkm.description = parse.re.sub(r"&lt;ref>.*?&lt;/ref>", r"", pkm.description)
			pkm.description = parse.re.sub(r"&lt;!--.*?-->", r"", pkm.description)
			pkm.description = parse.re.sub(r"&lt;gallery>\n*(.*\n*)*?&lt;/gallery>", r"", pkm.description,
										   parse.re.MULTILINE)
		# Make sure not in a file reference
		if "]]" in pkm.description:
			pkm.description = pkm.description[pkm.description.find("]]")+2::]
		# Modify beginning again
		while pkm.description[0] in ["\n", " ", "\r"]:
			pkm.description = pkm.description[1::]
		# Get rid of anomolies
		if "&lt;" in pkm.description:
			pkm.description = pkm.description[0:pkm.description.find(" &lt;")]
		# Check description length
		if len(pkm.description) >= DESCRIPTION_LENGTH:
			print("\tDescription exceeds description length: "+str(len(pkm.description)))

		# Prepare to get info on moves
		learnlist_tag = "{{learnlist/levelVI|"
		double_up = True
		if learnlist_tag not in page:
			learnlist_tag = "{{learnlist/level6|"
			double_up = False  # Skip a pipe before parsing

		# Get info on moves
		while learnlist_tag in page:
			page = page[page.find(learnlist_tag)+len(learnlist_tag)::]

			if double_up:
				page = page[page.find("|")+1::]

			# Get move requirements
			up_level = page[0:page.find("|")]

			# Get move
			page = page[page.find("|")+1::]
			# This is a generational difference correction:
			up_move = page[0:page.find("|")].replace("Sand-Attack", "Sand Attack")

			# Search database for moves:
			up_move_no = None
			for i in range(len(db.get_table("move").rows)):
				if db.get_table("move").get_cell("move_name", i) == up_move:
					up_move_no = i+1
					break
			if up_move_no is None:
				print("\t`" + up_move + "` replaced with NULL")
			pkm.moves.append([up_move_no, up_level])

	# Set up columns
	print("\tSetting up columns in `pkm`")
	pkm_table.set_columns([
		database.Column("pkm_code", "smallint", pk=True),
		database.Column("pkm_name", "varchar(32)", not_null=True, character_set="utf16",
						collate="utf16_unicode_ci", unique=True),
		database.Column("pkm_category", "varchar(32)", not_null=True, character_set="utf16",
						collate="utf16_unicode_ci", unique=False),
		database.Column("pkm_description", "varchar({0})".format(DESCRIPTION_LENGTH), character_set="utf16",
						collate="utf16_unicode_ci", not_null=True),
		database.Column("pkm_weight", "float", not_null=True),
		database.Column("evolution_code", "smallint", not_null=False, fk=True, relation="pkm")
		])
	learnset_table.set_columns([
		database.Column("pkm_code", "smallint", pk=True, fk=True, relation="pkm", not_null=True),
		database.Column("move_code", "smallint", pk=True, fk=True, relation="move", not_null=True),
		database.Column("pokemove_level", "tinyint")
		])
	poketype_table.set_columns([
		database.Column("pkm_code", "smallint", pk=True, fk=True, relation="pkm"),
		database.Column("type_code", "smallint", pk=True, fk=True, relation="type"),
		database.Column("poketype_is_primary", "boolean", not_null=True)
		])

	# Enter rows into table:
	learnset_number = 0
	for pkm in pkm_list:
		# Relate Types
		type1 = None
		type2 = None
		for i in range(len(db.get_table("type").rows)):
			if pkm.type1 is not None and pkm.type1.lower() == db.get_table("type").get_cell("type_name", i):
				type1 = str(db.get_table("type").get_cell("type_code", i))
			if pkm.type2 is not None and pkm.type2.lower() == db.get_table("type").get_cell("type_name", i):
				type2 = db.get_table("type").get_cell("type_code", i)

		# Commit pokemon object to table
		pkm_table.add_row([pkm.number, pkm.name, pkm.category, pkm.description, str(pkm.weight), None])
		poketype_table.add_row([pkm.number, type1, 1])

		# Commit pokemon type to table
		if type2 is not None and type1 != type2:
			poketype_table.add_row([pkm.number, type2, 0])

		# Commit pokemon moves to table
		learnset_keys = []
		for j in pkm.moves:
			learnset_number += 1
			# include some code to deal with multiple codes
			if str(pkm.number)+str(j[0]) not in learnset_keys:
				learnset_table.add_row([pkm.number, j[0], j[1]])
				learnset_keys.append(str(pkm.number)+str(j[0]))

	db.add_table(pkm_table)
	db.add_table(learnset_table)
	db.add_table(poketype_table)
