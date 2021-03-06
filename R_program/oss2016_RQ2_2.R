########################
## SANER2015 RQ2
## @author:Yuki Ueda
## @createdOn:2015/10/20
########################


### Set data
num <- data.frame() # Init

# Input csv
num <- read.csv("CSVdata_oss/numOfPatchsets_os_2.csv"
                 ,sep=",", header=TRUE)

### number of patchset's voting(+1, -1) is 1
index_1 <- list(data.frame(), data.frame()) # first vote is like or dislike
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

  index[[vote1]][[vote2]][[1]] <- rbind(index[[vote1]][[vote2]][[1]], num[i-1,])
  index[[vote1]][[vote2]][[2]] <- rbind(index[[vote1]][[vote2]][[2]], num[i,])
}

# Output to PDF file
for(i in index){
  for(j in i){ # first Comment
    value1 = j[[1]]$CurrentPar
    value2 = j[[2]]$CurrentPar
    name = paste("OS_2_", j[[1]]$VotingScore[1], j[[2]]$VotingScore[1], "_",length(value1),sep = "")
    pdf(paste("OSS_pdf/",name,".pdf",sep=""))
    boxplot(value1, value2, ylim=c(0,1))
    print(name)
  }
}
