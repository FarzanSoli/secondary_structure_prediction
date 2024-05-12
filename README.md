

python psipred_modal_script.py ./test_psipred.txt -o ./Secondary_structure.fas



docker build -t diffuse_bio_script .

docker run diffuse_bio_script ./test_psipred.txt ./Secondary_structure.fas



docker run diffuse_bio_script ./test_psipred.txt -o ./Secondary.fas

