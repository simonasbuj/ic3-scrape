# IC3 Scrape

Scrapes data from https://www.ic3.gov/Media/PDF/AnnualReport/2016State/StateReport.aspx?s=1 for years 2016-2023 and 57 states.
Exports results to postgres and as parquet files partitioned by year/state.   
Years and states can be changed in config.

Postgres is not required, if it's not up, it's just going to skip the upload.
Logs can be found in local "/logs" folder, even if it's running in docker.   
Consecutive docker runs also take local config changes.

## How To Run
#### docker-compose (also starts local postgres):
```
docker-compose up --build -d

# consecutive runs
docker start sb-shark-app
```

#### Poetry:
```
poetry install --no-dev
poetry run python main.py
```

### pip:
```
pip install -r requirements.txt
python main.py 
```


## Running Tests
#### Poetry:
```
poetry install
poetry run pytest
```

### pip:
```
pip install -r requirements.txt
pytest
```

### docker:
```
mac/linux:
  docker run -it --rm $(docker build -f run_tests.Dockerfile -q .)

windows:
  FOR /F %i IN ('docker build -f run_tests.Dockerfile -q .') DO docker run -it --rm %i

clean images created by running tests in docker:
  docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
```


 
