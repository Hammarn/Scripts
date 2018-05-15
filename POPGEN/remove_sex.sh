#!bin/bash


#exclude 0 and sex chr
rm exlist; touch exlist
grep -P "^0\t" $1.map >> exlist
grep -P "^MT\t" $1.map >> exlist
grep -P "^X\t" $1.map >> exlist
grep -P "^Y\t" $1.map >> exlist
grep -P "^XY\t" $1.map >> exlist

plink --bfile $1 --exclude exlist --make-bed --out tmp_file_bed_1 
plink --bfile tmp_file_bed_1~ --geno 0.1 --make-bed --out tmp_file_bed_2
plink --bfile tmp_file_bed_2 --mind 0.05 --make-bed --out ${1}_noSex_geno0.1_mind0.05
rm tmp_file_bed_1~tmp_file_bed_2
