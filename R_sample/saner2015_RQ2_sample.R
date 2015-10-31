########################
## SANER2015 RQ2
## @author:Toshiki Hirao
## @createdOn:2015/10/15
########################

### Set data
# num1にnumOfPatchsets_1_Start10000-End70814_RQ2.csvをcsv形式で読込
# num2, num3も同様
num1 <- data.frame() #初期化
num2 <- data.frame()
num3 <- data.frame()

num1 <- read.csv("CSVdata_q/numOfPatchsets_1.csv"
                 ,sep=",", header=TRUE)
num2 <- read.csv("CSVdata_q/numOfPatchsets_2.csv"
                 ,sep=",", header=TRUE)
num3 <- read.csv("CSVdata_q/numOfPatchsets_2.csv"
                 ,sep=",", header=TRUE)

### Separate infomation by CommentIndex
# 3つのvotingコメントがあったパッチ情報(num3)に対して，CommentIndex別で3分割した．
# Index3_1: num3で，CommentIndex = 1の情報
# Index3_2: num3で，CommentIndex = 2の情報
# Index3_3: num3で，CommentIndex = 3の情報
index3_1 <- data.frame()
index3_2 <- data.frame()
index3_3 <- data.frame()

# nrow(num3)はnum3の行数を指す
for(i in 1:nrow(num3)){
  # もし，num3のi行目のCommentIndexが１, num3のi行目のStatusがMergedの場合を指す
  # ちなみに，num3$--- のドルマークの意味は，そのtableのある列を指定したい時に使用する
  if(num3$CommentIndex[i] == 1 && num3$Status[i] == "merged"){
    # index3_1にnum3のi行目を挿入する
    #   rbind()は指定した行を抽出する関数
    #   num3[i, ]はi行目のセル全体を指す
    #   ちなみに，num3[ ,j]はj列目のセル全体を指す
    index3_1 <- rbind(index3_1, num3[i,])
  }
}
###同様
for(i in 1:nrow(num3)){
  if(num3$CommentIndex[i] == 2 && num3$Status[i] == "merged"){
    index3_2 <- rbind(index3_2, num3[i,])
  }
}
###同様
for(i in 1:nrow(num3)){
  if(num3$CommentIndex[i] == 3 && num3$Status[i] == "merged"){
    index3_3 <- rbind(index3_3, num3[i,])
  }
}

# 箱ヒゲ図:boxplot(指定した指標分の箱ヒゲ図分布が出る)
boxplot(index3_1$CurrentPar, index3_2$CurrentPar, index3_3$CurrentPar, xlab="Reviewer order", ylab="Reliability")
# Wilcox.test: ウィルコクソン検定
wilcox.test(index3_1$CurrentPar, index3_2$CurrentPar, correct = FALSE)
wilcox.test(index3_2$CurrentPar, index3_3$CurrentPar, correct = FALSE)
wilcox.test(index3_3$CurrentPar, index3_1$CurrentPar, correct = FALSE)
# これは指定した指標の概要情報．ま，特に必要ないが，見てみると良い！
summary(index3_1$CurrentPar)
summary(index3_2$CurrentPar)
summary(index3_3$CurrentPar)

boxplot(index3_1$score, index3_2$score, index3_3$score)

### number of patchset's voting(+1, -1) is 2
index2_1 <- data.frame()
index2_2 <- data.frame()

for(i in 1:nrow(num2)){
  if(num2$CommentIndex[i] == 1){
    index2_1 <- rbind(index2_1, num2[i,])
  }
}
for(i in 1:nrow(num2)){
  if(num2$CommentIndex[i] == 2){
    index2_2 <- rbind(index2_2, num2[i,])
  }
}
boxplot(index2_1$CurrentPar, index2_2$CurrentPar, xlab="Reviewer order", ylab="Reliability")
wilcox.test(index2_1$CurrentPar, index2_2$CurrentPar)
summary(index2_1$CurrentPar)
summary(index2_2$CurrentPar)

### number of patchset's voting(+1, -1) is 1
index1_1 <- data.frame()

for(i in 1:nrow(num1)){
  if(num1$CommentIndex[i] == 1){
    index1_1 <- rbind(index1_1, num1[i,])
  }
}
boxplot(index1_1$CurrentPar, xlab="Reviewer order", ylab="Reliability")
summary(index1_1$CurrentPar)
