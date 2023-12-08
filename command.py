import os
from time import sleep
import pyspark
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from api.parsing import parsing
import pandas as pd
from pyspark.sql import SQLContext
import tqdm

def main():

    while True:
        sc = SparkContext("local[*]", "cryptoscan")
        ssc = StreamingContext(sc, 3)      
        queue_rdd = []      
        sqlContext = SQLContext(sc)
        for _ in tqdm.tqdm(range(3)):
            df = parsing()
            spDF = sqlContext.createDataFrame(data = df)
            rdd = spDF.rdd
            queue_rdd += [rdd]
        inputStream = ssc.queueStream(queue_rdd)
        inputStream.pprint()
        ssc.start()
        ssc.stop(stopSparkContext=True, stopGraceFully=True)

if __name__ == "__main__":
    main()
