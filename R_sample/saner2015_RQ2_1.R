########################
## SANER2015 RQ2
## @author:Yuki Ueda
## @createdOn:2015/10/15
########################
pdf("RQ2_1.pdf")


### Set data
num <- data.frame() # Init

# Input numOfPatchsets_1_Start10000-End70705_RQ2.csv for csv
num <- read.csv("R_sample/numOfPatchsets_1_Start10000-End70705_RQ2.csv"
                 ,sep=",", header=TRUE)

### number of patchset's voting(+1, -1) is 1
# index_l_m: vote is "like" and status is "merge"
# index_d_a: vote is "dislike" and status is abandoned
index_l_m <- data.frame()
index_l_a <- data.frame()
index_d_m <- data.frame()
index_d_a <- data.frame()

for(i in 1:nrow(num)){
  if(num$VotingScore[i] == 1){      # vote is like
    if(num$Status[i] == "merged"){  # status is merge
      index_l_m <- rbind(index_l_m, num[i,])
    }else{                          # status is abandoned
      index_l_a <- rbind(index_l_a, num[i,])
    }
  }else{                            # vote is dislike
    if(num$Status[i] == "merged"){
      index_d_m <- rbind(index_d_m, num[i,])
    }else{
      index_d_a <- rbind(index_d_a, num[i,])
    }
  }
}

# Output to PDF file
boxplot(index_l_m$CurrentPar, xlab="Reviewer order", ylab="Reliability", main="Vote:like Status:merge")
summary(index_l_m$CurrentPar)
boxplot(index_l_a$CurrentPar, xlab="Reviewer order", ylab="Reliability", main="Vote:like: Status:abandoned")
summary(index_l_a$CurrentPar)
boxplot(index_d_m$CurrentPar, xlab="Reviewer order", ylab="Reliability", main="Vote:dislike Status:merge")
summary(index_d_m$CurrentPar)
boxplot(index_d_a$CurrentPar, xlab="Reviewer order", ylab="Reliability", main="Vote:dislike Status:abandoned")
summary(index_d_a$CurrentPar)

dev.off()
