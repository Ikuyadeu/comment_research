########################
## SANER2015 RQ2
## @author:Yuki Ueda
## @createdOn:2015/10/20
########################


### Set data
num <- data.frame() # Init

# Input numOfPatchsets_2_Start10000-End70705_RQ2.csv for csv
num <- read.csv("R_sample/numOfPatchsets_3_Start10000-End70705_RQ2.csv"
                 ,sep=",", header=TRUE)

### number of patchset's voting(+1, -1) is 1
# index_l_m: vote is "like" and status is "merge"
# index_d_a: vote is "dislike" and status is abandoned
index_l_m <- list(data.frame(), data.frame(), data.frame())
index_d_m <- list(data.frame(), data.frame(), data.frame())
index_l_a <- list(data.frame(), data.frame(), data.frame())
index_d_a <- list(data.frame(), data.frame(), data.frame())

for(i in 1:nrow(num)){
  CIndex = num$CommentIndex[i]      # CommentIndex
  if(num$Status[i] == "merged"){  # status is merge
    if(num$VotingScore[i] == 1){      # vote is like
      index_l_m[[CIndex]] <- rbind(index_l_m[[CIndex]], num[i,])
    }else{                          # vote is dislike
      index_d_m[[CIndex]] <- rbind(index_d_m[[CIndex]], num[i,])
    }
  }else{                            # status is abandoned
    if(num$VotingScore[i] == 1){
      index_l_a[[CIndex]] <- rbind(index_l_a[[CIndex]], num[i,])
    }else{
      index_d_a[[CIndex]] <- rbind(index_d_a[[CIndex]], num[i,])
    }
  }
}

# Summarize the index
index_merge <- list(index_l_m, index_d_m)
index_abondone <- list(index_l_a, index_d_a)
index <- list(index_abondone, index_merge)

# Output to PDF file
for(i in index){
  for(j in i){ # first Comment
    value1 = j[[1]]$CurrentPar
    for(k in i){ # second Comment
      value2 = k[[2]]$CurrentPar
      for(l in i){ # third Comment
        value3 = l[[3]]$CurrentPar
        name = paste("Vote:", j[[1]]$VotingScore[1], ",", k[[2]]$VotingScore[1], ",", l[[3]]$VotingScore[1], "Status:", j[[1]]$Status[1])
        jpeg(paste(name,".jpg"))
        boxplot(value1, value2, value3, xlab="Reviewer order", ylab="Reliability", main=paste("picture/",name))
        summary(value1)
        summary(value2)
        summary(value3)
      }
    }
  }
}
