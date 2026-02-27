str1 = "Time"
str2 = "mInE"

#convert to same case
str1 = tolower(str1)
str2 = tolower(str2)

#create vector from string
str1Vect <- strsplit(str1, split = "")[[1]]
str2Vect <- strsplit(str2, split = "")[[1]]

numDiff<-sum(str1Vect!=str2Vect)

message("Hamming distance:", numDiff)
normHammDist = (numDiff/minLen)
message("Normalized hamming distance:",normHammDist )