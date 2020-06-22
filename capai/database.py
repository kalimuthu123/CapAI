import os
import re
from sqlalchemy import create_engine,inspect
from .constants import Color
from .table import Table

class Database:
    
    def __init__(self,uri):
        self.tables = []
        self.thesaurus_object = None
        self.engine = create_engine(uri)
        self.inspector = inspect(self.engine)

    def set_thesaurus(self, thesaurus):
        self.thesaurus_object = thesaurus

    def get_number_of_tables(self):
        return len(self.tables)

    def get_tables(self):
        return self.tables

    def get_column_with_this_name(self, name):
        for table in self.tables:
            for column in table.get_columns():
                if column.name == name:
                    return column

    def get_table_by_name(self, table_name):
        for table in self.tables:
            if table.name == table_name:
                return table

    def get_tables_into_dictionary(self):
        data = {}
        for table in self.tables:
            data[table.name] = []
            for column in table.get_columns():
                data[table.name].append(column.name)
        return data

    def get_primary_keys_by_table(self):
        data = {}
        for table in self.tables:
            data[table.name] = table.get_pk_keys()
        return data

    def get_foreign_keys_by_table(self):
        data = {}
        for table in self.tables:
            data[table.name] = table.get_fk_keys()
        return data

    def get_primary_keys_of_table(self, table_name):
        for table in self.tables:
            if table.name == table_name:
                return table.get_pk_keys()

    def get_primary_key_names_of_table(self, table_name):
        for table in self.tables:
            if table.name == table_name:
                return table.get_primary_key_names()

    def get_foreign_keys_of_table(self, table_name):
        for table in self.tables:
            if table.name == table_name:
                return table.get_fk_keys()

    def get_foreign_key_names_of_table(self, table_name):
        for table in self.tables:
            if table.name == table_name:
                return table.get_foreign_key_names()

    def add_table(self, table):
        self.tables.append(table)

    def load(self):
        inspector=self.inspector 
        for table_name in inspector.get_table_names():
            table=self.create_table(table_name)
            self.add_table(table)
            self.alter_table(table_name)

  
    def create_table(self, table_name):
        table = Table()
        inspector=self.inspector
        table.name = table_name
        if self.thesaurus_object is not None:
            table.equivalences = self.thesaurus_object.get_synonyms_of_a_word(table_name)
        for column_name in inspector.get_columns(table_name):
            if self.thesaurus_object is not None:
                equivalences = self.thesaurus_object.get_synonyms_of_a_word(column_name)
            else:
                equivalences = []
            table.add_column(column_name["name"], column_name["type"], equivalences)
        return table

    def alter_table(self, table_name):
        inspector=self.inspector
        table = self.get_table_by_name(table_name)
        for column in inspector.get_primary_keys(table_name):
            table.add_primary_key(column)
        for column in inspector.get_foreign_keys(table_name):
            table.add_foreign_key(column["constrained_columns"][0],column["referred_table"], column["referred_columns"][0])

    def print_me(self):
        for table in self.tables:
            #print("tab",table)
            print('+-------------------------------------+')
            print("| %25s           |" % (table.name.upper()))
            print('+-------------------------------------+')
            for column in table.columns:
                print(column.is_primary())
                if column.is_primary():
                    print("| 🔑 %31s           |" % (Color.BOLD + column.name + ' (' + ')' + Color.END))
                elif column.is_foreign():
                    print("| #️⃣ %31s           |" % (Color.ITALIC + column.name + ' (' + ')' + Color.END))
                else:
                    print("|   %23s           |" % (column.name +' (' + ')'))
            print('+-------------------------------------+\n')
