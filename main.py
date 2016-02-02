import load
import database

# Create database object
db = database.Database("PokeDex")

# Load data
print("Loading types")
load.load_types(db)
print("Loading moves")
load.load_moves(db)
print("Loading Pokemon")
load.load_pokemon(db)

# Export SQL
open("dex.sql", "wb").write(db.to_sql().encode("utf16"))
