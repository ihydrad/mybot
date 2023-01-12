import pandas as pd
import io
import matplotlib.pyplot as plt
import numpy as np

from jobParser import JobParserDB


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

    cur_year_df = df[(df['Start'].dt.year == 2023)]
    plt.hist(cur_year_df['Start'].dt.month)

    buf = io.BytesIO()
    plt.grid()
    #plt.axis([0, 13, 0, 10])
    plt.xlabel("Месяц")
    plt.xticks(np.arange(1, 13, 1))
    plt.ylabel("Количество вакансий")
    plt.yticks(np.arange(0, 11, 1))
    plt.savefig(buf, format='png')
    buf.seek(0)

    return buf


if __name__ == "__main__":
    img = build_hist_year()

    with open("test.png", "wb") as f:
        f.write(img.getbuffer())
