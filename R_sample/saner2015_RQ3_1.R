########################
## SANER2015 RQ2
## @author:Yuki Ueda
## @createdOn:2015/10/15
########################
#pdf("RQ2_1.pdf")


### Set data
num <- data.frame() # Init

# Input csv
num <- read.csv("CSVdata_o/numOfPatchsets_1.csv"
                 ,sep=",", header=TRUE)

### number of patchset's voting(+1, -1) is 1
# index_like: vote is "like"
# index_dislike_a: vote is "dislike"
index_like <- data.frame()
index_dislike <- data.frame()


for(i in 1:nrow(num)){
  if(num$VotingScore[i] == 1){      # vote is like
    index_like <- rbind(index_like, num[i,])
  }else{                            # vote is dislike
    index_dislike <- rbind(index_dislike, num[i,])
  }
}

index <- list(index_like, index_dislike)

for(i in index){
  #value = i$CurrentPar
  #name = paste("Vote:", i$VotingScore[1], "Status:", i$Status[1],"Num:",length(value),sep="")
  #jpeg(paste("pictureRQ3_q/RQ3_1",name,".jpg",sep=""))
  #boxplot(value, xlab="Reviewer order", ylab="Reliability", main=name, ylim=c(0,1))
  cat(i$VotingScore[1])
  print(summary(i$CurrentPar))
}
