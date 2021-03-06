#! /usr/bin/env python

import re, sys, os, itertools, sets, getopt        # Load standard modules I often use
import numpy, gzip

'''
Takes the results from -doCounts pos and count files to compute the average, median, and standard deviation of coverage for each scaffold for each individual (in different files). In addition, it will identify sites that have coverage above or below desired limits, given the number of indivdiuals with coverage at that site (-l <low coverage limit per individual> -u <upper coverage limit per individual>. Set up to work with a specific interval file handle, given as input <-i interval file prior to .counts.gz or .pos.gz>. The output handle is given by -o <handle>, and will produce handle.ind.mean.txt, handle.ind.median.txt, handle.ind.sd.txt, handle.exclude.sites. If the bamlist -b <bamlist> is specified, individuals will be renamed according to bam naming scheme (assuming follows (XX_01_02) where XX=pop, 01 = pop time, 02 = individual number.
'''

def main(argv):
	try:
		opts,args = getopt.getopt(argv,'ho:i:l:u:b:')
	except getopt.GetOptError:
		print "collapse_scaffold_coverage_interval_indiv_filter.py -o <output handle> -i <name of input .gzipped interval handle> -l <per individual lower coverage limit> -u <per individual upper coverage limit> -b <bamfile used in ANGSD to identify individual names>"
		sys.exit(2)

	outputHandle=""
	intervalHandle=""
	upperLim=""
	lowerLim=""
	bamFile=""

	for opt, arg in opts:
		if opt == "-h":
			print "collapse_scaffold_coverage_interval_indiv_filter.py -o <output file name> -i <name of input .gzipped interval file> -b <bamfile used in ANGSD to identify individual names>"
			sys.exit(2)
		elif opt == "-o":
			outputHandle = arg
		elif opt == "-i":
			intervalHandle = arg
		elif opt == "-u":
			upperLim = float(arg)
		elif opt == "-l":
			lowerLim = float(arg)
		elif opt == "-b":
			bamFile = arg

	posInfo = gzip.open(intervalHandle+".pos.gz","rb")
	indCount = gzip.open(intervalHandle+".counts.gz","rb")

	outMean = open(outputHandle+".ind.mean.txt","w")
	outMedian = open(outputHandle+".ind.median.txt","w")
	outSD = open(outputHandle+".ind.sd.txt","w")
	exclude = open(outputHandle+".exclude.sites","w")


	sample_names = []

	#Grab sample names if file exists
	if len(bamFile) > 1:
		bam = open(bamFile,"r")
		for line in bam:
			line_lst = line.split('.')
			sample = line_lst[0]
			sample_names.append(sample)

	ind_res = {}
	ind_res_scaffDict = {}
	completed = []
	ind_order = []
	scaff_res_mean = {}
	scaff_res_median = {}
	scaff_res_sd = {}


	#Number of sequenced individuals
	def count_ind(count_line):
		ind_count = 0
		for doc in count_line:
			if doc > 0:
				ind_count += 1
		return ind_count

	#Mean of all individuals that have been sequenced with at least 1 read
	def mean_coverage(dist_counts,ind_count):
		tot_cov = sum(dist_counts)
		mean_cov = float(tot_cov)/ind_count
		return mean_cov
	#Iterate through pos and counts files simultaneously
	for pos, counts in itertools.izip(posInfo,indCount):
		pos = pos.strip().split("\t")
		counts = counts.strip().split("\t")
		#For each position but the header, extract the scaffold and position, count the number of individuals sequenced, and the mean coverage for all individuals, as well as those with any reads.
		if pos[0] != "chr":
			counts = map(int,counts)
			scaff = pos[0]
			bp = pos[1]
			inds_seq = count_ind(counts)
			mean_cov_all = numpy.mean(counts)
			mean_cov_seq = mean_coverage(counts,inds_seq)
			#For those sites that pass the filters, add them to the individual scaffold dictionaries, or else write them to the sites to exclude file.
			if mean_cov_all > lowerLim and mean_cov_seq < upperLim:
				if scaff not in completed:
					print scaff
					completed.append(scaff)
					for i in range(0,len(ind_order)):
						ind_res_scaffDict[ind_order[i]][scaff] = [int(counts[i])]
				else:
					for i in range(0,len(ind_order)):
						ind_res_scaffDict[ind_order[i]][scaff].append(int(counts[i]))
			else:
				exclude.write(scaff+"\t"+str(int(bp)-1)+"\t"+bp+"\n")
		else:
			for ind in counts:
				ind_res[ind] = []
				ind_res_scaffDict[ind] = {}
				ind_order.append(ind)

	#Write header, with either ind names from counts file, or bam if provided
	if len(bamFile) > 1:
		outMean.write("scaffold\t"+"\t".join(sample_names)+"\n")
		outMedian.write("scaffold\t"+"\t".join(sample_names)+"\n")
		outSD.write("scaffold\t"+"\t".join(sample_names)+"\n")
	else:
		outMean.write("scaffold\t"+"\t".join(ind_order)+"\n")
		outMedian.write("scaffold\t"+"\t".join(ind_order)+"\n")
		outSD.write("scaffold\t"+"\t".join(ind_order)+"\n")

	for scaff in completed:
		scaff_res_mean[scaff] = []
		scaff_res_median[scaff] = []
		scaff_res_sd[scaff] = []
		for ind in ind_order:
			ind_scaff = ind_res_scaffDict[ind][scaff]
			scaff_res_mean[scaff].append(str(round(numpy.mean(ind_scaff),2)))
			scaff_res_median[scaff].append(str(int(numpy.median(ind_scaff))))
			scaff_res_sd[scaff].append(str(round(numpy.std(ind_scaff),2)))

		print scaff+" calculations complete"

	for scaff in completed:
		outMean.write("%s\t%s\n"%(scaff,"\t".join(scaff_res_mean[scaff])))
		outMedian.write("%s\t%s\n"%(scaff,"\t".join(scaff_res_median[scaff])))
		outSD.write("%s\t%s\n"%(scaff,"\t".join(scaff_res_sd[scaff])))


	posInfo.close()
	indCount.close()
	outMean.close()
	outMedian.close()
	outSD.close()
	exclude.close()


if __name__ == "__main__":
		main(sys.argv[1:])
