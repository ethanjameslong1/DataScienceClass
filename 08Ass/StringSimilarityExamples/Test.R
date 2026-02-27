library(stringr)
library(hash)

#Damerau Levenshtein Distance
str1 = "sittin"
str2 = "kitten"

#convert to same case
str1 = tolower(str1)
str2 = tolower(str2)

len1 = str_length(str1)
len2 = str_length(str2)
  
# Maximum distance upto which matching
# is allowed
max_dist = floor(max(len1, len2) / 2) - 1
  
# Count of matches
match = 0
  
# Hash for matches
hash_s1 = hash(1:len1,0)
hash_s2 = hash(1:len2,0 )
  
print(hash_s1)

print(hash_s1[as.character(1)])
