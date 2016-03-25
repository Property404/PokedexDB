#!/usr/bin/env python3
import sys

# Check for Python version
if sys.version_info < (3,4):
	print("Requires Python version>=3.4")
	print("You are using Python "+str(sys.version_info[0])+"."+str(sys.version_info[1]))
	exit()

# Load other modules
from pokedex import load, database
import datetime

# Create database object
db = database.Database("PokeDex")
# Num of Pokemon
no_of_pokemon=721
use_alt_names = False
if len(sys.argv)>1:
	if sys.argv[1]=="-p" or sys.argv[1]=='-f':
		if len(sys.argv)>2:
			no_of_pokemon=int(sys.argv[2])
			if sys.argv[1]:
				use_alt_names = True
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
load.load_pokemon(db,no_of_pokemon,use_alt_names)

# Comment
db.comment = "/*\n\tPokedexDB\n\thttps://github.com/Property404/PokedexDB\n\tGenerated " +\
			 str(datetime.datetime.now()) +\
			 "\n\tPython version " + ".".join([str(i) for i in sys.version_info[0:3]]) + "\n*/\n"

# Export SQL
print("Exporting to SQL")
fp = open("dex.sql", "wb")
fp.write(db.to_sql().encode("utf8"))
fp.close()
print("Done!")
