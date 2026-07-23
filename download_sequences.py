#!/usr/bin/env python3

"""
Automated Biological Sequence Retrieval using Biopython Entrez

Author : Your Name
Purpose:
    Reads a list of Gene Names and Organisms,
    searches NCBI,
    downloads FASTA sequences,
    saves them individually,
    creates a summary CSV report.
"""

from Bio import Entrez
from Bio import SeqIO
import os
import csv

# -----------------------------------------------------
# NCBI Email
# -----------------------------------------------------
Entrez.email = input("Enter your email address: ").strip()

# Optional API Key
api = input("Enter NCBI API Key (Press Enter to skip): ").strip()

if api != "":
    Entrez.api_key = api

# -----------------------------------------------------
# Input File
# -----------------------------------------------------

input_file = input("\nEnter Gene List File : ").strip()

if not os.path.isfile(input_file):
    print("Input file not found.")
    quit()

# -----------------------------------------------------
# Output Folder
# -----------------------------------------------------

output_folder = "Downloaded_FASTA"

os.makedirs(output_folder, exist_ok=True)

# -----------------------------------------------------
# Report File
# -----------------------------------------------------

report_file = "download_report.csv"

report = []

success = 0
failed = 0

print("\nSearching NCBI...\n")

# -----------------------------------------------------
# Read Input File
# -----------------------------------------------------

with open(input_file) as file:

    for line in file:

        line = line.strip()

        if line == "":
            continue

        if line.startswith("#"):
            continue

        try:

            gene, organism = line.split("\t")

        except ValueError:

            print("Invalid line:", line)

            failed += 1

            continue

        print(f"Searching {gene} ({organism})...")

        query = f"{gene}[Gene] AND {organism}[Organism]"

        try:

            # -----------------------------
            # Search
            # -----------------------------

            handle = Entrez.esearch(
                db="nucleotide",
                term=query,
                retmax=1
            )

            result = Entrez.read(handle)

            handle.close()

            if len(result["IdList"]) == 0:

                print("   No record found")

                report.append([
                    gene,
                    organism,
                    "",
                    "",
                    "",
                    "Not Found"
                ])

                failed += 1

                continue

            uid = result["IdList"][0]

            # -----------------------------
            # Download FASTA
            # -----------------------------

            handle = Entrez.efetch(
                db="nucleotide",
                id=uid,
                rettype="fasta",
                retmode="text"
            )

            record = SeqIO.read(handle, "fasta")

            handle.close()

            filename = f"{gene}.fasta"

            filepath = os.path.join(output_folder, filename)

            SeqIO.write(record, filepath, "fasta")

            print("   Downloaded")

            report.append([
                gene,
                organism,
                record.id,
                len(record.seq),
                filename,
                "Success"
            ])

            success += 1

        except Exception as e:

            print("   Error:", e)

            report.append([
                gene,
                organism,
                "",
                "",
                "",
                "Failed"
            ])

            failed += 1

# -----------------------------------------------------
# Write CSV Report
# -----------------------------------------------------

with open(report_file, "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Gene",
        "Organism",
        "Accession",
        "Sequence_Length",
        "FASTA_File",
        "Status"
    ])

    writer.writerows(report)

# -----------------------------------------------------
# Summary
# -----------------------------------------------------

print("\n----------------------------------------")
print("Download Completed")
print("----------------------------------------")

print("Successful :", success)
print("Failed     :", failed)

print("\nOutput Folder :", output_folder)
print("Report File   :", report_file)

print("\nThank you for using Biopython!")
