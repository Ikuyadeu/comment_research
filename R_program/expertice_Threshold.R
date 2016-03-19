reviewers <- data.frame()
reviewers <- read.csv("CSVdata_journal/merged_qt2.csv", sep = ",", header = TRUE)

DF <- data.frame(Threshold<-c(), Reliability<-c())

threshold = 0
while(threshold < 2){
	reviewers$futureIncurrent <- ifelse(reviewers$ExpertiseLevel < threshold, 1, 0)
	reliability <- nrow(subset(reviewers, reviewers$futureIncurrent == reviewers$IncurrentVote)) / nrow(reviewers)

	DF <- rbind(DF, data.frame(c(threshold), c(reliability)))
	threshold = threshold + 0.01
}

write.csv(reviewers, "CSVdata_journal/futureIncurrent.csv", row.names=FALSE, quote=FALSE)

pdf("expert.pdf")
plot(DF$c.threshold., DF$c.reliability., xlab="Threshold", ylab="Reliability", xlim=c(0.0, 2.0), ylim=c(0.0, 1.0))
