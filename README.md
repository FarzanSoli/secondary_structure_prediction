
### Docker build
```
docker build -t diffuse_bio_script .
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
modal deploy psipred_modal_parallel.py 

f = modal.Function.lookup("protein-secondary-structure", "psipred")

f.remote("./test_psipred_dataset.txt")
```
----

### Modal run
----
```
modal run psipred_modal_parallel.py --input-text test_psipred_dataset.txt
```
