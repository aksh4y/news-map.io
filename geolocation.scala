import org.apache.spark.sql._

val dataPath = "data.csv"
val articlesPath = "articles.csv"

val data = spark.read.option("header", "true").csv(dataPath)
val articles = spark.read.option("header", "true").csv(articlesPath)


val output = articles.join(data, Seq("string"), "inner")
output.show(20, False)
spark.write.csv("out.csv")
