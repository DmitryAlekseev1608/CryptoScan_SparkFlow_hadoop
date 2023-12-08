import os

from time import sleep

import pyspark
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from api.parsing import parsing
import pandas as pd
from pyspark.sql import SQLContext
import multiprocessing

m = multiprocessing.Manager()
QUEUE_RDD = m.list()

def get_date(sqlContext):
    
    QUEUE_RDD = []
    while True:

        df = parsing()
        spDF = sqlContext.createDataFrame(data = df)
        rdd = spDF.rdd
        QUEUE_RDD += [rdd]

def start_spark(ssc):

    ssc.start()
    sleep(5)
    ssc.awaitTermination()

def main():
    
    QUEUE_RDD = []
    sc = SparkContext("local[*]", "cryptoscan")
    ssc = StreamingContext(sc, 5)
    sqlContext = SQLContext(sc)
    df = parsing()
    spDF = sqlContext.createDataFrame(data = df) 
    rdd = spDF.rdd
    QUEUE_RDD += [rdd]
    inputStream = ssc.queueStream(QUEUE_RDD)
    inputStream.pprint()

    p1 = multiprocessing.Process(target=get_date, args=[sqlContext])
    p1.start()
    p2 = multiprocessing.Process(target=start_spark, args=[ssc])
    p2.start()
    p1.join()
    p2.join()

if __name__ == "__main__":
    main()
