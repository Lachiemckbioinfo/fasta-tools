# This script checks the proportion of a genome assembly that is soft-masked.

from Bio import SeqIO
import sys



masked_bases = 0
total_bases = 0
infile = sys.argv[1]


with open(infile, 'r') as fasta_file:
    print(f"Opening file {infile}")
    for record in SeqIO.parse(fasta_file, "fasta"):
        seq = str(record.seq)
        masked_bases += sum(1 for base in seq if base.islower())
        total_bases += len(seq)

proportion_masked = masked_bases / total_bases
output_file = f"{infile}_masking.txt"

# Write results to output_file.
with open(output_file, "w") as outfile:
    outfile.write(f"Total bases: {total_bases}\n")
    outfile.write(f"Masked bases: {masked_bases}")
    outfile.write(f"Proportion of genome masked: {proportion_masked:.6f}")

# Print out results for general summary
print(f"Total bases: {total_bases}")
print(f"Masked bases: {masked_bases}")
print(f"Proportion of genome masked: {proportion_masked:.4f}")
