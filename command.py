import os
import time

import pyspark
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext

from api.parsing import parsing


def main():
    df = parsing()
    sdf = df.to_spark()
    sdf.show(10)
    d = sdf.format("json").save(d)
    q = spark.readStream.schema("age INT, name STRING").format("json").load(d).writeStream.format("console").start()
    time.sleep(3)
    q.stop()

    # # Create a local StreamingContext with two working thread and batch interval of 1 second
    # sc = SparkContext("local[*]", "cryptoscan")
    # ssc = StreamingContext(sc, 30)


if __name__ == "__main__":
    spark = SparkSession.builder.appName("spark3.2show").getOrCreate()
    print("Spark info :")
    print("Version of pyspark :", pyspark.__version__)
    os.environ["PYARROW_IGNORE_TIMEZONE"] = "1"

    main()
