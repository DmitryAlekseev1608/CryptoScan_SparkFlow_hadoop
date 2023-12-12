import datetime
import logging

from pyspark import SparkContext
from pyspark.sql import SparkSession


def main():
    sc = SparkContext()
    spark = SparkSession(sc)
    cur_date = datetime.date.today()
    sdf = spark.read.option("mergeSchema", "true").parquet(f"result/DATA={cur_date}")
    df = sdf.toPandas()
    df["PRICE"] = df["PRICE"].apply(lambda x: x.replace(",", ".")).astype(float)
    df = df.drop_duplicates()
    df = df.sort_values(by=["SYMBOL", "TIME"], ignore_index=True, ascending=False)
    df = df[["TIME", "MARKET", "SYMBOL", "PRICE"]]

    current_time = datetime.datetime.now()
    df["TIME"] = df["TIME"].astype(str)
    df["TIME"] = df["TIME"].apply(lambda x: f"{current_time.year}-{current_time.month}-{current_time.day}T{x}:00Z")

    df.to_csv("data/result.csv", index=False)
    print(df)
    logging.info(df)


if __name__ == "__main__":
    main()
