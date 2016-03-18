reviewers1 <- data.frame()
reviewers1 <- read.csv("CSVdata_journal/merged_qt2.csv", sep = ",", header = TRUE)

# get idList more than 5 %(725 * 0.05)
idlist <- data.frame()
idlist <- read.csv("CSVdata_journal/reviewerList_BasedOn_freqOfReview.csv", sep = ",", header = TRUE)
idlist <- head(idlist, n=nrow(idlist) * 0.05)

reviewers <- data.frame()
# reviewers <- reviewers1
for(i in idlist$id){
  reviewers <- rbind(reviewers, subset(reviewers1, reviewers1$ReviewerId == i))
}

# each ExpertiseLevel
current <- data.frame()
incurrent <- data.frame()

current <- subset(reviewers, reviewers$IncurrentVote == 0, ExpertiseLevel)$ExpertiseLevel
incurrent <- subset(reviewers, reviewers$IncurrentVote == 1, ExpertiseLevel)$ExpertiseLevel

print(wilcox.test(current, incurrent))

pdf("jounal.pdf")
boxplot(current, incurrent, xlab="current vs incurrent", ylab="ExpertiseLevel")
