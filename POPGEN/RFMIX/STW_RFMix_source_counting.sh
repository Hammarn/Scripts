/home/mariov/DataSets/sissy_that_walk_dataset


nano counts_per_line_base.sh
################################ script 
#!/bin/bash -l
#SBATCH -J counts_per_line_replace_here
#SBATCH -t 12:0:0
#SBATCH -A b2016104
#SBATCH -p core -n 1

c=replace_here

touch counts_per_line_${c}
for i in {1..1462}; do # number of alleles in the nalyzes (2x the individuals)
cut -d' ' -f${i} KS_STW_RFMix_output_chr${c}.rfmix.2.Viterbi.txt | grep 1 | wc -l > source_1_chr${c}
cut -d' ' -f${i} KS_STW_RFMix_output_chr${c}.rfmix.2.Viterbi.txt | grep 2 | wc -l > source_2_chr${c}
cut -d' ' -f${i} KS_STW_RFMix_output_chr${c}.rfmix.2.Viterbi.txt | grep 3 | wc -l > source_3_chr${c}
cut -d' ' -f${i} KS_STW_RFMix_output_chr${c}.rfmix.2.Viterbi.txt | grep 4 | wc -l > source_4_chr${c}
cut -d' ' -f${i} KS_STW_RFMix_output_chr${c}.rfmix.2.Viterbi.txt | grep 5 | wc -l > source_5_chr${c}
echo ${i} > column_${c}
paste column_${c} source_1_chr${c} source_2_chr${c} source_3_chr${c} source_4_chr${c} source_5_chr${c} > counts_per_line_temp_${c}
cat counts_per_line_${c} counts_per_line_temp_${c} >> counts_per_line_${c}

rm source_1_chr${c} source_2_chr${c} source_3_chr${c} source_4_chr${c} source_5_chr${c} counts_per_line_temp_${c} column_${c}
done
############################### END


for c in {1..22}; do 
sed "s/replace_here/${c}/g" counts_per_line_base.sh > counts_per_line_chr${c}.sh
chmod 777 counts_per_line_chr${c}.sh
sbatch counts_per_line_chr${c}.sh
done



python /home/mariov/DataSets/sashay_away_dataset/duplicate_tfam.py < stw6.fam.origname > counts_tfamdup
cut -d' ' -f1,2 counts_tfamdup | sed "s/_A$//g" | sed "s/_B$//g" > counts_ID

for c in {1..22}; do 
paste counts_ID counts_per_line_${c} | sed "s/\t/ /g" | cut -d' ' -f2,4,5,6,7,8,9 > counts_withID_chr${c}
echo ${c}
done


ID S1 S2 S3 S4 S5

touch counts_withID_full
for c in {1..22}; do 
cat counts_withID_chr${c} >> counts_withID_full
done

nano counts_withID_full #add header
ID S1 S2 S3 S4 S5

awk -F' ' 'NR==1{print;next} {if ($1 in seen); else b[c++]=$1; seen[$1]=1; for (i=2;i<=NF;i++) {a[$1","i]+=$i}} END{for (j=0;j<c;j++) {s=b[j]; for (i=2;i<=NF;i++){s=s" "a[b[j]","i]}; print s}}' counts_withID_full | column -t > counts_withID_full2

sed 's/  / /g' counts_withID_full2 | sed 's/                   / /g' | sed 's/    / /g' | sed 's/       / /g' | sed 's/   / /g' | sed 's/  / /g' | sed 's/  / /g' > counts_withID_full3

cut -d' ' -f 1,2 stw6.fam.origname > Add_pops
paste Add_pops counts_withID_full3 | sed "s/\t/ /g" > counts_withID_full4

nano counts_withID_full5


#### ploting
R
library('ggplot2')
library('reshape')

data=read.table("counts_withID_full5", header=T,sep="\t")
data <- reshape(data,
                varying = c("X1_Khoisan", "X2_West_Africa", "X3_East_Africa", "X4_Eurasia"),
                v.names = "Source_propotion",
                timevar = "Source",
                times = c("1_Khoisan", "2_West_African", "3_East_African", "4_Eurasian"),
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




