########################
## SANER2015 RQ2
## @author:Yuki Ueda
## @createdOn:2015/10/20
########################


### Set data
num <- data.frame() # Init

# Input csv
num <- read.csv("CSVdata_oss/numOfPatchsets_qt_3.csv"
                 ,sep=",", header=TRUE)

### number of patchset's voting(+1, -1) is 1
index_1 <- list(data.frame(), data.frame(), data.frame()) # first vote is like or dislike
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

  index[[vote1]][[vote2]][[vote3]][[1]] <- rbind(index[[vote1]][[vote2]][[vote3]][[1]], num[i-2,])
  index[[vote1]][[vote2]][[vote3]][[2]] <- rbind(index[[vote1]][[vote2]][[vote3]][[2]], num[i-1,])
  index[[vote1]][[vote2]][[vote3]][[3]] <- rbind(index[[vote1]][[vote2]][[vote3]][[3]], num[i,])
}

# Output to PDF file
for(i in index){
  for(j in i){ # first Comment
    for(k in j){ # second Comment
      value1 = k[[1]]$CurrentPar
      value2 = k[[2]]$CurrentPar
      value3 = k[[3]]$CurrentPar
      name = paste("QT_3_", k[[1]]$VotingScore[1], k[[2]]$VotingScore[1], k[[3]]$VotingScore[1], "_",length(value1),sep = "")
      pdf(paste("OSS_pdf/",name,".pdf",sep=""))
      boxplot(value1, value2,  value3, ylim=c(0,1))
      print(name)
    }
  }
}
