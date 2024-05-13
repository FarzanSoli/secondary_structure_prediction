
### Docker build
```
docker build -t diffuse_bio_script .
```
### Run the app
```
docker run diffuse_bio_script ./test_psipred_dataset.txt ./Secondary.fas
```
### Run multiple processes
```
docker run diffuse_bio_script ./test_psipred_dataset.txt
```

"./test_psipred_dataset.txt" is the input text file and "./Secondary.fas" is the file under /app that stores the secondary structures. 

### Modal Deploy
----
Modal deploy and run require s4pred package installed, which is not resolved!!

```
modal run psipred_modal_script.py

f = modal.Function.lookup("protein-secondary-structure", "psipred")

f.remote("./test_psipred_dataset.txt", "./Secondary_structure.fas")
```
----

### Modal run
----
```
modal run psipred_modal_script.py --input-text test_psipred_dataset.txt --output-directory ./Secondary_structure.fas
```
