from Bio import SeqIO
from collections import defaultdict
import sys


def find_duplicate_seqs(fasta_file):
    #Create dictionary to store sequence IDs
    sequence_dict = defaultdict(list)
    duplicate_ids = []

    #Parse multifasta and store sequences in the dictionary
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequence_dict[record.id].append(record.seq)

    #Find duplicate ids
    for record_id, sequences in sequence_dict.items():
        if len(sequences) > 1:
            duplicate_ids.append(record_id)
    
    return duplicate_ids


fasta_file = sys.argv[1]
duplicates = find_duplicate_seqs(fasta_file)

if duplicates:
    print("Duplicate record IDs found:")
    for duplicate_id in duplicates:
        print(duplicate_id)
    else:
        print("No duplicate record IDs found")
