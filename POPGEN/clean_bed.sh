#!/bin/bash
echo $1
basename=${1%.*}
echo $basename
#module load bioinfo-tools
#plink19

rm variants_to_remove
grep -P "\tI" ${basename}.bim >> variants_to_remove
grep -P  "\tD" ${basename}.bim >> variants_to_remove

grep -P "\tA\tT" ${basename}.bim >> variants_to_remove
grep -P "\tT\tA" ${basename}.bim >> variants_to_remove
grep -P "\tC\tG" ${basename}.bim >> variants_to_remove
grep -P "\tG\tC" ${basename}.bim >> variants_to_remove

plink --bfile $basename --exclude variants_to_remove --make-bed --out ./${basename}_cleaned_1

plink --bfile ${basename}_cleaned_1 --mind 0.05 --make-bed --out ${basename}_cleaned_2

plink --bfile ${basename}_cleaned_2 --geno 0.1 --make-bed --out ${basename}_cleaned

rm ${basename}_cleaned_1
rm ${basename}_cleaned_2