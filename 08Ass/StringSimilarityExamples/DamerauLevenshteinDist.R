library(stringr)

#Damerau Levenshtein Distance
str1 = "sitting"
str2 = "kitten"

#convert to same case
str1 = tolower(str1)
str2 = tolower(str2)



m = matrix(0, nrow = str_length(str1)+1, ncol = str_length(str2)+1)
##print(m)

#first row
for(x in 1:str_length(str2)+1)
{
  m[1,x] = x-1
}

#first Col
for(x in 1:str_length(str1)+1)
{
  m[x,1] = x-1
}

##print(m)


#for each Col
for(c in 1:str_length(str2)+1)
{

  #for each row
  for(r in 1:str_length(str1)+1)
  {
   
    ##print(str_sub(str1,r,r)) 
    ##print(str_sub(str1,c,c)) 
    # are the last characters the same
    if (str_sub(str1,r,r) == str_sub(str2,c,c))
      m[r,c] = m[r-1,c-1] 
    else
      m[r, c] = 1 + min(m[r-1, c] + 1,            # deletion
                       m[r, c-1] + 1,        # insertion
                       m[r-1, c-1])   # substitution
    
  }
  ##print(m)
  
}  

print(m)


message("Damerau Levenshtein distance:", m[nchar(str1)+1,nchar(str2)+1])
