#!/usr/bin/env python
import csv
import os
import typer

app = typer.Typer()

RAW_PATH = 'raw'
EXPORT_PATH = 'export'

TEMPLATE = """
[settings]
initialized = True
name = coub-%s

[project]
description = COUB %s
url = https://coub.com//api/v2/timeline/community/%s/fresh
http_mode = GET
work_modes = full,incremental,update
iterate_by = page

[params]
page_size_param = per_page
page_size_limit = 10
page_number_param = page


[data]
pages_number_key = total_pages
data_key = coubs
item_key = id
change_key = id

[storage]
storage_type = zip
compression = True
"""

PARAMS_TEMPLATE = '{"page" : 1, "per_page": 10, "order_by" : "likes_count"}'

@app.command()
def prepare():
    f = open('communities.csv', 'r', encoding='utf8')
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        print(row['id'])
        os.makedirs(row['id'])
        filepath = os.path.join(RAW_PATH, row['id'], 'apibackuper.cfg')
        f = open(filepath, 'w', encoding='utf8')
        f.write(TEMPLATE % (row['id'], row['name'], row['id']))
        f.close()

        filepath = os.path.join(row['id'], 'params.json')
        f = open(filepath, 'w', encoding='utf8')
        f.write(PARAMS_TEMPLATE)
        f.close()

@app.command()
def collect():
    f = open('communities.csv', 'r', encoding='utf8')
    reader = csv.DictReader(f, delimiter=',')
    current = os.getcwd()
    for row in reader:
        print(row['id'])
        os.chdir(os.path.join(RAW_PATH, row['id']))
        os.system('apibackuper run')        
        os.chdir(current)


@app.command()
def export():
    f = open('communities.csv', 'r', encoding='utf8')
    reader = csv.DictReader(f, delimiter=',')
    current = os.getcwd()
    for row in reader:
        print(row['id'])
        os.chdir(os.path.join(RAW_PATH, row['id']))
        if not os.path.exists(os.path.join(EXPORT_PATH, row['id'] + '.jsonl.bz2')):
            os.system('apibackuper export jsonl ../../export/%s.jsonl' % (row['id']))        
            os.chdir(current)
            os.system('xz -9 %s' % (os.path.join(EXPORT_PATH, row['id'] + '.jsonl')))


pass

if __name__ == "__main__":
    app()
