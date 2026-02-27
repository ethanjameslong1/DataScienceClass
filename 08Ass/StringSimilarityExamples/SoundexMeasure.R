library(stringr)
library(hash)

#Soundex Mesaure
str1 = "Tymczak"
str2 = "Tymczak"

#convert to same case
str1 = tolower(str1)

#step 1
str2 = paste(str_sub(str2,1,1),gsub('a|e|i|u|y|h|w','0', str_sub(str2,2,str_length(str2))),sep='')

print(str2)

#step 2
firstLetter = str_sub(str2,1,1)
if ((firstLetter=="b") || (firstLetter=="f")||(firstLetter=="p") || (firstLetter=="v"))
{
  firstDigit = 2
} else if ((firstLetter=="c") || (firstLetter=="g")||(firstLetter=="j") || (firstLetter=="k")||(firstLetter=="q") || (firstLetter=="s")||(firstLetter=="x") || (firstLetter=="z"))
{
  firstDigit = 3
} else if ((firstLetter=="d") || (firstLetter=="t"))
{
  firstDigit = 3
} else if (firstLetter=="l")
{
  firstDigit = 4
}else if ((firstLetter=="m") || (firstLetter=="b"))
{
  firstDigit = 5
} else if (firstLetter=="r")
  firstDigit = 6
##print(firstLetter)
##print(firstDigit)

if (firstDigit != 1)
  str2 = gsub('b|f|p|v','1', str_sub(str2,1,str_length(str2)))
if (firstDigit != 2)
  str2 = gsub('c|g|j|k|q|s|x|z','2', str_sub(str2,1,str_length(str2)))
if (firstDigit != 3)
  str2 = gsub('d|t','3', str_sub(str2,1,str_length(str2)))
if (firstDigit != 4)
  str2 = gsub('l','4', str_sub(str2,1,str_length(str2)))
if (firstDigit != 5)
  str2 = gsub('m|n','5', str_sub(str2,1,str_length(str2)))
if (firstDigit != 6)
  str2 = gsub('r','6', str_sub(str2,1,str_length(str2)))

#print(str2)

#step 3
str2 = gsub('11','1', str_sub(str2,1,str_length(str2)))
str2 = gsub('22','2', str_sub(str2,1,str_length(str2)))
str2 = gsub('33','3', str_sub(str2,1,str_length(str2)))
str2 = gsub('44','4', str_sub(str2,1,str_length(str2)))
str2 = gsub('55','5', str_sub(str2,1,str_length(str2)))
str2 = gsub('66','6', str_sub(str2,1,str_length(str2)))
str2 = gsub('77','7', str_sub(str2,1,str_length(str2)))
str2 = gsub('88','8', str_sub(str2,1,str_length(str2)))
str2 = gsub('99','9', str_sub(str2,1,str_length(str2)))
#print(str2)

str2 = gsub('0','', str_sub(str2,1,str_length(str2)))


#print(str2)

#step 4
numDigits = str_count(str2,"[0-9]")
#print(numDigits)

if (numDigits<3)
  str2 = paste(str2,str_sub('000',1,numDigits-3),sep='')

str2 = str_sub(str2,1,4)

print(str2)
