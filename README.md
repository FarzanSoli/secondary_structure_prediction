

python psipred_modal_script.py ./test_psipred.txt -o ./Secondary_structure.fas


docker build -t diffuse_bio_script .

#### Directory of the input text file : ./test_psipred.txt
#### Directory of the output secondary structure file : ./Secondary.fas
docker run diffuse_bio_script ./test_psipred.txt -o ./Secondary.fas

