#!/usr/bin/python3
import argparse
import os
import getopt
from .database import Database
from .langConfig import LangConfig
from .parser import Parser
from .stopwordFilter import StopwordFilter
from .thesaurus import Thesaurus
from .constants import Color, without_color
from .settings import DEBUG

class capai:
    def __init__(
            self,
            database_path,
            language_path,
            json_output_path=None,
            thesaurus_path=None,
            stopwords_path=None,
            color=False
    ):
        if color == False:
            without_color()

        database = Database(database_path)
        self.stopwordsFilter = None
        language_path = os.path.dirname(os.path.abspath(__file__)) + '/lang_store/english.csv'
        if thesaurus_path:
            thesaurus = Thesaurus()
            thesaurus.load(thesaurus_path)
            database.set_thesaurus(thesaurus)

        if stopwords_path:
            self.stopwordsFilter = StopwordFilter()
            self.stopwordsFilter.load(stopwords_path)

        database.load()
        #database.print_me()
        config = LangConfig()
        config.load(language_path)

        self.parser = Parser(database, config)
        self.json_output_path = json_output_path

    def get_query(self, input_sentence):
        queries = self.parser.parse_sentence(input_sentence, self.stopwordsFilter)

        if self.json_output_path:
            self.remove_json(self.json_output_path)
            for query in queries:
                query.print_json(self.json_output_path)

        full_query = ''

        for query in queries:
            full_query += str(query)
            print(query)

        return full_query

    def remove_json(self, filename="output.json"):
        if os.path.exists(filename):
            os.remove(filename)

def print_help_message():
    if DEBUG :
        print ('\n')
        print ('Usage:')
        print ('\tpython capai.py -d <path> -l <path> -i <input-sentence> [-t <path>] [-j <path>]')
        print ('Parameters:')
        print ('\t-h\t\t\tprint this help message')
        print ('\t-d <path>\t\tpath to SQL schema')
        print ('\t-l <path>\t\tpath to language configuration file')
        print ('\t-i <input-sentence>\tinput sentence to parse')
        print ('\t-j <path>\t\tpath to JSON output file')
        print ('\t-t <path>\t\tpath to thesaurus file')
        print ('\n')


def main(argv):
    # try:
    opts, args = getopt.getopt(argv,"d:l:i:t:j:")
    database_path = None
    input_sentence = None
    language_path = os.path.dirname(os.path.abspath(__file__)) + '/lang_store/english.csv',
    thesaurus_path = None
    json_output_path = None

    for i in range(0, len(opts)):
        if opts[i][0] == "-d":
            database_path = opts[i][1]
        #elif opts[i][0] == "-l":
            #language_path = opts[i][1]
        elif opts[i][0] == "-i":
            input_sentence = opts[i][1]
        elif opts[i][0] == "-j":
            json_output_path = opts[i][1]
        elif opts[i][0] == "-t":
            thesaurus_path = opts[i][1]
        else:
            print_help_message()
            # sys.exit()
            raise getopt.GetoptError('capai : Invalid args received',None)
    
    if (database_path is None) or (input_sentence is None) or (language_path is None):
        raise getopt.GetoptError('capai : Invalid args received',None)
    else:
        if thesaurus_path is not None:
            thesaurus_path = str(thesaurus_path)
        if json_output_path is not None:
            json_output_path = str(json_output_path)

    #try:
    ln2sqlObj = capai(str(database_path), str(language_path), thesaurus_path, json_output_path) 
    
    return ln2sqlObj.get_query(str(input_sentence))
    #except Exception, e:
    #    print color.BOLD + color.RED + str(e) + color.END

    # except getopt.GetoptError:
    #     print_help_message()


# if __name__ == '__main__':
#     main(sys.argv[1:])
