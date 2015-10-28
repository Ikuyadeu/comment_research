########################
## SANER2015 RQ2
## @author:Yuki Ueda
## @createdOn:2015/10/20
########################
#pdf("RQ2_2.pdf")


### Set data
num <- data.frame() # Init

# Input csv
num <- read.csv("CSVdata_o/numOfPatchsets_3.csv"
                 ,sep=",", header=TRUE)

### number of patchset's voting(+1, -1) is 1
index_1 <- data.frame() # first vote is like or dislike
index_2 <- list(index_1, index_1) # second vote is like or dislike
index <- list(index_2,index_2)

for(i in 1:nrow(num)){
  Id = num$ReviewId[i]
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
    print(result)

    threshold = result[['1st Qu.']] - 1.5 * IQR(value)
  }
}




### number of patchset's voting(+1, -1) is 1
index_1 <- data.frame() # first vote is like or dislike
index_2 <- list(index_1, index_1) # second vote is like or dislike
index <- list(index_2,index_2)

for(i in 1:nrow(num)){
  Id = num$ReviewId[i]
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

  if(num$CurrentPar[i-1] > threshold && num$CurrentPar[i] > threshold){
    index[[vote1]][[vote2]] <- rbind(index[[vote1]][[vote2]], num[i-1,])
    index[[vote1]][[vote2]] <- rbind(index[[vote1]][[vote2]], num[i,])
  }
}

# Output to PDF file
for(i in index){ # first Comment
  for(j in i){  # second Comment
    value = j$CurrentPar
    name = paste("Vote:", j$VotingScore[1], ",", j$VotingScore[2], "Num:",length(j$CurrentPar),sep = "")
    print(name)
    result <- min(value)
    print(result)
  }
}
