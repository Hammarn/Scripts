library(ggplot2,reshape2)
library(viridis)
library(scales)
library(vegan)



args=commandArgs(TRUE)
evecfile=args[1]
#bamlist=args[2] ##tfam-like file
outfile=args[3]

evec=read.table(evecfile,skip=1,col.names=c("Ind","PC1","PC2","PC3","PC4","PC5","PC6","PC7","PC8","PC9","PC10","Pop"))

modern=subset(evec,!grepl('Unk*',evec[[12]]))
popMean=aggregate(.~Pop,data=modern,mean)
ancient=subset(evec,grepl('Unk*',evec[[12]]))
#bam_tab=read.table(bamlist)
#ancient_cult=cbind(ancient,Treatment=bam_tab$V4)
#ancient=cbind(ancient_cult,Sample=bam_tab$V5)


pdf(paste(outfile ,'PC1PC2.pca.pdf',sep=''))
ggplot(modern,aes(x=PC1, y=PC2))+geom_point(colour='grey80')+theme_bw()+guides(fill=FALSE)+
  geom_text(data=popMean,label=popMean$Pop,colour='grey75',aes(x=PC1,y=PC2))+
  geom_point(data=ancient,aes(x=PC1,y=PC2,colour=Pop),size=5)+
  theme(legend.background=element_blank(),legend.key=element_blank()) #+
dev.off()

pdf(paste(outfile ,'PC1PC3.pca.pdf',sep=''))
ggplot(modern,aes(x=PC1, y=PC3))+geom_point(colour='grey80')+theme_bw()+guides(fill=FALSE)+
  geom_text(data=popMean,label=popMean$Pop,colour='grey75',aes(x=PC1,y=PC3))+
  geom_point(data=ancient,aes(x=PC1,y=PC3,colour=Pop),size=5)+
  theme(legend.background=element_blank(),legend.key=element_blank()) #+
dev.off()

pdf(paste(outfile ,'PC1PC4.pca.pdf',sep=''))
ggplot(modern,aes(x=PC1, y=PC4))+geom_point(colour='grey80')+theme_bw()+guides(fill=FALSE)+
  geom_text(data=popMean,label=popMean$Pop,colour='grey75',aes(x=PC1,y=PC4))+
  geom_point(data=ancient,aes(x=PC1,y=PC4,colour=Pop),size=5)+
  theme(legend.background=element_blank(),legend.key=element_blank()) #+
dev.off()

pdf(paste(outfile ,'PC2PC3.pca.pdf',sep=''))
ggplot(modern,aes(x=PC2, y=PC3))+geom_point(colour='grey80')+theme_bw()+guides(fill=FALSE)+
  geom_text(data=popMean,label=popMean$Pop,colour='grey75',aes(x=PC2,y=PC3))+
  geom_point(data=ancient,aes(x=PC2,y=PC3,colour=Pop),size=5)+
  theme(legend.background=element_blank(),legend.key=element_blank()) #+

  dev.off()
pdf(paste(outfile ,'PC2PC4.pca.pdf',sep=''))
ggplot(modern,aes(x=PC2, y=PC4))+geom_point(colour='grey80')+theme_bw()+guides(fill=FALSE)+
  geom_text(data=popMean,label=popMean$Pop,colour='grey75',aes(x=PC2,y=PC4))+
  geom_point(data=ancient,aes(x=PC2,y=PC4,colour=Pop),size=5)+
  theme(legend.background=element_blank(),legend.key=element_blank()) #+
dev.off()
