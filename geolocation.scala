import org.apache.spark.sql._

val dataPath = "geodata/data.parquet.gzip"
val articlesPath = "geodata/articles.csv"

val data = spark.read.option("header", "true").parquet(dataPath)
val articles = spark.read.option("header", "true").csv(articlesPath)


val output = articles.join(data, Seq("string"), "inner")
output.show(20, False)
spark.write.csv("data/out.csv")
