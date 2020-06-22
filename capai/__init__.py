from .capai import main as __main__
import re
import os
from .settings import DEBUG

def getSql(query, sqlUri, outputFile=None):
    # unit test
    # args = ['-d', 'capai/emp_dump.sql', '-l', 'capai/lang/english.csv', '-i', query, '-j', 'capai/output.json','-x']
    # args = ['-d', 'capai/emp_dump.sql', 'capai/lang/english.csv', '-i', query, '-j', 'capai/output.json']
    # args = ['-d', 'capai/timesheet.sql', '-l', 'capai/lang/english.csv', '-i', query, '-j', 'capai/output.json']

    args = ['-d', sqlUri,
            #'-l', os.path.dirname(os.path.abspath(__file__)
             #                     ) + '/lang/english.csv',
            '-i', query,
            '-j', outputFile]

    sql = __main__(args)

    return str(sql)

def getSql_like(query, sqlUri, outputFile=None):
    sql = getSql(query, sqlUri, outputFile)

    sql = re.sub("(WHERE \S+ )=", r'\g<1>LIKE', sql)
    sql = re.sub("(AND \S+ )=", r'\g<1>LIKE', sql)
    sql = re.sub("(OR \S+ )=", r'\g<1>LIKE', sql)

    # 'abc def' -> '%abc%def%'
    for i in re.findall("'(.*?)'", sql):
        sql = sql.replace(i, "%" + i + "%")
        sql = sql.replace(i, i.replace(' ', '%'))

    return sql
