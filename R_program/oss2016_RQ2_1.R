########################
## SANER2015 RQ2
## @author:Yuki Ueda
## @createdOn:2015/10/15
########################


### Set data
num <- data.frame() # Init

# Input csv
num <- read.csv("CSVdata_oss/numOfPatchsets_os_1.csv"
                 ,sep=",", header=TRUE)

### number of patchset's voting(+1, -1) is 1
# index_l_m: vote is "like" and status is "merge"
# index_d_a: vote is "dislike" and status is abandoned
index_l <- data.frame()
index_d <- data.frame()

for(i in 1:nrow(num)){
  if(num$VotingScore[i] == 1){      # vote is like
    index_l <- rbind(index_l, num[i,])
  }else{                            # vote is dislike
    index_d <- rbind(index_d, num[i,])
  }
}

index <- list(index_l, index_d)

for(i in index){
  value = i$CurrentPar
  name = paste("OS_1_", i$VotingScore[1], "_",length(value),sep = "")
  pdf(paste("OSS_pdf/",name,".pdf",sep=""))
  boxplot(value, ylim=c(0,1))
  print(name)
}
