import pymongo
from urllib.parse import quote_plus
from git import Repo
import autocactus_settings as aset



def get_from_db():
    """
    Get message from MongoDB
    """
    mongo_uri = "mongodb://{0}:{1}@{2}/{3}".format(quote_plus(aset.MONGODB_USER),
                                               quote_plus(aset.MONGODB_PASSWORD),
                                               aset.MONGODB_SERVER,
                                               aset.MONGODB_DBNAME)
    client = pymongo.MongoClient(mongo_uri)
    db = client[aset.MONGODB_DBNAME]
    curso = db[aset.MONGODB_DBNAME].find({'status': 'new'})
    posts = []
    for doc in curso:
      posts.append(doc)

    return posts

def publish():
    """
    Publisher main function.
    """
    posts = get_from_db()

get_from_db()
