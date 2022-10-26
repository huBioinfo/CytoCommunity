library(diceR)

#Import data.
NodeMask <- read.csv("Run1/NodeMask.csv", header = FALSE)
nonzero_ind <- which(NodeMask$V1 == 1)

#Find the file names of all soft clustering results.
allSoftClustFile <- list.files(path = "./", pattern = "ClusterAssignMatrix1.csv", recursive = TRUE)
allHardClustLabel <- vector()

for (i in 1:length(allSoftClustFile)) {
  
  ClustMatrix <- read.csv(allSoftClustFile[i], header = FALSE, sep = ",")
  ClustMatrix <- ClustMatrix[nonzero_ind,]
  HardClustLabel <- apply(as.matrix(ClustMatrix), 1, which.max)
  rm(ClustMatrix)
  
  allHardClustLabel <- cbind(allHardClustLabel, as.vector(HardClustLabel))
  
} #end of for.

finalClass <- diceR::majority_voting(allHardClustLabel, is.relabelled = FALSE)
write.table(finalClass, file = "ConsensusLabel_MajorityVoting.csv", append = FALSE, quote = FALSE, row.names = FALSE, col.names = FALSE)


