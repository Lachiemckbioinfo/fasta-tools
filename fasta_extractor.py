from Bio import SeqIO
import sys

#Input files
genelist_file = sys.argv[1]
input_fasta = sys.argv[2]
output_fasta = sys.argv[3]

#ARead genelist_file and append lines to genelist
genelist = []
with open(genelist_file) as file:
    while line := file.readline():
        genelist.append(line.rstrip())


def extract_sequences(genelist, input_fasta, output_fasta):
    #Start counters
    genecount = len(genelist)
    genes_found = 0
    #Establish a list of parsed and absent sequences so that unextracted fastas can later be identified
    genes_parsed = []
    missing_genes = []
    #Open file and extract sequences
    with open(output_fasta, "w") as outfile:
        for record in SeqIO.parse(input_fasta, "fasta"):
            genes_parsed.append(record.id)
            if record.id in genelist:
                SeqIO.write(record, outfile, "fasta")
                genelist.remove(record.id)
                genes_found += 1
                print(f"Gene {record.id} extracted and saved to {output_fasta}")
                
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
genecount, genes_found, missing_genes = extract_sequences(genelist, input_fasta, output_fasta)
print(f"Extracted {genes_found} fasta sequences from {input_fasta} and saved them to {output_fasta}.\n")
#Return missing genes
if len(missing_genes) > 0:
    print(f"{len(missing_genes)} fasta sequences were not found. Fasta sequences not found:")
    for gene in missing_genes:
        print(f"{gene}\n")
