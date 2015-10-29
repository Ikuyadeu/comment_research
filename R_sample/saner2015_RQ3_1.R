########################
## SANER2015 RQ2
## @author:Yuki Ueda
## @createdOn:2015/10/15
########################
#pdf("RQ2_1.pdf")


### Set data
num <- data.frame() # Init

# Input csv
num <- read.csv("CSVdata_o/numOfPatchsets_1.csv"
                 ,sep=",", header=TRUE)

value = num$CurrentPar
result <- summary(value)
print(result)

threshold = result[['1st Qu.']] - 1.5 * IQR(value)

index <- data.frame()

for(i in 1:nrow(num)){
  if(num$CurrentPar[i] > threshold){
    index <- rbind(index, num[i,])
  }
}

value = index$CurrentPar
result <- min(value)
print(result)
