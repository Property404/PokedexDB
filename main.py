import load
import database
import datetime
import sys

# Create database object
db = database.Database("PokeDex")

# Load data
print("Loading types")
load.load_types(db)
print("Loading moves")
load.load_moves(db)
print("Loading Pokemon")
load.load_pokemon(db)

# Comment
db.comment = "/*\n\tPokedexDB\n\thttps://github.com/Property404/PokedexDB\n\tGenerated " +\
			 str(datetime.datetime.now()) +\
			 "\n\tPython version " + ".".join([str(i) for i in sys.version_info[0:3]]) + "\n*/\n"

# Export SQL
fp = open("dex.sql", "wb")
fp.write(db.to_sql().encode("utf16"))
fp.close()
