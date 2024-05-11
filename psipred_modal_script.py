import io
import os
import sys
import json
import modal
import argparse
import subprocess
# =============================================
path_network = os.getcwd()+'r\s4pred'
path_utilities = os.getcwd()+r'\s4pred'
sys.path.append(path_network)
sys.path.append(path_utilities)
# =============================================
# app = modal.App("protein-secondary-structure") 

# =============================================
# @app.function()
def export_fasta(text_file):
    """ Given a text file, this function export '.fas' file. """
    fas_file = os.path.splitext(text_file)[0] + '.fas'
    id_ = None
    # Sequence_dict = {}
    with open(text_file, 'r') as in_file, open(fas_file, 'w') as out_file:
        for line in in_file:
            line = line.split('\t')
            id_ = line[0]
            sequence = line[-1]
            out_file.write(f'>{id_}\n')
            # Write sequence with line breaks every 100 characters
            for i in range(0, len(sequence), 100):
                out_file.write(sequence[i:i+100]+'\n')
    return fas_file

# =============================================
from s4pred import run_model
# @app.function()
def psipred(input_text, output_directory, args):
    # Export FASTA file
    fasta_file = export_fasta(input_text)   
    # Specify the path to run_model.py
    run_model_path = os.path.join('s4pred', 'run_model.py')
    # Construct the command
    command = [
        'python',        # Python interpreter
        run_model_path,  # Path to run_model.py
        '--device', 'gpu',
        '--outfmt', 'fas',
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

# =============================================
# @app.local_entrypoint()
def main():
    parser = argparse.ArgumentParser(description='Predict Secondary Structure with the S4PRED model')
    parser.add_argument('input_text_file', metavar='input_text_file', type=str, 
                        help='text file with protein sequences.')
    parser.add_argument('-d','--device', metavar='d', type=str, default='cpu',
                        help='Device to run on, Either: cpu or gpu (default; cpu).')
    parser.add_argument('-t','--outfmt', metavar='m', type=str, default='fas',
                        help='Output format, Either: ss2, fas, or horiz (default; fas).') 
    parser.add_argument('-o','--output_directory', metavar='o', type=str, default = './results_ss.fas',
                        help='Output directory to save the result file.') 
    # ----------------------------------------
    args = parser.parse_args()   
    output_file = psipred(args.input_text_file, args.output_directory, args)

   
if __name__ == "__main__":
    main()

# modal deploy psipred_modal_script.py ./s4pred/example/test_psipred_dataset.txt -o ./s4pred/example/Test_ss.fas
# f = modal.Function.lookup("protein-secondary-structure")
# f.remote()


# python psipred_modal_script.py ./test_psipred.txt -o ./Secondary_structure.fas


