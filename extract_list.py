#!/usr/bin/env python3

from Bio import Entrez, SeqIO
import os

# ----------------------------------------------------
# Set your email (required by NCBI)
# ----------------------------------------------------
Entrez.email = input("Enter your email address: ").strip()

# ----------------------------------------------------
# Ask for input file
# ----------------------------------------------------
input_file = input("\nEnter the path to the gene list file: ").strip()

# Check file existence
if not os.path.exists(input_file):
    print("\nERROR: File not found.")
    quit()

# Create output directory
output_dir = "Downloaded_FASTA"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("\nDownloading sequences...\n")

success = 0
failed = 0

# ----------------------------------------------------
# Read file
# ----------------------------------------------------
with open(input_file) as f:

    for line in f:

        line = line.strip()

        # Skip blank lines
        if line == "":
            continue

        # Skip comments/header
        if line.startswith("#"):
            continue

        parts = line.split("\t")

        if len(parts) != 3:
            print("Skipping invalid line:", line)
            failed += 1
            continue

        gene, accession, organism = parts

        print(f"Downloading {gene} ({organism})...")

        try:

            handle = Entrez.efetch(
                db="nucleotide",
                id=accession,
                rettype="fasta",
                retmode="text"
            )

            record = SeqIO.read(handle, "fasta")
            handle.close()

            filename = os.path.join(
                output_dir,
                f"{gene}_{accession}.fasta"
            )

            SeqIO.write(record, filename, "fasta")

            print(f"   Saved -> {filename}")

            success += 1

        except Exception as e:

            print("   Failed:", accession)
            print("   Error :", e)

            failed += 1

print("\n---------------------------------------")
print("Download Complete")
print("---------------------------------------")
print("Successful :", success)
print("Failed     :", failed)
print("Output Dir :", output_dir)