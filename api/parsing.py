import datetime
import threading
from queue import Queue
from subprocess import PIPE, Popen

import pandas as pd

import api.bybit.REST_Ticker as bybit
import api.gate_io.API_Gate_io as gate_io
import api.htx.API_HTX as htx
import api.kukoin.API_Kukoin as kukoin
import os
import stat


def parsing():
    while True:
        cur_date = datetime.date.today()
        cur_time = datetime.datetime.now().time().strftime("%H:%M")

        q1 = Queue()
        q2 = Queue()
        q3 = Queue()
        q4 = Queue()

        # init threads
        t1 = threading.Thread(target=bybit.get_data_from_endpoint, args=[q1, cur_date, cur_time])
        t2 = threading.Thread(target=gate_io.get_data_from_endpoint, args=[q2, cur_date, cur_time])
        t3 = threading.Thread(target=htx.get_data_from_endpoint, args=[q3, cur_date, cur_time])
        t4 = threading.Thread(target=kukoin.get_data_from_endpoint, args=[q4, cur_date, cur_time])

        # start threads
        t1.start()
        t2.start()
        t3.start()
        t4.start()

        # join threads to the main thread
        t1.join()
        t2.join()
        t3.join()
        t4.join()

        q1 = q1.get()
        q2 = q2.get()
        q3 = q3.get()
        q4 = q4.get()

        df1 = pd.DataFrame(q1)
        df2 = pd.DataFrame(q2)
        df3 = pd.DataFrame(q3)
        df4 = pd.DataFrame(q4)

        frames = [df1, df2, df3, df4]
        df = pd.concat(frames)

        df = df.assign(COUNT=df.groupby(by=["SYMBOL", "CASH"])["PRICE"].transform("count"))
        df = df[df.COUNT > 1]
        df = df[df["CASH"] == "USDT"]

        df = df.sort_values(by=["SYMBOL"], ignore_index=True, ascending=False)
        df = df[["DATA", "TIME", "MARKET", "SYMBOL", "PRICE"]]

        PATH1 = "/opt/hadoop/airflow/dags/alex_crypto/temp/market.txt"
        PATH2 = "/temp/market.txt"

        with open(PATH1, "w") as f:
            dfAsString = df.to_string(header=False, index=False, decimal=",") + "\n"
            f.write(dfAsString)

        os.chmod(PATH1, stat.S_IROTH)
        os.chmod(PATH1, stat.S_IWOTH)
        os.chmod(PATH1, stat.S_IXOTH)
        
        put = Popen(["hdfs", "dfs", "-put", "-f", PATH1, "/user/alekseevdo/temp/market.txt"], stdin=PIPE, bufsize=-1)
        put.communicate()

        while cur_time == datetime.datetime.now().time().strftime("%H:%M"):
            pass


if __name__ == "__main__":
    parsing()
