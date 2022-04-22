#!/usr/bin/env Rscrip

## Example usage:
## Rscript examine_tract_lengths_and_plot.R AFAR_2way_1-8_1-22_574_60_0.99_100.RData localanc_AFAR_2way_1-8_1-22_574_60_0.99_100.RData

library("MOSAIC")
library(ggplot2)
library(reshape2)

args = commandArgs(trailingOnly=TRUE)

## args[1] is normal .Rdata
# args[2] is localanc.Rdata

load(args[1])
load(args[2])


tract_lengths=function(t.localanc, thresh=0.8) {
  ans=list()
  t.A=dim(t.localanc[[1]])[1]
  for (a in 1:t.A) {
    ans[[a]]=list()
    for (ch in 1:length(t.localanc)) {
      ans[[a]][[ch]]=list()
      anc.calls=t(apply(t.localanc[[ch]][a,,],2,function(x) x>thresh))
      for (i in 1:dim(localanc[[1]])[2]) {
    d=diff(anc.calls[,i])
    segs=cumsum(abs(d))
    ans[[a]][[ch]][[i]]=as.numeric(table(segs))
      }
    }
  }
  return(ans)
}

bin_tracts=function(tract.lengths, nh=20, min.length=NULL, max.length=NULL, mids=NULL) {
  if (is.null(min.length)) min.length=min(unlist(tract.lengths))
  if (is.null(max.length)) max.length=max(unlist(tract.lengths))
  if (is.null(mids)) mids=seq(min.length,max.length,length.out=nh)
  ans=data.frame(mids=mids)
  t.A=length(tract.lengths)
  for (a in 1:t.A)
    ans[,a+1]=sapply(mids,function(x) sum(x==mids[sapply(unlist(tract.lengths[[a]]),function(y) which.min(abs(mids-y)))]))
  colnames(ans)=c("mids",1:t.A)
  return(ans)
}

tract.lengths=tract_lengths(localanc)
binned.tracts=bin_tracts(tract.lengths)

testFST <- as.data.frame(all_Fst$panels)
top_anc <- vector("list",A)
top_anc[[1]] <-   paste("1-", rownames(testFST)[which.min(testFST$`anc 1`)], sep ="")
top_anc[[2]] <-   paste("2-", rownames(testFST)[which.min(testFST$`anc 2`)], sep ="")
top_anc[[3]] <-   paste("3-", rownames(testFST)[which.min(testFST$`anc 3`)], sep ="")

colnames(binned.tracts)<-c("mids",top_anc[[1]],top_anc[[2]],top_anc[[3]])

df_long <- melt(binned.tracts, id.vars = "mids")
ggplot() +
  ggtitle(target)+
  scale_y_continuous(trans='log10')+
  geom_line(data = df_long, aes(x = mids / 60, y= value, colour=variable))+
  geom_point(data = df_long, aes(x = mids / 60, y= value, colour=variable))+
  xlab("tract length (cM)") +
  ylab("Number of Tracts") +
  guides(colour=guide_legend(title="Ancestry"))+
  theme_bw()+
  theme(plot.title = element_text(hjust = 0.5))

ggsave(paste("Tract_lenghts_",target, "_", A, "-way.pdf", sep = ""), device = "pdf",   width = 10, height = 10)
