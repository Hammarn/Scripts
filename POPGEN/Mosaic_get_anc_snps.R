#!/usr/bin/env Rscrip
###require(MOSAIC)

## Example usage:
## Rscript ~/Scripts/POPGEN/Mosaic_get_anc_snps.R AFAR_2way_1-8_1-22_574_60_0.99_100.RData localanc_AFAR_2way_1-8_1-22_574_60_0.99_100.RData 2

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
    snps[[i]] <- snps[[i]][,c(2,1,3,4)]
}

## Create the tfam file!
fileConn<-file(paste(target,"_EU.tfam", sep=""))
to_write <- c()
num_inds <- NUMA/2
for (ind in  1:num_inds){
    to_write <- c(paste(target, "_EU " ,target,ind, " 0 0 1 1" ,sep = ""), to_write)
}
writeLines(to_write,fileConn )
close(fileConn)

# Not needed
#positions=lapply(1:nchrno, function(i) lapply(1:NUMA, function(h) snps[[i]][anc[[i]][[h]],4])) 

for (chr in 1:nchrno){
    target.genos=as.integer(as.matrix(laf_open_fwf(paste0("../../MOSAIC_inputs/",target,"genofile.",chr), column_widths=rep(1,NUMA),column_types=rep("character",NUMA))[,]))
    anc.calls=t(apply(pos_localanc[[chr]][a,,],2,function(x) x>0.8)) 
    anc.genos=(target.genos+1)*anc.calls
    anc.snps=cbind(snps[[chr]],anc.genos)
    write.table(anc.snps, paste(target,"_ancestry_",a,"_chr",chr,".tped",sep=""), sep = "\t", row.names = FALSE,quote = FALSE,col.names = F)
    print(paste("Done with", paste(target,"_ancestry_",a,"_chr",chr,".tped",sep="")))
}
