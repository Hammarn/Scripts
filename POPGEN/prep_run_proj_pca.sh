## 1 is the basename of the merged plinkfile
## 2 i number of indivudals in modern reference
## 3 is number of individuals in ancient samples


module load bioinfo-tools
module load plink/1.90b4.9
module load  eigensoft

## Inputs
infile=$1
fbase=$(basename $infile)
mod_popfile=ref_pop_all.pop
anc_popfile=EU.pop

grep -f $mod_popfile $infile.tfam > keep.tmp
grep -f $anc_popfile $infile.tfam >> keep.tmp

plink --tfile $infile --keep keep.tmp --recode --out $fbase.subset

python ~/Scripts/POPGEN/ped_add_pop.py $fbase.subset

mv $fbase.subset2.ped $fbase.subset.ped

### make the parameter file
rm pca.par
echo  outliermode: 2 >> pca.par
echo altnormstyle:    NO >> pca.par
echo familynames:     NO >> pca.par
echo grmoutname:      grmjunk >> pca.par
echo killr2:    YES >> pca.par
echo r2thresh:  0.7 >> pca.par
echo genotypename: ${fbase}.subset.ped >> pca.par
echo snpname: ${fbase}.subset.map >> pca.par
echo indivname: ${fbase}.subset.ped >> pca.par
echo evecoutname: ${fbase}.popsubset_withOutliers.evec >> pca.par
echo evaloutname: ${fbase}.popsubset_withOutliers.eval >> pca.par
echo lsqproject: YES >> pca.par
echo poplistname: ${mod_popfile} >> pca.par
echo shrinkmode: YES >> pca.par


### Run the PCA
module load bioinfo-tools
module load eigensoft
smartpca -p pca.par > logfile_aDNA_unknown.log
rm modern_ancient.txt
printf 'Reference\n%.0s' {1..${2}} > modern_ancient.txt
printf 'Extracted\n%.0s' {1..${3}} >> modern_ancient.txt
paste ${fbase}.popsubset_withOutliers.evec modern_ancient.txt > plot.evec
