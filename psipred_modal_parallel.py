import io
import os
import sys
import json
import modal
import argparse
import subprocess
import multiprocessing
from modal import Image
from multiprocessing import Pool
# =============================================
app = modal.App("protein-secondary-structure") 

input_text = modal.Mount.from_local_file(
    local_path=os.getcwd()+"/test_psipred_dataset.txt",
    remote_path="/root/test_psipred_dataset.txt",
)
# =============================================
path_network = os.path.join(os.getcwd(), r's4pred')
path_utilities = os.path.join(os.getcwd(), r's4pred')
sys.path.append(path_network)
sys.path.append(path_utilities)
# =============================================

def process_fasta_file(i, fasta_file):
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
    # Save the result
    return result
# =============================================
@app.function(mounts=[input_text])
def psipred(input_text):
    # Export FASTA file
    fasta_file = os.path.splitext(input_text)[0] + '.fas'
    id_ = None
    sequence_count = 0
    file_count = 0
    fasta_file = os.path.join(os.getcwd(), f"fasta_file_{file_count}.fas")
    fasta_files = []
    Sequence_dict = {}
    with open(input_text, 'r') as in_file:
        for line in in_file:
            line = line.split('\t')
            id_ = line[0]
            sequence = line[-1]
            Sequence_dict[id_] = sequence
            sequence_count += 1
            # If we have reached 5000 sequences, write them to a new fasta file
            if sequence_count % 50 == 0:
                with open(fasta_file, 'w') as out_file:
                    for id_, sequence in Sequence_dict.items():
                        out_file.write(f'>{id_}\n')
                        out_file.write(sequence+'\n')
                # Reset variables for the next chunk
                Sequence_dict = {}
                file_count += 1
                fasta_file = os.path.join(os.getcwd(), f"fasta_file_{file_count}.fas")
                # Append the name of the final generated FASTA file
                fasta_files.append(fasta_file)
        # Write any remaining sequences to a final fasta file
        if Sequence_dict:
            with open(fasta_file, 'w') as out_file:
                for id_, sequence in Sequence_dict.items():
                    out_file.write(f'>{id_}\n')
                    out_file.write(sequence+'\n')
            # Append the name of the final generated FASTA file
            fasta_files.append(fasta_file)
    # ------------------------------------------------
    file_list = []
    for i in range(len(fasta_files)):        
        file_list.append((i,'./'+ os.path.basename(fasta_files[i])))
    return file_list
# =============================================

def save_as_fasta(filename, sequences):
    with open(filename, "w") as file:
        for i, sequence in enumerate(sequences):
            file.write(sequence + "\n")

# =============================================
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run psipred script")
    parser.add_argument("input_text", help="Path to input text file")
    args = parser.parse_args()
    file_list = psipred(args.input_text)
    with Pool(4) as pool:
        # Use pool.starmap to process each file in parallel
        results = process_fasta_file.starmap(file_list)
    for i in range(len(file_list)): 
        save_as_fasta(file_list[i][1], 
                      [">" + x.strip() for x in [''.join(list(results[i].stdout))][0].split(">")[1:] if x.strip()])


