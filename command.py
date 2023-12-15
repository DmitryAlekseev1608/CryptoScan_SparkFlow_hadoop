import re
from multiprocessing import Process

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext

from api.parsing import parsing


def process_stream(record, spark):
    if not record.isEmpty():
        df = spark.createDataFrame(record)
        df = df.selectExpr("_1 as DATA", "_2 as TIME", "_3 as MARKET", "_4 as SYMBOL", "_5 as PRICE")
        df.repartition(2).write.mode("append").partitionBy("DATA", "SYMBOL").format("parquet").option(
            "compression", "snappy"
        ).save("/user/alekseevdo/result")
        df.show()


def start_spark():

    sc = SparkContext("local[*]", "cryptoscan")
    spark = SparkSession(sc)
    ssc = StreamingContext(sc, 1)
    inputStream = ssc.textFileStream("temp").map(lambda x: re.split(r"\s+", x))
    inputStream.foreachRDD(lambda rdd: process_stream(rdd, spark))
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
