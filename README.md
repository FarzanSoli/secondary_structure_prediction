

python psipred_modal_script.py ./test_psipred.txt -o ./Secondary_structure.fas

### Docker build
----
docker build -t diffuse_bio_script .

### Run the app
----
#### Directory of the input text file : ./test_psipred.txt
#### Directory of the output secondary structure file : ./Secondary.fas
docker run diffuse_bio_script ./test_psipred.txt -o ./Secondary.fas

modal run psipred_modal_script.py --arguments input_text_file="./test_psipred.txt" output_file="./Secondary.fas"
