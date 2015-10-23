########################
## SANER2015 RQ2
## @author:Yuki Ueda
## @createdOn:2015/10/15
########################
#pdf("RQ2_1.pdf")


### Set data
num <- data.frame() # Init

# Input csv
num <- read.csv("CSVdata/numOfPatchsets_1.csv"
                 ,sep=",", header=TRUE)

### number of patchset's voting(+1, -1) is 1
# index_l_m: vote is "like" and status is "merge"
# index_d_a: vote is "dislike" and status is abandoned
index_l_m <- data.frame()
index_d_m <- data.frame()
index_l_a <- data.frame()
index_d_a <- data.frame()

for(i in 1:nrow(num)){
  if(num$Status[i] == "merged"){      # status is merge
    if(num$VotingScore[i] == 1){      # vote is like
      index_l_m <- rbind(index_l_m, num[i,])
    }else{                            # vote is dislike
      index_d_m <- rbind(index_d_m, num[i,])
    }
  }else{                              # status is abandoned
    if(num$VotingScore[i] == 1){      # vote is like
      index_l_a <- rbind(index_l_a, num[i,])
    }else{
      index_d_a <- rbind(index_d_a, num[i,])
    }
  }
}

index_merge <- list(index_l_m, index_d_m)
index_abondone <- list(index_l_a, index_d_a)
index <- list(index_abondone, index_merge)

for(i in index){
  for(j in i){
    value = j$CurrentPar
    name = paste("Vote:", j$VotingScore[1], "Status:", j$Status[1],"Num:",length(value),sep="")
    jpeg(paste("picture_o/RQ1",name,".jpg",sep=""))
    boxplot(value, xlab="Reviewer order", ylab="Reliability", main=name)
    summary(value)
  }
}
