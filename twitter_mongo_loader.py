'''

Name: Seah Pei Ming
Email: pmseah.2020@scis.smu.edu.sg

'''

import os
from pymongo import MongoClient
import json 
from dotenv import load_dotenv

def run_mongo_loader():

    # COMPLETE THIS PART

    # Refer to the OVERVIEW diagram

    # This script must retrieve the tweets info from a JSON file (e.g. earthquake.json)
    # and insert each tweet as a DOCUMENT into MongoDB


    # For example:
    # Given a tweet with:
    #    ID: 1623735160020541442
    #    Text: #Donation #Unicef #TurkeyEarthquake Donate blankets and clothing
    #
    # Create a DOCUMENT that looks like this:
    #    {
    #        "tweet_id": "1623735160020541442",
    #        "tweet_text": "#Donation #Unicef #TurkeyEarthquake Donate blankets and clothing"
    #    }
    #
    # IMPORTANT
    #    No duplicates allowed in MongoDB collection.
    #    2 or more documents with the same tweet_id (e.g. 1623735160020541442) will NOT be allowed.
    

    # Next, your script must insert each such DOCUMENT into MongoDB
    #    It is up to you how you name your Database, e.g. twitter
    #    Collection name must match the topic, e.g. earthquake


    # Lastly, once all tweets are inserted into MongoDB as DOCUMENTS
    #    Delete/remove the input JSON file from the file system (e.g. earthquake.json)
    
    
    # Please verify that your Python script works by running it stand-alone (not as part of DAG)
    # In this case, you should go into MongoDB shell and
    # see if Database "twitter" --> Collection "earthquake" is populated with data.
    # You can use Jupyter Notebook for this.

    load_dotenv()

    topic = ""
    # find all .json files in the current directory
    dag_file_path = os.path.abspath(__file__)
    dag_dir_path = os.path.dirname(dag_file_path)
    for file in os.listdir(dag_dir_path):
        if file.endswith(".json"):
            topic = file.split('.')[0]

    # client = MongoClient(os.environ.get("MONGO_URI"))
    client = MongoClient()
    twitter_db = client['twitter_db']
    twitter_collection = twitter_db[f'{topic}_collection']

    output_file_path = os.path.join(os.path.dirname(dag_file_path), f'{topic}.json')
    with open(output_file_path) as f:
        file_data = json.load(f)

    twitter_collection.create_index([('tweet_id', 1)], unique=True)
    twitter_collection.insert_many(file_data, ordered=False)

    os.remove(output_file_path)


if __name__ == "__main__":
    run_mongo_loader()