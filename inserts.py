'''
Copyright (c) 2018, Miguel Liezun <liezun.js@gmail.com>

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
'''

import sys
import time


def processTable(table):
    name, *fields = table.split('\n')
    name = name\
        .replace('CREATE TABLE', '')\
        .replace('IF NOT EXISTS', '')\
        .replace('(', '')\
        .replace(' ', '')

    def fieldMap(field):
        field = field.split(' ')
        field = tuple(filter(lambda c: c != '', field))
        return (field[0], field[1])

    def filterField(field):
        for k in ['KEY', 'INDEX', 'REFERENCES', 'CONSTRAINT', 'ON DELETE', 'ON UPDATE']:
            if k in field:
                return False
        return len(field)

    fields = filter(filterField, fields)
    return name, dict(map(fieldMap, fields))


def genStr(x):
    from random import randrange
    s = ''
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKMLNOPQRSTUVWXYZ0123456789'
    for i in range(x):
        s += chars(randrange(len(chars)))
    return s


def genByTypes(n, fields):
    values = {}
    for field in fields:
        datatype = fields[field]
        for i in range(n):
            if i == 0:
                values[field] = []
            if 'INT' in datatype.upper():
                values[field].append(i)
            if 'DECIMAL' in datatype.upper():
                length = datatype.upper()\
                    .replace('DECIMAL', '')\
                    .replace('(', '')\
                    .replace(')', '')
                length = tuple(map(int, length.split(',')))
                values[field].append((length[0]-length[1])*str(i) + '.' + length[1]*str(i))
            if 'VARCHAR' in datatype.upper():
                length = datatype.upper()\
                    .replace('VARCHAR', '')\
                    .replace('(', '')\
                    .replace(')', '')\
                    .replace(',', '')
                length = int(length)
                if len(field) + len(str(i)) <= length:
                    values[field].append(field + str(i))
                else:
                    values[field].append(genStr(length))
            if 'TEXT' in datatype.upper():
                values[field].append(field + str(i))
            if 'CHAR(1)' in datatype.upper():
                values[field].append('A')
            if 'DATE' in datatype.upper():
                values[field].append(time.strftime('%Y-%m-%d %H:%M:%S'))
    return values


def mapValues(value):
    if type(value) == str:
        return f'"{value}"'
    elif type(value) == int:
        return f'{value}'
    return ''

def generateInserts(n, tables):
    for name in tables:
        inserts = [[] for i in range(n)]
        for values in genByTypes(n, tables[name]).values():
            for i in range(n):
                inserts[i].append(values[i])

        def mapInsert(values):
            start = f'INSERT INTO {name} SELECT '
            return start + ','.join(map(mapValues, values)) + ';'

        yield map(mapInsert, inserts)


def main(n, filepath):
    fd = open(filepath, 'r')
    lines = fd.readlines()
    tables = []
    start = False
    table = ''
    for line in lines:
        l = line.replace('`', '')
        if 'CREATE TABLE' in l:
            start = True
        if 'ENGINE' in l and start:
            tables.append(table)
            start = False
            table = ''
        if start:
            table += l
    tables = dict(map(processTable, tables))
    for tableInserts in generateInserts(int(n), tables):
        print('\n'.join(tableInserts))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: inserts.py n /path/to/script.sql')
    else:
        main(sys.argv[1], sys.argv[2])
