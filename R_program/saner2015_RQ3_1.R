########################
## SANER2015 RQ3
## @author:Yuki Ueda
## @createdOn:2015/10/28
########################

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
  value = i$CurrentPar
  name = paste("Vote:", i$VotingScore[1],"Num:",length(value),sep="")
  print(name)
  result <- summary(value)

  threshold = result[['1st Qu.']] - 1.5 * IQR(value)
  value = subset(i, CurrentPar > threshold)$CurrentPar
  trueMin <- min(value)
  print(paste(result[['Median']],result[['1st Qu.']],trueMin,sep=","))
}
