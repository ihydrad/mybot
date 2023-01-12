import pandas as pd
import io

from jobParser import JobParserDB
import matplotlib.pyplot as plt


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

def build_hist_year():
    db = JobParserDB("ufa")

    data = db.db_get_all_job()
    data = job_to_str(data)

    io_str_file = io.StringIO(data)

    df = pd.read_csv(io_str_file)
    df['Start'] = df['Start'].astype('datetime64[s]')
    df.sort_values(by="Start", inplace=True)

    plt.hist(df['Start'].dt.month, range=[1, 13])

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return buf

if __name__ == "__main__":
    img = build_hist_year()

    with open("test.png", "wb") as f:
        f.write(img.getbuffer())
    


