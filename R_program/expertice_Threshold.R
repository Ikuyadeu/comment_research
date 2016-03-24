reviewers <- data.frame()
reviewers <- read.csv("CSVdata_journal/merged_qt2.csv", sep = ",", header = TRUE)

DF <- data.frame(Threshold<-c(), Precision<-c(), Recall<-c(), TNrate<-c(), Accuracy<-c(), fm<-c())

threshold = 0
while(threshold < 4){
	reviewers$futureIncurrent <- ifelse(reviewers$ExpertiseLevel < threshold, 1, 0)

	# positive is prediction reviewer will incurrent
	positive <- subset(reviewers, reviewers$futureIncurrent == 1)
	negative <- subset(reviewers, reviewers$futureIncurrent == 0)

	# tp is prediction incurrent and real incurrent
	tp = nrow(subset(positive, positive$IncurrentVote == 1))
	fp = nrow(subset(positive, positive$IncurrentVote == 0))
	tn = nrow(subset(negative, negative$IncurrentVote == 1))
	fn = nrow(subset(negative, negative$IncurrentVote == 0))

	precision <- ifelse(tp+fp==0, 0, tp / (tp + fp))
	recall <- ifelse(tp+fn==0, 0, tp / (tp + fn))
	TNrate <- ifelse(tn+fp==0, 0, tn / (tn + fp))
	Accuracy <- ifelse(tp+tn+fp+fn==0, 0, (tp + tn) / (tp + tn + fp + fn))
	f <-  ifelse(recall+precision==0, 0,  2 * recall * precision / (recall + precision))

	DF <- rbind(DF, data.frame(c(threshold), c(precision), c(recall), c(TNrate), c(Accuracy), c(f)))
	threshold = threshold + 0.05
}

write.csv(reviewers, "CSVdata_journal/futureIncurrent.csv", row.names=FALSE, quote=FALSE)

pdf("pdf_journal/Precision.pdf")
plot(DF$c.threshold., DF$c.precision., xlab="Threshold", ylab="Precision", xlim=c(0.0, 4.0), ylim=c(0.0, 1.0))

pdf("pdf_journal/Recall.pdf")
plot(DF$c.threshold., DF$c.recall., xlab="Threshold", ylab="Recall", xlim=c(0.0, 4.0), ylim=c(0.0, 1.0))

pdf("pdf_journal/TNrate.pdf")
plot(DF$c.threshold., DF$c.TNrate., xlab="Threshold", ylab="TNrate", xlim=c(0.0, 4.0), ylim=c(0.0, 1.0))

pdf("pdf_journal/Accuracy.pdf")
plot(DF$c.threshold., DF$c.Accuracy., xlab="Threshold", ylab="Accuracy", xlim=c(0.0, 4.0), ylim=c(0.0, 1.0))


pdf("pdf_journal/f.pdf")
plot(DF$c.threshold., DF$c.f., xlab="Threshold", ylab="f", xlim=c(0.0, 4.0), ylim=c(0.0, 1.0))
