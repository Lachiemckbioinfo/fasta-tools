from Bio import SeqIO
#import sys
import argparse

#Program details
progname = "Fasta-Extractor"
github = "https://github.com/Lachiemckbioinfo/fasta_extractor"

#Initiate argparse
parser = argparse.ArgumentParser(
    prog = f'{progname}',
    description = 'This program uses BioPython to extract fasta sequences from a multifasta using a list of sequence names',
    epilog = f'Thank you for using {progname}. For more details, please visit the GitHub repository at {github}'
)
#Argparse arguments
#Input file (list of gene names)
parser.add_argument("-i", "--input",
                    required=True,
                    type = argparse.FileType('r'),
                    metavar = '',
                    dest = "genelist",
                    help = 'Input file containing sequence list. Sequence names must be one name per line')

parser.add_argument('-f', "--fasta",
                    dest = 'infile',
                    metavar = '',
                    help = 'Input fasta file',
                    required=True)

parser.add_argument("-o", "--out",
                    required=True,
                    metavar = '',
                    type = argparse.FileType('w'),
                    dest = "outfile",
                    help = "Output file name.")


#Parse argparse parser parse
args = parser.parse_args()
genelist_file = args.genelist
infile = args.infile
outfile = args.outfile
outfile_name = outfile.name


#Input files
#genelist_file = sys.argv[1]
#input_fasta = sys.argv[2]
#output_fasta = sys.argv[3]

#ARead genelist_file and append lines to genelist
genelist = []
with genelist_file:
    while line := genelist_file.readline():
        genelist.append(line.rstrip())


def extract_sequences(genelist, infile, outfile):
    #Start counters
    genecount = len(genelist)
    genes_found = 0
    #Establish a list of parsed and absent sequences so that unextracted fastas can later be identified
    genes_parsed = []
    missing_genes = []
    #Open file and extract sequences
    with outfile:
        for record in SeqIO.parse(infile, "fasta"):
            genes_parsed.append(record.id)
            if record.id in genelist:
                SeqIO.write(record, outfile, "fasta")
                genelist.remove(record.id)
                genes_found += 1
                print(f"Gene {record.id} extracted and saved to {outfile_name}")
                
                #Break loop when all sequences are found
                if not genelist:
                    print("All genes extracted")
                    break
        if len(genelist) > 0:
            for gene in genelist:
                if gene not in genes_parsed:
                    missing_genes.append(gene)

    return genecount, genes_found, missing_genes


#Perform fasta sequence extraction
genecount, genes_found, missing_genes = extract_sequences(genelist, infile, outfile)
print(f"Extracted {genes_found} fasta sequences from {infile} and saved them to {outfile_name}.\n")
#Return missing genes
if len(missing_genes) > 0:
    print(f"{len(missing_genes)} fasta sequences were not found. Fasta sequences not found:")
    for gene in missing_genes:
        print(f"{gene}\n")
