### Transcript quant and expression

This will use RSEM to quantify transcript abundance in the absence of annotation data from a reference genome. The results of this can be used in differential expression analyses using count data.

##### Starting with Trinity de novo (not guided)

##### RSEM

Testing these commands first from the FAS suggestions. `--strand-specific` indicates that this will use Bowtie2's --norc command which indicates stranded data.
```bash
rsem-calculate-expression --bowtie2 --num-threads 1 --strand-specific --paired-end  10-33254-aida-Chest_S10_clp.fq.1.gz  10-33254-aida-Chest_S10_clp.fq.2.gz  ./ref/transcripts  WSFW_RSEM_bowtie2
```
This seems to have worked, so running `rsem_exp_array.sh` on first individual in array.

##### Kallisto
fast way

Running one command fist in idev
```bash
kallisto quant -i ./ref/Trinity.idx -o 10-33254-aida-Chest_S10.kallisto_out -b 100 -t 20 --fr-stranded 10-33254-aida-Chest_S10_clp.fq.1.gz  10-33254-aida-Chest_S10_clp.fq.2.gz
```

##### Next steps

It would probably be worthwhile to investigate Trinity's documentation on QC and batch effects:
https://github.com/trinityrnaseq/trinityrnaseq/wiki/QC-Samples-and-Biological-Replicates

Can I do something similar with STAR output?

This requires quantification matrices which I dont think I've created yet (but maybe did when I ran RSEM?):
https://github.com/trinityrnaseq/trinityrnaseq/wiki/Trinity-Transcript-Quantification

For diff expression , it would be interesting to compare between body parts vs. between populations in one big heat map. This should be possible and might even be one utility of Trinotate Web.
