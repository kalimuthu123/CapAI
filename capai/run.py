"""import MySQLdb 
hostname="localhost"
username="root"
password="mysqlroot"
database="blk_superset"
db_connection = MySQLdb.connect( host=hostname, user=username, passwd=password, db=database )
print("Connected") 
# Making Cursor Object For Query Execution 
cursor=db_connection.cursor() 
print(cursor.execute("SHOW TABLES;"))

cursor.execute("SHOW TABLES;")
##print("table",cursor.fetchall())
for table_name in cursor:
    print(table_name)

cursor.execute("SHOW COLUMNS FROM  ab_permission_view;")
cursor.execute("SHOW INDEX FROM ab_permission_view WHERE Key_name = 'PRIMARY';")"""

from sqlalchemy import create_engine,inspect
engine = create_engine("mysql://root:mysqlroot@localhost/blk_superset",echo = True)
print (len(engine.table_names()))
for table_name in engine.table_names():
    print(table_name)
inspector = inspect(engine)
schemas = inspector.get_schema_names()

for column in inspector.get_foreign_keys("ab_permission_view", schema="blk_superset"):
           print("Column: %s" % column)

"""for column in inspector.get_unique_constraints("ab_permission_view", schema="blk_superset"):
           print("Column: %s" % column)
for column in inspector.get_indexes("ab_permission_view", schema="blk_superset"):
           print("Column: %s" % column)
for column in inspector.get_pk_constraint("ab_permission_view", schema="blk_superset"):
           print("Column: %s" % column)
for column in inspector.get_primary_keys("ab_permission_view", schema="blk_superset"):
           print("Column: %s" % column)
for column in inspector.get_foreign_keys("ab_permission_view", schema="blk_superset"):
           print("Column: %s" % column)"""

"""for schema in schemas:
    print("schema: %s" % schema)
    for table_name in inspector.get_table_names(schema=schema):
        print("table_name: %s" % table_name)
        for column in inspector.get_columns(table_name, schema=schema):
           print("Column: %s" % column)"""
