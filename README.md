This code returns secondary structure of a given protein sequences (in this case, an example file "test_psipred_dataset.txt") using [s4pred](https://github.com/psipred/s4pred) package. Following instructions show how to build local application and acquire the secondary structure. 

"psipred_parallel.py" is similar to "psipred_script.py" where you can run the process in parallel on cpu. 

You can change the device within both "psipred_parallel.py" and "psipred_script.py" files. If you want to run "psipred_parallel.py" code, update the docker file accordingly (commented lines within docker file).

### Docker build
```
docker build -t secondary_structure_prediction .
```
### Run multiple processes
```
docker run secondary_structure_prediction ./test_psipred_dataset.txt ./Secondary_structure.fas
```

"./test_psipred_dataset.txt" is the input text file and "./Secondary_structure.fas" is the file under /app that stores the secondary structures. 

