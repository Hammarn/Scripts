#!/usr/bin/env Rscrip
###require(MOSAIC)
library(data.table)
library("LaF")

#library("MOSAIC", lib = "~/R")
library("MOSAIC")

args = commandArgs(trailingOnly=TRUE) 

## args[1] is normal .Rdata
# args[2] is localanc.Rdata

load(args[1])
load(args[2])

a = as.numeric(args[3]) 
# ancestry to extract

### Get local ancestry per SNP instead of Grid
pos_localanc=grid_to_pos(localanc, "../../MOSAIC_inputs/", g.loc, chrnos) # loads all chromosomes
##Get a matrix with True for all positions where MOSAIC is more then 90% sure that the ancestry is a
#anc=lapply(1:nchrno, function(ch) lapply(1:NUMA, function(h) pos_localanc[[ch]][a,h,]>0.9))

## Getting the SNPs for the snpfile
## Assumes that snpfile has the Alleles in it!
snps=list()
for (i in 1:nchrno) {
    snps[[i]]= read.table(paste0("../../MOSAIC_inputs/snpfile.",chrnos[i]))
    snps[[i]] <- snps[[i]][,c(2,1,4,5,6)]
}

# Not needed
#positions=lapply(1:nchrno, function(i) lapply(1:NUMA, function(h) snps[[i]][anc[[i]][[h]],4])) 

for (chr in 1:nchrno){
    target.genos=as.integer(as.matrix(laf_open_fwf(paste0("../../MOSAIC_inputs/",target,"genofile.",chr), column_widths=rep(1,NUMA),column_types=rep("character",NUMA))[,]))
    anc.calls=t(apply(pos_localanc[[chr]][a,,],2,function(x) x>0.8)) 
    anc.genos=(target.genos+1)*anc.calls
    anc.snps=cbind(snps[[chr]],anc.genos)
    write.table(anc.snps, paste(target,"_ancestry_",a,"_chr",i,".haps",sep=""), sep = "\t", row.names = FALSE,quote = FALSE,col.names = F)
    print(paste("Done with", paste(target,"_ancestry_",a,"_chr",i,".haps",sep=""))
  }
}
