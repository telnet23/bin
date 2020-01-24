import sqlite3
import sys

primary = sys.argv[1]
secondary = sys.argv[2]
db = sqlite3.connect(primary)
db.execute(f'ATTACH "{secondary}" as secondary')
db.execute('BEGIN')
for row in db.execute('SELECT * FROM secondary.sqlite_master WHERE type = "table"'):
    name = row[1]
    if name.startswith('sqlite_'):
        continue
    create = row[4]
    create = create.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
    create = create.replace(', UNIQUE (id, service)', '')
    db.execute(create)
    replace = f'REPLACE INTO main.{name} SELECT * FROM secondary.{name}'
    db.execute(replace)
db.commit()
db.execute('DETACH DATABASE secondary')
