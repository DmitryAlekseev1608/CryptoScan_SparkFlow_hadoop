from multiprocessing import Process

import pandas as pd
import pyspark
import tqdm
from pyspark import SparkContext
from pyspark.sql import SparkSession, SQLContext
from pyspark.streaming import StreamingContext

from api.parsing import parsing


def start_spark():
    sc = SparkContext("local[*]", "cryptoscan")
    ssc = StreamingContext(sc, 3)
    inputStream = ssc.textFileStream("temp")
    inputStream.pprint()
    ssc.start()
    ssc.awaitTermination()


def main():
    p_pars = Process(target=parsing)
    p_spark = Process(target=start_spark)
    p_pars.start()
    p_spark.start()
    p_pars.join()
    p_spark.join()


if __name__ == "__main__":
    main()
