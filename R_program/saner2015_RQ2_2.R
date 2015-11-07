########################
## SANER2015 RQ2
## @author:Yuki Ueda
## @createdOn:2015/10/20
########################
#pdf("RQ2_2.pdf")


### Set data
num <- data.frame() # Init

# Input csv
num <- read.csv("CSVdata_q/numOfPatchsets_2.csv"
                 ,sep=",", header=TRUE)

### number of patchset's voting(+1, -1) is 1
index_1 <- list(data.frame(), data.frame()) # first vote is like or dislike
index_2 <- list(index_1, index_1) # second vote is like or dislike
index_m <- list(index_2, index_2) # merge or abandoned
index <- list(index_m,index_m)

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

  if(num$Status[i] == "merged"){
    merge_or_abandone = 1
  }else{
    merge_or_abandone = 2
  }

  if(num$VotingScore[i] == 1){
    vote2 = 1
  }else{
    vote2 = 2
  }

  index[[merge_or_abandone]][[vote1]][[vote2]][[1]] <- rbind(index[[merge_or_abandone]][[vote1]][[vote2]][[1]], num[i-1,])
  index[[merge_or_abandone]][[vote1]][[vote2]][[2]] <- rbind(index[[merge_or_abandone]][[vote1]][[vote2]][[2]], num[i,])
}

# Output to PDF file
for(i in index){
  for(j in i){ # first Comment
    for(k in j){ # second Comment
      value1 = k[[1]]$CurrentPar
      value2 = k[[2]]$CurrentPar
      name = paste("Vote:", k[[1]]$VotingScore[1], ",", k[[2]]$VotingScore[1], "Status:", k[[1]]$Status[1],"Num:",length(value1),sep = "")
      jpeg(paste("picture_q/RQ2_2",name,".jpg",sep=""))
      boxplot(value1, value2, xlab="Reviewer order", ylab="Reliability", ylim=c(0,1))
      print(name)
    }
  }
}
