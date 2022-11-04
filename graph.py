import pandas as pd
import io

from jobParser import JobParserDB
import matplotlib.pyplot as plt

db = JobParserDB("ufa")
data = db.db_get_all_job()

def job_to_str(data):
    txt = "Name,Start,End\n"
    for item in data:
        try:
            _, name, start, end = item
            txt += f"{name},{start},{end}\n"
        except ValueError:
            _, name, start = item
            txt += f"{name},{start},None\n"
    
    return txt

data = job_to_str(data)

io_file = io.StringIO(data)
df = pd.read_csv(io_file)
df['Start'] = df['Start'].astype('datetime64[s]')
df.sort_values(by="Start", inplace=True)

plt.hist(df['Start'].dt.month, range=[1, 13])
plt.savefig('hist.png')


