library(stringr)

#Levenshtein Distance
str1 = "man"
str2 = "wOMAN"

#convert to same case
str1 = tolower(str1)
str2 = tolower(str2)



m = matrix(0, nrow = str_length(str1)+1, ncol = str_length(str2)+1)
print(m)

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

print(m)


#for each Col
for(c in 1:str_length(str2)+1)
{
  #message("Looking at :",str_sub(str2,c-1,c-1))
  #for each row
  for(r in 1:str_length(str1)+1)
  {
    #print(str_sub(str1,r-1,r-1))
    
    # are the last characters the same
    if (str_sub(str1,r-1,r-1) == str_sub(str2,c-1,c-1)) 
    {
      m[r,c] = min(m[r,c-1]+1, m[r-1,c-1],m[r-1,c]+1) 
    }
    else
    {
      m[r,c] = min(m[r,c-1]+1, m[r-1,c-1]+1,m[r-1,c]+1) 
    }
    
  }
  
}  

print(m)


message("Levenshtein distance:", m[nchar(str1)+1,nchar(str2)+1])
