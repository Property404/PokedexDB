import load
import database

db = database.Database("PokeDex")
print("Loading types")
load.load_types(db)
print("Loading moves")
load.load_moves(db)
print("Loading Pokemon")
load.load_pokemon(db)


open("dex_xml.html","wb").write(db.to_html().encode("utf16"))
open("dex_sql.txt","wb").write(db.to_sql().encode("utf16"))