library('ggplot2')
library('reshape')

data=read.table("counts_withID_full3", header=T,sep="\t")
data <- reshape(data,
                varying = c("AFR", "CEU", "CDX","YRI", "Khoisan"),
                v.names = "Source_propotion",
                timevar = "Source",
                times = c("1_AFR", "2_CEU", "3_CDX","4_YRI","5_Khoisan"),
                direction = "long")
data <- subset(data, select = -c(id))
Source=data$Source

p <- ggplot(data, aes(x=Source, y=Source_propotion)) +
             geom_point(alpha=0.3, aes(fill=Source, color=Source), position = "jitter", size = 0.7) +
             geom_boxplot(alpha=0, size=0.2) +
             ggtitle("Genome proportion assigned to source") +
             labs(y="Genome proportion") +
             theme(axis.title.x=element_blank(), legend.position="bottom",axis.text.x=element_blank(), axis.ticks.x=element_blank())
p2 <- p + facet_wrap( ~ Pop)
p3<- p2 + scale_color_manual(values=c("1_Khoisan"="#FF8C1E", "2_West_African"="#9A283D", "3_East_African"="#9FC22E" , "4_Eurasian"="#115E81" ))
ggsave(plot=p3, dpi=600, filename="STW5_RFMix_sourceproportion.pdf", width=8.3, height=11.7, units="in",  useDingbats=FALSE)
