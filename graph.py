
import pandas as pd
import io

from jobParser import JobParserDB

db = JobParserDB("ufa")

data_closed = db.db_get_all_closed_job()
data_opened = db.db_get_all_active_job()

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

data_closed.extend(data_opened)
data = job_to_str(data_closed)
print(data)

io_file = io.StringIO(data)
df = pd.read_csv(io_file)
#df['Start'] = df['Start'].astype('datetime64[s]')

df['Start'] = pd.to_datetime(df['Start'], unit='s', origin='unix')
df.sort_values(by="Start", inplace=True)
print(df[["Name", "Start"]])
