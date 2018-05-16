#!/usr/bin/env Rscript
## Takes a .genome file from PLINK as ARGV 1 and outputs a 



args = commandArgs(trailingOnly=TRUE)
if (length(args)==0) {
      stop("At least one argument must be supplied (input file).n", call.=FALSE)
}    

data1<- read.table (args[1], header = T)
data2<-sort(data1$PI_HAT, decreasing = TRUE)

plot(data2, cex=0.8, pch = 20, col="aquamarine4")
title("IBS_proportion")
dev2bitmap(paste("IBS_proportion_",args[1],".pdf", sep=""), type="pdfwrite")
