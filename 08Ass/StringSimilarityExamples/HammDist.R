library(stringr)

str1 = "Time"
str2 = "mInE"

#convert to same case
str1 = tolower(str1)
str2 = tolower(str2)

#get min num characters
minLen = min(str_length(str1),str_length(str2))
print(minLen)

numDiff<-0

for(x in 1:minLen)
{
  #print(str_sub(str1,x,x))
  if (str_sub(str1,x,x) != str_sub(str2,x,x)) {
    numDiff = numDiff +1
  }
}

message("Hamming distance:", numDiff)
normHammDist = (numDiff/minLen)
message("Normalized hamming distance:",normHammDist )