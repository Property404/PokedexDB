#########################################
#              database.py              #
# Contains classes related to database  #
#               structure               #
#########################################


# Column of a table
class Column:	
	# constructor
	def __init__(self, name, type, pk=None, fk=None, relation=None, hidden = None, not_null = None):
		# General column info
		self.name = name
		self.type = type #e.g VARCHAR, int, float

		# Keys
		self.pk = False if pk==None else pk
		self.fk = False if fk==None else fk
		self.relation = relation

		# Default
		self.not_null = False if not_null  == None else not_null
		if self.pk:
			self.not_null = True
		
# Table of a database
class Table(object):
	# Constructor
	def __init__(self, name):
		self.name = name
		self.columns = []
		self.rows = []
	
	# Getters
	def get_cell(self, column, row):
		for i in range(len(self.columns)):
			if self.columns[i].name==column:
				break
		return self.rows[row][i]
		
	# Setters and adders
	def add_row(self, row):
		assert len(row) == len(self.columns)
		self.rows.append(row)
		
	def add_columns(self, column):
		self.columns.append(column)
		
	def set_columns(self, columns):
		self.columns=columns

	# Export as XML 
	def to_xml(self):
		# Begin table tag
		xml="<table name='{0}'>\n".format(self.name)
		
		# Begin columns tag
		xml+="\t<columns>\n"
		
		# Show columns
		for i in self.columns:
			xml+="\t\t<column pk='{0}' fk='{1}' type='{2}'>{3}</column>\n".format("true" if i.pk==True else "false", "true" if i.fk==True else "false", i.type, i.name)
		xml+="\t</columns>\n"
		
		#Show rows
		for i in self.rows:
			xml+="\t<row>\n"
			for j in i:
				xml+="\t\t<cell>{0}</cell>\n".format(j)
			xml+="\t</row>\n"
		
		# End
		xml += "</table>"
		return xml

class Database:
	# Constructor
	def __init__(self, name = None):
		self.name = name
		self.tables = []
	
	# Getters
	def get_table(self, tname):
		for i in self.tables:
			if i.name == tname:
				return i
		return None
		
	# Setters
	def add_table(self, table):
		self.tables.append(table)
	
	# Export as HTML by using XML with custom styling
	def to_html(self):
		html = """<!DOCTYPE html>
<html>
<body>
<style>
row {border: 1px solid black; display: table-row; }
columns {border: 1px solid black; display: table-row; }
column {border: 1px solid black; display: table-cell; font-weight: bold; background-color: #CCC;}
cell {border: 1px solid black; display: table-cell; }
</style>"""
		
		html+="\n"
		for i in self.tables:
			html += i.to_xml()
	
		html+="""
</body>
</html>"""

		return html
		
	# Create database with SQL
	def to_sql(self):
		commands=""
		# Cycle through tables
		for i in self.tables:
			commands+="CREATE TABLE IF NOT EXISTS `"+i.name+"`("
			
			# Add column names
			f_keys = [] # foreign key list
			for j in i.columns:
				commands+="`"+j.name+"` "+j.type+(" NOT NULL" if j.not_null else "")+(" PRIMARY KEY" if j.pk else "")+","
				# Add to foreign key list
				if j.fk:
					f_keys.append(j)
			
			# Add foreign keys
			for j in f_keys:
				commands+="FOREIGN KEY {0}({1}) REFERENCES {2}({3}) ON UPDATE CASCADE ON DELETE RESTRICT,".format("fk_{0}_{1}".format(i.name,j.name),j.name,j.relation,self.get_table(j.relation).columns[0].name)
			commands=commands[0:-1]+");\n"
			
			# Insert in all rows
			commands+="INSERT INTO `{0}` (`{1}`) VALUES ".format(i.name, "`,`".join(k.name for k in i.columns))
			
			# Add rows
			for j in i.rows:
				commands+="({0}),".format(",".join(("'"+k.replace("'","''")+"'" if isinstance(k,str) else ("'"+str(k)+"'" if k != None else "NULL")) for k in j));
			commands=commands[0:-1]+";\n"
		return commands