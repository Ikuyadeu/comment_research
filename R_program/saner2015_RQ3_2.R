########################
## SANER2015 RQ3
## @author:Yuki Ueda
## @createdOn:2015/10/28
########################


### Set data
num <- data.frame() # Init

# Input csv
num <- read.csv("CSVdata_o/numOfPatchsets_2.csv"
                 ,sep=",", header=TRUE)

### number of patchset's voting(+1, -1) is 1
index <- list(list(data.frame(),data.frame()),list(data.frame(),data.frame()))

for(i in 1:nrow(num)){
  CIndex = num$CommentIndex[i]      # CommentIndex
  if(CIndex==1){
    if(num$VotingScore[i] == 1){
      vote1 = 1
    }else{
      vote1 = 2
    }
    next
  }

  if(num$VotingScore[i] == 1){
    vote2 = 1
  }else{
    vote2 = 2
  }

  index[[vote1]][[vote2]] <- rbind(index[[vote1]][[vote2]], num[i-1,])
  index[[vote1]][[vote2]] <- rbind(index[[vote1]][[vote2]], num[i,])
}

# Output to PDF file
for(i in index){ # first Comment
  for(j in i){  # second Comment
    value = j$CurrentPar
    name = paste("Vote:", j$VotingScore[1], ",", j$VotingScore[2], "Num:",length(j$CurrentPar),sep = "")
    print(name)
    result <- summary(value)

    threshold = result[['1st Qu.']] - 1.5 * IQR(value)
    value = subset(j, CurrentPar > threshold)$CurrentPar
    trueMin <- min(value)
    print(paste(result[['Median']],result[['1st Qu.']],trueMin,sep=","))
  }
}
