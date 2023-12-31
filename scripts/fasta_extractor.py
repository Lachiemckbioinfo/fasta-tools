from Bio import SeqIO
#import sys
import argparse

#Program details
progname = "Fasta-Extractor"
github = "https://github.com/Lachiemckbioinfo/fasta_extractor"

#Initiate argparse
parser = argparse.ArgumentParser(
    prog = f'{progname}',
    description = f'{progname} BioPython to extract fasta sequences from a multifasta using a list of sequence names',
    epilog = f'Thank you for using {progname}. For more details, please visit the GitHub repository at {github}'
)
#Argparse arguments
#Input file (list of gene names)
parser.add_argument("-i", "--input",
                    required=False,
                    type = argparse.FileType('r'),
                    metavar = '',
                    dest = "genelist",
                    help = 'Input file containing sequence list. Sequence names must be one name per line. If no file is entered, then the entire fasta file will be extracted.')

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


parser.add_argument("--format",
                    required = False,
                    default = "fasta",
                    metavar = "",
                    dest = "fmt",
                    choices = ["fasta", "pir", "tab", "fasta-2line"],
                    help = "Output format. Options: 'fasta', 'fasta-2line', 'pir', 'tab'. Default = fasta")

#If intending to use genbank, seqxml or imgt formats, then molecule type will have to be defined
#xdna works as well


parser.add_argument("--quiet",
                    required=False,
                    help = "Silence print messages. Default = false",
                    action = 'store_true')


#Parse argparse parser parse
args = parser.parse_args()
genelist_file = args.genelist
infile = args.infile
outfile = args.outfile
outfile_name = outfile.name
quiet = args.quiet
fmt = args.fmt

'''
if fmt == 'xdna':
    openmode = 'wb'
else:
    openmode = "w"
'''


#Read genelist_file and append lines to genelist
genelist = []
if genelist_file is not None:
    with genelist_file:
        while line := genelist_file.readline():
            genelist.append(line.rstrip())
else:
    if quiet == False:
        print(f"Extracting all fasta sequences from {infile}")
    for record in SeqIO.parse(infile, "fasta"):
        genelist.append(record.id)


def extract_sequences(genelist, infile, outfile):
    #Start counters
    genecount = len(genelist)
    genes_found = 0
    #Establish a list of parsed and absent sequences so that unextracted fastas can later be identified
    genes_parsed = []
    missing_genes = []
    


    #Open file and extract sequences
    #with open(outfile, openmode):
    with outfile:
        if quiet == False:
                print(f'Reading fasta file {infile}')
        for record in SeqIO.parse(infile, "fasta"):
            genes_parsed.append(record.id)
            if record.id in genelist:
                SeqIO.write(record, outfile, fmt)
                genelist.remove(record.id)
                genes_found += 1
                if quiet == False:
                    print(f"Gene {record.id} extracted and saved to {outfile_name} ({genes_found}/{genecount})")
                
                #Break loop when all sequences are found
                if not genelist:
                    if quiet == False:
                        print("All genes extracted")
                    break
        if len(genelist) > 0:
            for gene in genelist:
                if gene not in genes_parsed:
                    missing_genes.append(gene)

    return genecount, genes_found, missing_genes


#Perform fasta sequence extraction
genecount, genes_found, missing_genes = extract_sequences(genelist, infile, outfile)
if quiet == False:
    print(f"Extracted {genes_found} fasta sequences from {infile} and saved them to {outfile_name}.\n")

#Return missing genes
if quiet == False:
    if len(missing_genes) > 0:
        print(f"{len(missing_genes)} fasta sequences were not found. Fasta sequences not found:")
        for gene in missing_genes:
            print(f"{gene}\n")
