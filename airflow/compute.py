# df = df.assign(MIN=df.groupby(by=["SYMBOL", "CASH"])["PRICE"].transform("min"))
# df = df.assign(MAX=df.groupby(by=["SYMBOL", "CASH"])["PRICE"].transform("max"))
# df["DIFFER"] = df.apply(lambda row: row.MAX - row.MIN, axis=1)
