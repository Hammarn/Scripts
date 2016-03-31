module load bioinfo-tools
module load rseqc
module load samtools
bam=$1
bed12=/sw/data/uppnex/igenomes/Homo_sapiens/Ensembl/GRCh37/Annotation/Genes/genes.bed
bam_stat.py -i $bam 2> $bam.bam_stat.txt
junction_annotation.py -i $bam -o $bam.rseqc -r $bed12
junction_saturation.py -i $bam -o $bam.rseqc -r $bed12
inner_distance.py -i $bam -o $bam.rseqc -r $bed12
geneBody_coverage.py -i $bam -o $bam.rseqc -r $bed12
infer_experiment.py -i $bam -r $bed12 > $bam.infer_experiment.txt
read_distribution.py -i $bam -r $bed12 > $bam.read_distribution.txt
read_duplication.py -i $bam -o $bam.read_duplication
RPKM_saturation.py -i $bam -r $bed12 -d '1+-,1-+,2++,2--' -o $bam.RPKM_saturation
