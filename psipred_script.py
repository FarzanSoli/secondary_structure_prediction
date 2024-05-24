import io
import os
import sys
import json
import modal
import argparse
import subprocess
import multiprocessing
from modal import Image
from itertools import starmap
# =============================================
path_network = os.path.join(os.getcwd(), r's4pred')
path_utilities = os.path.join(os.getcwd(), r's4pred')
sys.path.append(path_network)
sys.path.append(path_utilities)
# =============================================
app = modal.App("protein-secondary-structure") 

input_text = modal.Mount.from_local_file(
    local_path=os.getcwd()+"/test_psipred_dataset.txt",
    remote_path="/root/test_psipred_dataset.txt",
)

output_directory = modal.Mount.from_local_file(
    local_path=os.getcwd()+'./Secondary_structure.fas',
    remote_path="/root/Secondary_structure.fas",
)

@app.function(mounts=[input_text, output_directory])
def psipred(input_text, output_directory):
    # Export FASTA file
    fasta_file = os.path.splitext(input_text)[0] + '.fas'
    id_ = None
    # Sequence_dict = {}
    with open(input_text, 'r') as in_file, open(fasta_file, 'w') as out_file:
        for line in in_file:
            line = line.split('\t')
            id_ = line[0]
            sequence = line[-1]
            out_file.write(f'>{id_}\n')
            out_file.write(sequence+'\n')
    # Specify the path to run_model.py
    run_model_path = os.path.join('s4pred', 'run_model.py')
    # Construct the command
    command = [
        'python',        # Python interpreter
        run_model_path,  # Path to run_model.py
        '--device', "cpu",
        '--outfmt', "fas",
        fasta_file,     # Input FASTA file
        ]
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)
    # Check for errors
    if result.returncode != 0:
        print("Error:", result.stderr)
    else:
        with open(output_directory, 'w') as f:
            f.write(result.stdout)
    # -------------------------------------------            
    with open(output_directory, "r") as file:
        # Read the entire content of the file
        content = file.read()
    proteins_info = {}
    proteins = content.strip().split('>')
    for protein in proteins:
        if protein:
            # Split each protein into lines
            lines = protein.strip().split('\n')
            protein_id = lines[0]  # First line contains the ID
            sequence = ''.join(lines[1:])  # The rest of the lines make up the sequence
            # Find the structure (if exists)
            structure_index = sequence.find('CC')  # Assuming structure starts with 'CC'
            if structure_index != -1:
                structure = sequence[structure_index:]  # Extract structure from the sequence
                sequence = sequence[:structure_index]  # Remove structure from the sequence
            else:
                structure = None
            proteins_info[proteins.index(protein)+1] = {'ID': protein_id, 'Structure': structure}
    
    with open(output_directory, 'w') as file:
        json.dump(proteins_info, file, indent=2)

# -----------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run psipred script")
    parser.add_argument("input_text", help="Path to input text file")
    parser.add_argument("output_directory", default = './Secondary_structure.fas', 
                        help="Path to output directory")
    args = parser.parse_args()
    psipred(args.input_text, args.output_directory)

