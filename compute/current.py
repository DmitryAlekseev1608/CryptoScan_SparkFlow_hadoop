import datetime
import logging

from pyspark import SparkContext
from pyspark.sql import SparkSession
from tgbot.telegrambot import send_dataframe_to_telegram


def main():
    sc = SparkContext()
    spark = SparkSession(sc)
    cur_date = datetime.date.today()
    sdf = spark.read.option("mergeSchema", "true").parquet(f"result/DATA={cur_date}")
    df = sdf.toPandas()
    df = df[df["TIME"] == df["TIME"].max()]
    df["PRICE"] = df["PRICE"].apply(lambda x: x.replace(",", ".")).astype(float)

    df = df.assign(MIN=df.groupby(by=["SYMBOL"])["PRICE"].transform("min"))
    df = df.assign(MAX=df.groupby(by=["SYMBOL"])["PRICE"].transform("max"))
    df["DIFFER"] = df.apply(lambda row: row.MAX - row.MIN, axis=1)

    df = df[(df["MIN"] == df["PRICE"]) | (df["MAX"] == df["PRICE"])]
    df = df.drop_duplicates()

    df = df.sort_values(by=["DIFFER"], ignore_index=True, ascending=False)[:12]
    df = df[["TIME", "MARKET", "SYMBOL", "PRICE"]]

    send_dataframe_to_telegram(df)
    logging.info(df)


if __name__ == "__main__":
    main()
