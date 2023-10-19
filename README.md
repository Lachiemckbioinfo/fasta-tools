# Fasta extractor
Fasta Extractor is a straightforward Python script for extracting fasta sequences from a multifasta file using a list of sequence names. Fasta extractor uses Argparse and BioPython to parse input files and fasta sequences.

## Installation
The only external requirement that Fasta Extractor needs is BioPython. This can be installed using pip.
```
pip install -r requirements.txt
```

## Usage
```
usage: Fasta-Extractor [-h] -i  -f  -o

Fasta-Extractor BioPython to extract fasta sequences from a multifasta using a list of sequence names

options:
  -h, --help     show this help message and exit
  -i , --input   Input file containing sequence list. Sequence names must be one name per line
  -f , --fasta   Input fasta file
  -o , --out     Output file name.

Thank you for using Fasta-Extractor. For more details, please visit the GitHub repository at https://github.com/Lachiemckbioinfo/fasta_extractor
```

Fasta Extractor has three required commands: input file (your gene list, ```-i/--input```), fasta file (where you are extracting sequences from, ```-f/--fasta```), and output file (where fasta sequences are being saved to, ```-o/--out```).

An example usage of Fasta Extractor would look like this:
```
python fasta_extractor.py --input genelist.txt --fasta sequences.fa --out output_sequences.fa
```
