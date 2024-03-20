# juypter-env

``` bash
docker compose up -d
```

http://localhost:18888/lab?

## how to get python code from ipynb file
``` bash
cd ./work

# way 1
docker run --rm -v $PWD:/home/jovyan/mnt/ -it jupyter/scipy-notebook /bin/bash -c 'cd ./mnt; jupyter nbconvert --to script ./plot-trace-view.ipynb'

# way 2
cat plot-trace-view.ipynb | jq -j '.cells  | map( select(.cell_type == "code") | .source + ["\n\n"] )  | .[][]'
```
