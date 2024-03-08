# IS459 Big Data Architecture Assingment 1

## Prerequisite
1. Install WSL
2. Set up apache airflow
3. Install mongodb on WSL

## How to run
Optional if you want to use virtual environment

1. Rename this repo to dags and put it inside your airflow folder
  - airflow
    - dags
      - twitter_dag.py
      - ...
2. Run `pip install -r requirements`
3. Create .env file and copy and paste from .sample-env, replacing the variables with your own values
4. Download chrome and chromedriver for selenium to run
  - Go to https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json
  - Click the first url under channels -> Stable -> downloads -> chrome
  - Click the first url under channels -> Stable -> downloads -> chromedriver
  - unzip both folder and copy and paste both folder into $HOME directory of your WSL
4. Run `airflow scheduler`
5. Open another terminal and run `airflow webserver --port 8080`
6. Open localhost:8080 and find dag with the name `is459_assignment1_twitter`
7. Click the run button and click `Trigger DAG`
8. Use the web UI to check if DAG is successful
9. Check if documents were successfully inserted into mongodb using mongo shell
10. Open another terminal and run `mongo` (or `mongosh` if ``mongo`` does not work)
11. Run `show dbs`
12. Find the name of the db which is `twitter_db` and run `use twitter_db`
13. Run `show collections` which should give you `{topic}_collection` (replace {topic} with your topic)
14. Run `db.{topic}_collection.find()` to see your tweets
