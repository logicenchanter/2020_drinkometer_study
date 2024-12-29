# In order to import baseline data into R: 
# - export Excel data as a baseline.csv file with semicolon separating columns
# save the baseline.csv file in the R's working directory - if necessary, check the working directory by running getwd()
# the code below assumes comma as a decimal sign
rm(list = ls())
baseline <- read.csv("~/baseline_f.csv", header = TRUE)


# treatment groups

n <- nrow(baseline) 
groupA <- trunc(nrow(baseline)/2)
groupB <- nrow(baseline) - groupA
groups <- c(groupA, groupB)
conn <- sample(groups, 1)
expn <- nrow(baseline) - conn

# vector for recording between-group differences in baseline parameters
diff <- vector()

# the loop stops after the first allocation solution is found where each of the 9 baseline criteria are met 
# (i.e. difference between Group A and Group B is less than 0.3)

for (i in 1:1000) {
  rows <- sample(nrow(baseline))
  baseline <- baseline[rows, ]
  
  for (j in 2:10) {
    diff[j] <- abs((mean(baseline[c(1:conn),j]) - mean(baseline[c(conn:n),j])))
  }

  if (all(diff < 0.3, na.rm = TRUE)) {
    print("Allocation successful")
    break
  }
}
baseline$Group <- c(rep("Control", times = conn), rep("Experimental", times = expn))

# baseline[order(baseline$Subj),]

# Change to write.csv in case “.” should be used for the decimal point and a comma (“,”) for the separator.
# write.csv2() uses a comma (“,”) for the decimal point and a semicolon (“;”) for the separator.
library(openxlsx)

write.xlsx(baseline, file = "allocation_f.xlsx")

print("Check the R working directory for results saved as the allocation.csv file")
