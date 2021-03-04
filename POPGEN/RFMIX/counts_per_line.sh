#!/bin/bash -l
#SBATCH -t 12:0:0
#SBATCH -A snic2018-8-252 
#SBATCH -p core -n 1

c=$1

touch counts_per_line_${c}
for i in {1..154}; do # number of alleles in the nalyzes (2x the individuals)
    cut -d' ' -f${i} AFR_FB_chr${c}.2.Viterbi.txt  | grep 1 | wc -l > source_1_chr${c}
    cut -d' ' -f${i} AFR_FB_chr${c}.2.Viterbi.txtt | grep 2 | wc -l > source_2_chr${c}
    cut -d' ' -f${i} AFR_FB_chr${c}.2.Viterbi.txt | grep 3 | wc -l > source_3_chr${c}
    cut -d' ' -f${i} AFR_FB_chr${c}.2.Viterbi.txt | grep 4 | wc -l > source_4_chr${c}
    #cut -d' ' -f${i} AFR_all_chr${c}.rfmix.2.Viterbi.txt | grep 5 | wc -l > source_5_chr${c}
    #cut -d' ' -f${i} AFR_all_chr${c}.rfmix.2.Viterbi.txt | grep 6 | wc -l > source_6_chr${c}
    echo ${i} > column_${c}
    paste column_${c} source_1_chr${c} source_2_chr${c} source_3_chr${c} source_4_chr${c} > counts_per_line_temp_${c}
    cat counts_per_line_temp_${c} >> counts_per_line_${c}
    
    rm source_1_chr${c} source_2_chr${c} source_3_chr${c} source_4_chr${c}   counts_per_line_temp_${c} column_${c}
done
