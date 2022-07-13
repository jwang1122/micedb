import sqlite3
import uuid
import pandas as pd

# miceDF = pd.read_csv('asm.csv')
miceDF = pd.read_csv('nlrp3.csv')

# print(miceDF)

# print(miceDF.columns)

conn = sqlite3.connect('mice.db')
c = conn.cursor()

vals = 'msid', 'gender', 'geno', 'dob.', 'ear', 'mom', 'dad', 'cage', 'usage', 'date'

sql = f"INSERT INTO mice VALUES (?{',?' * len(vals)}, ?)"

# loop
for i, data in enumerate(miceDF.iloc):
    # print(i, data['Ms ID'], data['Gender'])
    param = [uuid.uuid4().hex]
    for s in vals:
        if data[s] is None:
            param.append(None)
            continue
        param.append(f"{data[s]}")
    param.append('Nlrp3')
    c.execute(sql, param)
    conn.commit()

conn.close()

print("Done.")
