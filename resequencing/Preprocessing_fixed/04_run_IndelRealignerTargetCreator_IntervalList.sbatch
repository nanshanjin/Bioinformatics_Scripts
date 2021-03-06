#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --time=0-23:59:00
#SBATCH --qos=normal
#SBATCH -e ./logs/indelcreator_%A_%a.err            # File to which STDERR will be written
#SBATCH -o ./logs/indelcreator_%A_%a.out           # File to which STDOUT will be written
#SBATCH -J indelcreator            # Job name
#SBATCH --mem=64000

export PATH=/usr/lib/jvm/jre-1.8.0-openjdk.x86_64/bin:$PATH
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk.x86_64/jre

SAMPLEDIR=/home/eenbody/reseq_WD/Preprocessing_fixed/03_sort_idx_sum
REF=/home/eenbody/Enbody_WD/WSFW_DDIG/Reference_Genome_WSFW/WSFW_ref_final_assembly.fasta
WORK_D=/home/eenbody/reseq_WD/Preprocessing_fixed/04_indel_realign

#########MAKE SURE THIS DIRECTORY EXISTS####
#mkdir logs

cd $WORK_D

java -Xmx16g -XX:ParallelGCThreads=1 -jar ~/BI_software/GenomeAnalysisTK.jar \
-T RealignerTargetCreator \
-nt 20 \
-R $REF \
-I $SAMPLEDIR/1_33221_naimii_CTCACG_dedup_sorted.bam \
-I $SAMPLEDIR/2_33223_naimii_CAGCTT_dedup_sorted.bam \
-I $SAMPLEDIR/3_33225_naimii_CGCTAC_dedup_sorted.bam \
-I $SAMPLEDIR/4_33228_naimii_ATTGTA_dedup_sorted.bam \
-I $SAMPLEDIR/5_33230_naimii_TCCTAG_dedup_sorted.bam \
-I $SAMPLEDIR/6_33232_naimii_AGATCC_dedup_sorted.bam \
-I $SAMPLEDIR/7_33233_naimii_TTGTCA_dedup_sorted.bam \
-I $SAMPLEDIR/8_33234_naimii_AGCTTT_dedup_sorted.bam \
-I $SAMPLEDIR/9_33235_naimii_ATCCGC_dedup_sorted.bam \
-I $SAMPLEDIR/10_33240_naimii_CTGAAA_dedup_sorted.bam \
-I $SAMPLEDIR/11_33248_aida_CTGGCC_dedup_sorted.bam \
-I $SAMPLEDIR/12_33249_aida_TAATGT_dedup_sorted.bam \
-I $SAMPLEDIR/13_33252_aida_ATTTCG_dedup_sorted.bam \
-I $SAMPLEDIR/14_33253_aida_TGTACG_dedup_sorted.bam \
-I $SAMPLEDIR/15_33254_aida_CAGTGT_dedup_sorted.bam \
-I $SAMPLEDIR/17_33257_aida_GACTCA_dedup_sorted.bam \
-I $SAMPLEDIR/18_33297_lorentzi_ATGACT_dedup_sorted.bam \
-I $SAMPLEDIR/19_47720_moretoni_GTAGGC_dedup_sorted.bam \
-I $SAMPLEDIR/20_36126_moretoni_AGACCA_dedup_sorted.bam \
-I $SAMPLEDIR/21_36148_moretoni_TCAGCC_dedup_sorted.bam \
-I $SAMPLEDIR/22_36149_moretoni_ACGGTC_dedup_sorted.bam \
-I $SAMPLEDIR/23_36182_moretoni_TTCGAA_dedup_sorted.bam \
-I $SAMPLEDIR/24_36188_moretoni_AGGTAC_dedup_sorted.bam \
-I $SAMPLEDIR/25_47617_lorentzi_TATCAG_dedup_sorted.bam \
-I $SAMPLEDIR/26_47623_lorentzi_CCATGT_dedup_sorted.bam \
-I $SAMPLEDIR/27_47631_lorentzi_ATGCGC_dedup_sorted.bam \
-I $SAMPLEDIR/28_47653_lorentzi_TTAGCT_dedup_sorted.bam \
-I $SAMPLEDIR/29_47657_lorentzi_GCCATA_dedup_sorted.bam \
-I $SAMPLEDIR/30_47672_lorentzi_AGTGCC_dedup_sorted.bam \
-I $SAMPLEDIR/31_47683_lorentzi_CTTGAC_dedup_sorted.bam \
-I $SAMPLEDIR/32_47707_moretoni_CATTAG_dedup_sorted.bam \
-I $SAMPLEDIR/33_47717_moretoni_TCGGAT_dedup_sorted.bam \
-I $SAMPLEDIR/34_47745_moretoni_CGATGT_dedup_sorted.bam \
-I $SAMPLEDIR/35_47815_moretoni_TGACCA_dedup_sorted.bam \
-I $SAMPLEDIR/36_97513_lorentzi_GCCAAT_dedup_sorted.bam \
-I $SAMPLEDIR/37_97528_lorentzi_CTTGTA_dedup_sorted.bam \
-I $SAMPLEDIR/16_33256_aida_ATCACG_dedup_sorted.bam \
-o WSFW_indel_${SLURM_ARRAY_TASK_ID}.intervals \
-L split_fai/split_faiWSFW_ref_final_assembly.fasta_${SLURM_ARRAY_TASK_ID}.interval_list
