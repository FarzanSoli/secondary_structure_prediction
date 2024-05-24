
### Docker build
```
docker build -t diffuse_bio_script .
```
### Run multiple processes
```
docker run diffuse_bio_script ./test_psipred_dataset.txt ./Secondary_structure.fas
```

"./test_psipred_dataset.txt" is the input text file and "./Secondary_structure.fas" is the file under /app that stores the secondary structures. 

