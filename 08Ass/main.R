library(stringr)
library(hash)

my_data <- read.csv("./babyNamesUSYOB-mostpopular.csv")
names_list <- as.character(my_data$Name)

cat("Enter a name to compare: ")
user_val <- readLines(con = "stdin", n = 1)

if (length(user_val) == 0 || user_val == "") {
  stop("No name entered. Execution halted.")
}
user_val <- tolower(trimws(user_val))

calc_jaro <- function(str1, str2) {
  str1 <- tolower(str1); str2 <- tolower(str2)
  if (str1 == str2) return(1.0)
  l1 <- nchar(str1); l2 <- nchar(str2)
  if (l1 == 0 || l2 == 0) return(0.0)
  
  max_dist <- floor(max(l1, l2) / 2) - 1
  match <- 0
  h1 <- hash(1:l1, 0); h2 <- hash(1:l2, 0)
  
  for (i in 1:l1) {
    start_j <- max(1, i - max_dist)
    end_j <- min(l2, i + max_dist)
    for (j in start_j:end_j) {
      if (str_sub(str1, i, i) == str_sub(str2, j, j) && h2[[as.character(j)]] == 0) {
        h1[as.character(i)] <- 1; h2[as.character(j)] <- 1
        match <- match + 1
        break
      }
    }
  }
  if (match == 0) return(0.0)
  t <- 0; point <- 1
  for (i in 1:l1) {
    if (h1[[as.character(i)]]) {
      while (h2[[as.character(point)]] == 0) { point <- point + 1 }
      if (str_sub(str1, i, i) != str_sub(str2, point, point)) { t <- t + 1 }
      point <- point + 1
    }
  }
  return((match/l1 + match/l2 + (match - t/2)/match) / 3.0)
}

calc_hamming <- function(str1, str2) {
  str1 <- tolower(str1); str2 <- tolower(str2)
  l1 <- nchar(str1); l2 <- nchar(str2)
  minL <- min(l1, l2)
  if (minL == 0) return(max(l1, l2))
  diffs <- 0
  for(i in 1:minL) {
    if (str_sub(str1, i, i) != str_sub(str2, i, i)) diffs <- diffs + 1
  }
  return(diffs)
}

calc_levenshtein <- function(str1, str2) {
  str1 <- tolower(str1); str2 <- tolower(str2)
  l1 <- nchar(str1); l2 <- nchar(str2)
  
  if (l1 == 0) return(l2)
  if (l2 == 0) return(l1)
  
  m <- matrix(0, nrow = l1 + 1, ncol = l2 + 1)
  m[,1] <- 0:l1
  m[1,] <- 0:l2
  
  for(c in 2:(l2 + 1)) {
    for(r in 2:(l1 + 1)) {
      if (str_sub(str1, r-1, r-1) == str_sub(str2, c-1, c-1)) {
        m[r, c] <- m[r-1, c-1]
      } else {
        m[r, c] <- 1 + min(m[r-1, c], m[r, c-1], m[r-1, c-1])
      }
    }
  }
  return(m[l1 + 1, l2 + 1])
}

cat("\nComparing '", user_val, "' against dataset:\n", sep="")
for (i in 1:min(100, length(names_list))) {
  target <- names_list[i]
  if (is.na(target)) next
  
  cat(sprintf("\nName: %s\n Jaro: %.4f | Hamming: %d | Levenshtein: %d\n", 
              target, calc_jaro(user_val, target), 
              calc_hamming(user_val, target), 
              calc_levenshtein(user_val, target)))
}
