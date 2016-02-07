#########################################
#              database.py              #
# Contains classes related to database  #
#               structure               #
#########################################


# Column of a table
class Column:	
	# constructor
	def __init__(self, name, datatype, pk=None, fk=None, relation=None, not_null=None, unique=None):
		# General column info
		self.name = name
		self.datatype = datatype  # e.g VARCHAR, int, float

		# Keys
		self.pk = False if pk is None else pk
		self.fk = False if fk is None else fk
		self.relation = relation

		# Default
		self.not_null = True if not_null is None else not_null
		self.unique = False if unique is None else unique
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
			if self.columns[i].name == column:
				break
		return self.rows[row][i]

	# Setters and adders
	def add_row(self, row):
		assert len(row) == len(self.columns)
		self.rows.append(row)

	def add_columns(self, column):
		self.columns.append(column)

	def set_columns(self, columns):
		self.columns = columns


class Database:
	# Constructor
	def __init__(self, name=None):
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

	# Export SQL
	def to_sql(self):
		commands = ""
		# Cycle through tables
		for i in self.tables:
			commands += "CREATE TABLE IF NOT EXISTS `"+i.name+"`("

			# Add column names
			f_keys = []  # foreign key list
			p_keys = []  # primary key list
			for j in i.columns:
				commands += "`{0}` {1}{2}{3},".format(j.name, j.datatype, (" NOT NULL" if j.not_null else ""),
													  (" UNIQUE" if j.unique else ""))
				# Add to foreign key list
				if j.fk:
					f_keys.append(j)
				if j.pk:
					p_keys.append(j)


			# Add foreign keys
			for j in f_keys:
				commands += "FOREIGN KEY {0}({1}) REFERENCES {2}({3}) ON UPDATE CASCADE ON DELETE RESTRICT,".\
					format("fk_{0}_{1}".format(i.name, j.name), j.name, j.relation,
						   self.get_table(j.relation).columns[0].name)

			# Add primary key
			commands += "PRIMARY KEY("
			for j in p_keys:
				commands += j.name + ","
			commands = commands[0:-1]+"));\n\n"

			# Insert in all rows
			commands += "INSERT INTO `{0}` (`{1}`) VALUES ".format(i.name, "`,`".join(k.name for k in i.columns))

			# Add rows
			for j in i.rows:
				commands += "({0}),".format(",".join(("'"+k.replace("'", "''")+"'" if isinstance(k, str)
													 else ("'"+str(k)+"'" if k is not None else "NULL")) for k in j))
			commands = commands[0:-1]+";\n\n"
		return commands
