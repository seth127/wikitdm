require(tm)
setwd("~/Documents/wikitdm")

wiki <- read.csv("wiki-test-5-IDF.csv")

text <- paste(readLines("hacking.txt"), collapse = '\n')

vct <- VCorpus(VectorSource(text))


tf <- termFreq(vct[[1]])


docs <- c("This is a text.", "This another one.")
vc <- VCorpus(VectorSource(docs))
