#!/usr/bin/env Rscrip
###require(MOSAIC)
library(data.table)

library("MOSAIC", lib = "~/R")

args = commandArgs(trailingOnly=TRUE) 

## args[1] is normal .Rdata
# args[2] is localanc.Rdata

load(args[1])
load(args[2])

a = as.numeric(args[3]) 
# ancestry to extract

### Get local ancestry per SNP instead of Grid
pos_localanc=grid_to_pos(localanc, "./", g.loc, chrnos) # loads all chromosomes
##Get a matrix with True for all positions where MOSAIC is more then 90% sure that the ancestry is a
anc=lapply(1:nchrno, function(ch) lapply(1:NUMA, function(h) pos_localanc[[ch]][a,h,]>0.9))

## Getting the SNPs for the snpfile
## Assumes that snpfile has the Alleles in it!
snps=list()
for (i in 1:nchrno) {
    snps[[i]]= read.table(paste0("snpfile.",chrnos[i]))
}
positions=lapply(1:nchrno, function(i) lapply(1:NUMA, function(h) snps[[i]][anc[[i]][[h]],4])) 

for (i in 1:22){
  for (hap in 1:(length(alpha)*2)){
   if (hap %% 2  ){
     # Get  First Allele
     to_write<-snps[[i]][which(snps[[i]]$V4 %in% positions[[i]][[hap]]),][,c(4,5)]
   } else {
     #second allele
     to_write<-snps[[i]][which(snps[[i]]$V4 %in% positions[[i]][[hap]]),][,c(4,6)]
   }
    write.table(to_write, paste(target"_ancestry_",a,"_chr",i,"_hap_",hap,".bimlike",sep=""), sep = "\t", row.names = FALSE,quote = FALSE,col.names = F)
  }
}
