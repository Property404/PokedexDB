#!/usr/bin/env python3
from pokedex import load, database
import datetime
import sys

# Create database object
db = database.Database("PokeDex")
# Num of Pokemon
no_of_pokemon=721
if len(sys.argv)>1:
	if sys.argv[1]=="-p":
		if len(sys.argv)>2:
			no_of_pokemon=int(sys.argv[2])
		else:
			print("Number of Pokemon not specified")
			exit()
	else:
		print("No option "+sys.argv[1])
		exit()

# Load data
print("Loading types")
load.load_types(db)
print("Loading moves")
load.load_moves(db)
print("Loading Pokemon")
load.load_pokemon(db,no_of_pokemon)

# Comment
db.comment = "/*\n\tPokedexDB\n\thttps://github.com/Property404/PokedexDB\n\tGenerated " +\
			 str(datetime.datetime.now()) +\
			 "\n\tPython version " + ".".join([str(i) for i in sys.version_info[0:3]]) + "\n*/\n"

# Export SQL
fp = open("dex.sql", "wb")
fp.write(db.to_sql().encode("utf8"))
fp.close()
