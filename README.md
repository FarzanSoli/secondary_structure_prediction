

python psipred_modal_script.py ./test_psipred.txt ./Secondary_structure_____.fas

### Docker build
----
docker build -t diffuse_bio_script .

### Run the app
----
#### Directory of the input text file : ./test_psipred.txt
#### Directory of the output secondary structure file : ./Secondary.fas
docker run diffuse_bio_script ./test_psipred.txt ./Secondary.fas

modal run psipred_modal_script.py text_file="./test_psipred.txt" output_file="./Secondary.fas"



modal run psipred_modal_script.py --input-text test_psipred.txt --output-directory ./Secondary_structure.fas



modal run psipred_modal_script.py



modal --outdir ./Secondary.fas ./test_psipred.txt run psipred_modal_script.py