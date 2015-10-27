########################
## SANER2015 RQ2
## @author:Yuki Ueda
## @createdOn:2015/10/20
########################
#pdf("RQ2_2.pdf")


### Set data
num <- data.frame() # Init

# Input csv
num <- read.csv("CSVdata_q/numOfPatchsets_3.csv"
                 ,sep=",", header=TRUE)

### number of patchset's voting(+1, -1) is 1
index_1 <- data.frame() # first vote is like or dislike
index_2 <- list(index_1, index_1) # second vote is like or dislike
index_3 <- list(index_2, index_2)
index <- list(index_3,index_3)

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
  }else if(CIndex==2){
    if(num$VotingScore[i] == 1){
      vote2 = 1
    }else{
      vote2 = 2
    }
    next
  }

  if(num$VotingScore[i] == 1){
    vote3 = 1
  }else{
    vote3 = 2
  }

  index[[vote1]][[vote2]][[vote3]] <- rbind(index[[vote1]][[vote2]][[vote3]], num[i-2,])
  index[[vote1]][[vote2]][[vote3]] <- rbind(index[[vote1]][[vote2]][[vote3]], num[i-1,])
  index[[vote1]][[vote2]][[vote3]] <- rbind(index[[vote1]][[vote2]][[vote3]], num[i,])
}

# Output to PDF file
for(i in index){ # first Comment
  for(j in i){  # second Comment
    for(k in j){
      name = paste("Vote:", k$VotingScore[1], ",", k$VotingScore[2], ",", k$VotingScore[3],"Num:",length(k$CurrentPar),sep = "")
      print(name)
      print(summary(k$CurrentPar))
    }
  }
}
