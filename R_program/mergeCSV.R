data1 <- data.frame()
data2 <- data.frame()
# data1 = read.csv("CSVdata_journal/example2.csv", sep=",", header=TRUE)
# data2 = read.csv("CSVdata_journal/example1.csv", sep=",", header=TRUE)
data1 = read.csv("CSVdata_journal/Qt2.csv", sep=",", header=TRUE)
data2 = read.csv("CSVdata_journal/expertiseLevel_qt.csv", sep=",", header=TRUE)

# merge Two data
output <- merge(x = data1, y = data2, by = c("ReviewId", "ReviewerId"), all.x = TRUE)

# convert NA to 0
output$ExpertiseLevel <- ifelse(is.na(output$ExpertiseLevel),0, output$ExpertiseLevel)

write.csv(output, "CSVdata_journal/merged_qt2.csv", row.names=FALSE, quote=FALSE)
