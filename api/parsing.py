import datetime
import threading
from queue import Queue

import pandas as pd

import api.bybit.REST_Ticker as bybit

# import gate_io.API_Gate_io as gate_io
import api.htx.API_HTX as htx
import api.kukoin.API_Kukoin as kukoin


def parsing():
    cur_date = datetime.date.today()
    cur_time = datetime.datetime.now().time().strftime("%H:%M")

    q1 = Queue()
    # q2 = Queue()
    q3 = Queue()
    q4 = Queue()

    # init threads
    t1 = threading.Thread(target=bybit.get_data_from_endpoint, args=[q1, cur_date, cur_time])
    # t2 = threading.Thread(target=gate_io.get_data_from_endpoint, args=[q2, cur_date, cur_time])
    t3 = threading.Thread(target=htx.get_data_from_endpoint, args=[q3, cur_date, cur_time])
    t4 = threading.Thread(target=kukoin.get_data_from_endpoint, args=[q4, cur_date, cur_time])

    # start threads
    t1.start()
    # t2.start()
    t3.start()
    t4.start()

    # join threads to the main thread
    t1.join()
    # t2.join()
    t3.join()
    t4.join()

    q1 = q1.get()
    # q2 = q2.get()
    q3 = q3.get()
    q4 = q4.get()

    df1 = pd.DataFrame(q1)
    df3 = pd.DataFrame(q3)
    df4 = pd.DataFrame(q4)

    frames = [df1, df3, df4]
    df = pd.concat(frames)

    df = df.assign(COUNT=df.groupby(by=["SYMBOL", "CASH"])["PRICE"].transform("count"))
    df = df[df.COUNT > 1]
    df = df.assign(MIN=df.groupby(by=["SYMBOL", "CASH"])["PRICE"].transform("min"))
    df = df.assign(MAX=df.groupby(by=["SYMBOL", "CASH"])["PRICE"].transform("max"))

    df["DIFFER"] = df.apply(lambda row: row.MAX - row.MIN, axis=1)
    df = df.sort_values(by=["DIFFER", "PRICE"], ignore_index=True, ascending=False)

    df = df.iloc[:12]
    df = df[["DATA", "TIME", "MARKET", "SYMBOL", "CASH", "PRICE"]]
    return df


if __name__ == "__main__":
    parsing()
