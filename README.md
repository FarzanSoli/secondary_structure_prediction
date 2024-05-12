
### Docker build
----
docker build -t diffuse_bio_script .

### Run the app
----
#### Directory of the input text file : ./test_psipred_dataset.txt
#### Directory of the output secondary structure file : ./Secondary.fas
docker run diffuse_bio_script ./test_psipred_dataset.txt ./Secondary.fas
----
### Modal Deploy
----
modal run psipred_modal_script.py
f = modal.Function.lookup("protein-secondary-structure", "psipred")
f.remote("./test_psipred_dataset.txt", "./Secondary_structure.fas")
----

### Modal run
----
modal run psipred_modal_script.py --input-text test_psipred_dataset.txt --output-directory ./Secondary_structure.fas

