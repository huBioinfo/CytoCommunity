# Hyperparameter
InputFolderName <- "MIBI_TNBC_KNNgraph_Input"

Sys.time()
#Create an outer folder to collect all images.
FolderName_0 <- "ImageCollection"
if (file.exists(FolderName_0)) {
  
  cat("The folder already exists!")

} else {
  
  dir.create(FolderName_0)
  
}

#Create an inner folder for each image. The order is based on the "ImageNameList.txt".
ImageNameList <- read.csv(paste(c("./", InputFolderName, "/ImageNameList.txt"), collapse = ''), header = FALSE)
for (k in 1:nrow(ImageNameList)) {
  FolderName_1 <- paste(c(FolderName_0, "/", ImageNameList[k, 1]), collapse = '')
  if (file.exists(FolderName_1)) {
    
    cat("The folder already exists!")
    
  } else {
    
    dir.create(FolderName_1)
    
  }
  
}

#Find all subfolder names with "Fold".
dirs <- list.dirs(recursive = TRUE)
Fold_FolderName <- grep("Fold", dirs, value = TRUE)

for (p in 1:length(Fold_FolderName)) {
  print(paste(c("This is Run", p, "/", length(Fold_FolderName)), collapse = '')) #12s/Run(10*10=100runs).
  
  for (q in 1:nrow(ImageNameList)) {
    GraphIdx_FileName <- paste(c(Fold_FolderName[p], "/GraphIdx_", q-1, ".csv"), collapse = '') #"q-1" is for 0-based Python indexing.
    ClusterAssignMatrix1_FileName <- paste(c(Fold_FolderName[p], "/ClusterAssignMatrix1_", q-1, ".csv"), collapse = '') #"q-1" is for 0-based Python indexing.
    NodeMask_FileName <- paste(c(Fold_FolderName[p], "/NodeMask_", q-1, ".csv"), collapse = '') #"q-1" is for 0-based Python indexing.
    
    #Extract the true image id.
    ImageId <- as.numeric(read.csv(GraphIdx_FileName, header = FALSE))
    ImageName <- ImageNameList[ImageId+1, 1]  #"ImageId+1" is because ImageId is 0-based Python indexing.
    
    #Extract the useful string for renaming.
    ImpStr <- strsplit(Fold_FolderName[p], "/")
    #ImpStr <- strsplit(tail(ImpStr[[1]], n = 1), "/")
    TimeName <- ImpStr[[1]][2]
    FoldName <- ImpStr[[1]][3]
    
    #Copy the "GraphIdx_xx.csv" file, "ClusterAssignMatrix1_xx.csv" file and "NodeMask_xx.csv" file and rename them in the collected image folder.
    ImageName_FolderName <- paste(c(FolderName_0, "/", ImageName), collapse = '')
    
    file.copy(GraphIdx_FileName, ImageName_FolderName)
    OldName <- paste(c(ImageName_FolderName, "/GraphIdx_", q-1, ".csv"), collapse = '')
    NewName <- paste(c(ImageName_FolderName, "/GraphIdx_", TimeName, "_", FoldName, ".csv"), collapse = '')
    file.rename(OldName, NewName)
    
    file.copy(ClusterAssignMatrix1_FileName, ImageName_FolderName)
    OldName <- paste(c(ImageName_FolderName, "/ClusterAssignMatrix1_", q-1, ".csv"), collapse = '')
    NewName <- paste(c(ImageName_FolderName, "/ClusterAssignMatrix1_", TimeName, "_", FoldName, ".csv"), collapse = '')
    file.rename(OldName, NewName)
    
    file.copy(NodeMask_FileName, ImageName_FolderName)
    OldName <- paste(c(ImageName_FolderName, "/NodeMask_", q-1, ".csv"), collapse = '')
    NewName <- paste(c(ImageName_FolderName, "/NodeMask_", TimeName, "_", FoldName, ".csv"), collapse = '')
    file.rename(OldName, NewName)
    
  }
  
}


Sys.time()
rm(list = ls())
library(diceR)
Image_dirs <- list.dirs(path = "ImageCollection", recursive = FALSE)

for (kk in 1:length(Image_dirs)) {
  print(paste(c("This is Image", kk, "/", length(Image_dirs)), collapse = '')) #10s/Image(140images).
  
  #Import data.
  NodeMask_FileName <- paste(c(Image_dirs[kk], "/NodeMask_Time1_Fold1.csv"), collapse = '')
  NodeMask <- read.csv(NodeMask_FileName, header = FALSE)
  nonzero_ind <- which(NodeMask$V1 == 1)
  
  #Find the file names of all soft clustering results.
  allSoftClustFile <- list.files(path = Image_dirs[kk], pattern = "ClusterAssignMatrix1", recursive = TRUE)
  allHardClustLabel <- vector()
  
  for (i in 1:length(allSoftClustFile)) {
    
    SoftClust_FileName <- paste(c(Image_dirs[kk], "/", allSoftClustFile[i]), collapse = '')
    ClustMatrix <- read.csv(SoftClust_FileName, header = FALSE, sep = ",")
    ClustMatrix <- ClustMatrix[nonzero_ind,]
    HardClustLabel <- apply(as.matrix(ClustMatrix), 1, which.max)
    rm(ClustMatrix)
    
    allHardClustLabel <- cbind(allHardClustLabel, as.vector(HardClustLabel))
    
  } #end of for.
  
  
  finalClass <- diceR::majority_voting(allHardClustLabel, is.relabelled = FALSE)
  finalClass_FileName <- paste(c(Image_dirs[kk], "/ConsensusLabel_MajorityVoting.csv"), collapse = '')
  write.table(finalClass, file = finalClass_FileName, append = FALSE, quote = FALSE, row.names = FALSE, col.names = FALSE)

}
Sys.time()


