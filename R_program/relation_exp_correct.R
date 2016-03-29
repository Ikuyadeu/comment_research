reviewers <- data.frame()
reviewers <- read.csv("CSVdata_journal/Qt3.csv", sep = ",", header = TRUE)

# get idList more than 5 %(725 * 0.05)
# idlist <- data.frame()
# idlist <- read.csv("CSVdata_journal/reviewerList_BasedOn_freqOfReview.csv", sep = ",", header = TRUE)
# idlist <- head(idlist, n=nrow(idlist) * 0.05)
#
# reviewers <- data.frame()
# for(i in idlist$id){
#   reviewers <- rbind(reviewers, subset(reviewers1, reviewers1$ReviewerId == i))
# }

# each ExpertiseLevel
current <- data.frame()
incurrent <- data.frame()

current <- subset(reviewers, reviewers$IncurrentVote == 0)$CurrentChain
incurrent <- subset(reviewers, reviewers$IncurrentVote == 1)$CurrentChain

print(wilcox.test(current, incurrent))

pdf("pdf_journal/CurrentChain.pdf")
boxplot(current, incurrent, xlab="current vs incurrent", ylab="ExpertiseLevel")
