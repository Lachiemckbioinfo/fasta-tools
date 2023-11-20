from Bio import SeqIO
import sys

def update_query_descriptions(template_file, query_file, output_file):
    # Load protein sequences and their descriptions
    template_sequences = SeqIO.to_dict(SeqIO.parse(template_file, "fasta"))
    print("Parsed template sequences")

    # Create a list to store updated CDS sequences
    updated_query_records = []
    missing_records = []
    # Parse CDS sequences and update descriptions
    for query_record in SeqIO.parse(query_file, "fasta"):
        # Check if the CDS sequence has a corresponding protein sequence
        if query_record.id in template_sequences:
            # Update the description using the BLAST result from the protein sequence
            template_description = template_sequences[query_record.id].description
            updated_query_record = query_record
            updated_query_record.description = template_description
            updated_query_records.append(updated_query_record)
            print(f"Parsed {updated_query_record.id}")
        else:
            missing_records.append(query_record.id)
    # Write the updated CDS sequences to the output file
    with open(output_file, "w") as output_handle:
        SeqIO.write(updated_query_records, output_handle, "fasta")
        print(f"Wrote updated records to {output_handle}")
    with open("logfile.txt", "w") as logfile:
        logfile.write(f"Missing records: {len(missing_records)}\n")
        for record in missing_records:
            logfile.write(f"{record}\n")


if __name__ == "__main__":
    # Replace the file paths with your actual file paths
    template_fasta = sys.argv[1]
    query_fasta = sys.argv[2]
    output_fasta = sys.argv[3]

    # Call the function to update CDS descriptions
    update_query_descriptions(template_fasta, query_fasta, output_fasta)
