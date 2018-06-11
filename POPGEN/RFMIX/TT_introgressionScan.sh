# remove SNPs that are in the first and last 2Mb from each chr

cp ../dataset_dense_final/hg19_index_file . # index file

awk '{print $0, $2-2000000}' hg19_index_file > hg19_index_file_withlast2Mbcol


# list with SNPs within the 2Mb ends FOR EXCLUSION
cat hg19_index_file_withlast2Mbcol | while read line; do 
C=$( echo $line | cut -d' ' -f1 )
P=$( echo $line | cut -d' ' -f6 )
awk '$4<=2000000' TT_forRFMix_chr${C}.bim > BorderSNPs_chr${C}_beg
awk -v r=$P '{if($4>=r) print}' TT_forRFMix_chr${C}.bim > BorderSNPs_chr${C}_end
done

for C in {1..22};do 
cat BorderSNPs_chr${C}_beg BorderSNPs_chr${C}_end > BorderSNPs_chr${C}
rm BorderSNPs_chr${C}_beg BorderSNPs_chr${C}_end
done
#  34802 total


#Just SNPs pos
for C in {1..22};do 
cut -f4 BorderSNPs_chr${C} > BorderSNPs_chr${C}_justpos
done

# Add SNP pos to Viterbi
for C in {1..22};do 
cut -f4 TT_forRFMix_chr${C}.bim > bimpos_chr${C}
done



for C in {1..22};do 
paste bimpos_chr${C} TT_RFMix_output_chr${C}.rfmix.2.Viterbi.txt | sed "s/\t/ /g" > Viterbi_pos_chr${C}
done

#grep the non matching
for C in {1..22}; do
grep -Fvwf BorderSNPs_chr${C}_justpos Viterbi_pos_chr${C} > Viterbi_pos_2Mbfilter_chr${C}
done 

for C in {1..22}; do
cut -d' ' -f2- Viterbi_pos_2Mbfilter_chr${C} > Viterbi_RFMix_i2_2Mbfilter_chr${C}
done 

awk -F' ' '{print NF; exit}' TT_forRFMix_chr22_shapeit.alleles 

awk -F' ' '{print NF; exit}' Viterbi_RFMix_i2_2Mbfilter_chr22




################################## FEBRUARY 21 2017

# Replace the code 'khoisan' from sources to their original code on the tfam
python duplicate_tfam.py < tt4_originalnames.fam > ID_dupl # wc -l ID_dupl: 1088
cut -d' ' -f1-2 ID_dupl | sed 's/_A$//g' | sed 's/_B$//g' > ID_counts

awk '{ FS = " " } ; { print NF}' dataset_DF_RFMix_output_chr1.rfmix.1.Viterbi.txt
#942

#create the key for each sample position
cat -n ID_counts | sed "s/^     //g" | sed "s/^    //g" | sed "s/^   //g" |  sed "s/^ //g" | sed "s/^ //g" |sed 's/\t/ /g' > Viterbi_key

cut -d' ' -f2 Viterbi_key | sort | uniq > Pops


#Identify the positions in the Viterbi for each pop
cat Pops | while read line; do
grep "${line}" Viterbi_key | cut -d' ' -f1 | sed ':a;N;$!ba;s/\n/,/g'  > Lines_"${line}"
done

#create bim files with 2Mb filtering
module load bioinfo-tools 
module load plink

for c in {1..22}; do 
plink --bfile TT_forRFMix_chr${c} --exclude BorderSNPs_chr${c} --make-bed --out TT_2Mb_filtered_chr${c}
done

#Extract info
cat Pops | while read line; do
L=$( cat Lines_"${line}" )
for c in {1..22}; do 
cut -d' ' -f ${L} Viterbi_RFMix_i2_2Mbfilter_chr${c} > Vit_counts_"${line}"_chr${c}

awk -F' ' '{temp=gsub(/1/,""); print temp/(temp+NF)}' Vit_counts_"${line}"_chr${c} > VitSources_"${line}"_chr${c}_source_1
awk -F' ' '{temp=gsub(/2/,""); print temp/(temp+NF)}' Vit_counts_"${line}"_chr${c} > VitSources_"${line}"_chr${c}_source_2
awk -F' ' '{temp=gsub(/3/,""); print temp/(temp+NF)}' Vit_counts_"${line}"_chr${c} > VitSources_"${line}"_chr${c}_source_3
awk -F' ' '{temp1=gsub(/4/,""); temp2=gsub(/5/,""); print (temp1+temp2)/(temp1+temp2+NF)}' Vit_counts_"${line}"_chr${c} > VitSources_"${line}"_chr${c}_source_4and5

cat  TT_2Mb_filtered_chr${c}.bim  | cut -d' ' -f1-4 > Pos_chr${c}
done
done



# index file based on hg19.fai file from KSP proj
nano hg19_index_file
cat hg19_index_file | while read line; do ## Add the absolute position for each chr and sum the value with the Chr Pos
	C=$( echo $line | cut -d' ' -f1 )
	P=$( echo $line | cut -d' ' -f3 )
	sed -e "s/$/\t${P}/g" Pos_chr${C} | awk '{print $0, $4+$7}' > Pos_chr${C}_xxx
done


#### for plotting
for c in {1..22}; do
#awk '{ sum += $4; n++ } END { if (n > 0) print sum / n; }' Pos_chr${c} >> AveragePos_perChr
cut -f4 Pos_chr${c} | Rscript -e 'd<-scan("stdin", quiet=TRUE)' \
          -e 'cat(min(d), max(d), median(d), mean(d), sep=" ")' | sed -e "s/$/\n/g" >> AveragePos_perChr
done
cut -d' ' -f1,3 hg19_index_file > index
paste index AveragePos_perChr | sed "s/ /\t/g" > chr_middles
awk '{print $2+$6}' chr_middles > chr_middles_points
 



cat Pops | while read line; do
for c in {1..22}; do 
paste Pos_chr${c}_xxx VitSources_"${line}"_chr${c}_source_1 VitSources_"${line}"_chr${c}_source_2 VitSources_"${line}"_chr${c}_source_3 VitSources_"${line}"_chr${c}_source_4and5 > Z_"${line}"_chr${c}_Sources_perSNP ######################## WRONGGGG
echo "${line}_${c}"
done
done

#merge chr files
cat Pops | while read line; do
touch "${line}"_Sources_perSNP
for c in {1..22}; do 
cat "${line}"_Sources_perSNP Z_"${line}"_chr${c}_Sources_perSNP >> "${line}"_Sources_perSNP
done
done


cat Pops | while read line; do
sed -i "s/\t/ /g" "${line}"_Sources_perSNP
sed -i '1 i\chr SNP X Pos A1 A2 CHR_StartPos Full_Pos Source1 Source2 Source3 Source45' "${line}"_Sources_perSNP
done




################################################################

R
library('ggplot2')
library('reshape')


pop_list = c("GuiGhanaKgal_Sources_perSNP", "Juhoansi_Sources_perSNP", "Karretjie_Sources_perSNP", "Khomani_Sources_perSNP", "Khwe_Sources_perSNP", "Nama_Sources_perSNP", "Xade_KS_Sources_perSNP", "Xun_Sources_perSNP")


for (i in pop_list) {
data=read.table(i, header=T,sep=" ")

chr_mp=read.table("chr_middles_points_edit", header=T)

data <- reshape(data,
                varying = c("Source2", "Source3", "Source45"),
                v.names = "External_Source_propotion",
                timevar = "Ext_Source",
                times = c("2_West_African", "3_East_African", "4_Eurasian"),
                direction = "long")

data <- subset(data, select = -c(id))
Ext_Source=data$Ext_Source
Source1=data$Source1
chr_break <- unique(data$CHR_StartPos)
perc_all <- quantile(data$External_Source_propotion, 0.99)



z <- ggplot(data, aes(x=Full_Pos)) + theme_classic() + labs(y="Genome proportion")
z2 <- z + geom_ribbon(aes(ymin=0, ymax=Source1, group=chr, fill = factor(chr%%2), color = factor(chr%%2)), alpha=0.2) 
z3 <- z2 + geom_point(aes(y=External_Source_propotion, fill=Ext_Source, color=Ext_Source), size = 0.7) 
z4 <- z3 + scale_fill_manual(values=c("#ACABAC", "#E4D8CA", "#894CE0", "#45DB75", "#F9684F")) + scale_color_manual(values=c("#ACABAC", "#E4D8CA", "#894CE0", "#45DB75", "#F9684F"))
z5 <- z4 + geom_hline(aes(yintercept=as.numeric(perc_all)), color="black", alpha=0.7)
z6 <- z5 + theme(legend.position="bottom", axis.title.x=element_blank(), legend.title=element_blank())
z7 <- z6 + scale_x_continuous(breaks = chr_mp$Pos, minor_breaks=NULL,labels= chr_mp$chr, expand = c(0, 0)) + scale_y_continuous(expand = c(0, 0),  limits = c(0, 1))

#ggsave(plot=z7, dpi=300, filename="Nama_introgression_scanTRAIL2.jpeg", width=8, height=2.5, units="in")

ggsave(plot=z7, dpi=300, filename=paste(i, "_introgression_scan_Feb2017.jpeg", sep=""), width=8, height=2.5, units="in")
}


purple: #894CE0


################################################################

R
library('ggplot2')
library('reshape')


pop_list = c("GuiGhanaKgal_Sources_perSNP", "Juhoansi_Sources_perSNP", "Karretjie_Sources_perSNP", "Khomani_Sources_perSNP", "Khwe_Sources_perSNP", "Nama_Sources_perSNP", "Xade_KS_Sources_perSNP", "Xun_Sources_perSNP")


for (i in pop_list) {
data=read.table(i, header=T,sep=" ")

chr_mp=read.table("chr_middles_points_edit", header=T)

data <- reshape(data,
                varying = c("Source2", "Source3", "Source45"),
                v.names = "External_Source_propotion",
                timevar = "Ext_Source",
                times = c("2_West_African", "3_East_African", "4_Eurasian"),
                direction = "long")

data <- subset(data, select = -c(id))
Ext_Source=data$Ext_Source
Source1=data$Source1
chr_break <- unique(data$CHR_StartPos)
perc_all <- quantile(data$External_Source_propotion, 0.99)



z <- ggplot(data, aes(x=Full_Pos)) + theme_classic() + labs(y="Genome proportion")
z2 <- z + geom_ribbon(aes(ymin=0, ymax=Source1, group=chr, fill = factor(chr%%2), color = factor(chr%%2)), alpha=0.2) 
z3 <- z2 + geom_point(aes(y=External_Source_propotion, fill=Ext_Source, color=Ext_Source), size = 0.7) 
z4 <- z3 + scale_fill_manual(values=c("#ACABAC", "#E4D8CA", "#894CE0", "#45DB75", "#F9684F")) + scale_color_manual(values=c("#ACABAC", "#E4D8CA", "#894CE0", "#45DB75", "#F9684F"))
z5 <- z4 + geom_hline(aes(yintercept=as.numeric(perc_all)), color="black", alpha=0.7)
z6 <- z5 + theme(legend.position="bottom", axis.title.x=element_blank(), legend.title=element_blank())
z7 <- z6 + scale_x_continuous(breaks = chr_mp$Pos, minor_breaks=NULL,labels= chr_mp$chr, expand = c(0, 0)) + scale_y_continuous(expand = c(0, 0),  limits = c(0, 1))

#ggsave(plot=z7, dpi=300, filename="Nama_introgression_scanTRAIL2.jpeg", width=8, height=2.5, units="in")

ggsave(plot=z7, dpi=300, filename=paste(i, "_introgression_scan_Feb2017.jpeg", sep=""), width=8, height=2.5, units="in")
}




### for Bantu pops

R
library('ggplot2')
library('reshape')

pop_list_BS = c("Ghanzi_BS_Sources_perSNP", "Khwe_Sources_perSNP", "Sotho_G_Sources_perSNP", "Zulu_G_Sources_perSNP", "SEBantu_Sources_perSNP", "SWBantu_Sources_perSNP")


for (i in pop_list_BS) {
data=read.table(i, header=T,sep=" ")

chr_mp=read.table("chr_middles_points_edit", header=T)

data <- reshape(data,
                varying = c("Source1", "Source3", "Source45"),
                v.names = "External_Source_propotion",
                timevar = "Ext_Source",
                times = c("1_Khoesan", "3_East_African", "4_Eurasian"),
                direction = "long")

data <- subset(data, select = -c(id))

Ext_Source=data$Ext_Source
Source1=data$Source1
perc_all <- quantile(data$External_Source_propotion, 0.99)

z <- ggplot(data, aes(x=Full_Pos)) + theme_classic() + labs(y="Genome proportion")
z2 <- z + geom_ribbon(aes(ymin=0, ymax=Source2, group=chr, fill = factor(chr%%2), color = factor(chr%%2)), alpha=0.2) + expand_limits(y = c(0, 1))
z3 <- z2 + geom_point(aes(y=External_Source_propotion, fill=Ext_Source, color=Ext_Source), size = 0.7) 
z4 <- z3 + scale_fill_manual(values=c("#894CE0", "#D6BBFC", "#EAC59B", "#45DB75", "#F9684F")) + scale_color_manual(values=c("#894CE0", "#D6BBFC", "#EAC59B", "#45DB75", "#F9684F"))
z5 <- z4 + geom_hline(aes(yintercept=as.numeric(perc_all)), color="black", alpha=0.7)
z6 <- z5 + theme(legend.position="bottom", axis.title.x=element_blank(), legend.title=element_blank())
z7 <- z6 + scale_x_continuous(breaks = chr_mp$Pos, minor_breaks=NULL,labels= chr_mp$chr, expand = c(0, 0)) + scale_y_continuous(expand = c(0, 0),  limits = c(0, 1))

ggsave(plot=z7, dpi=300, filename=paste(i, "_introgression_scan_BS_Feb2017.jpeg", sep=""), width=8, height=2.5, units="in")
}


EAC59B
#894CE0 #D6BBFC

