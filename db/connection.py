from pymongo import MongoClient
from dotenv import load_dotenv
import os


load_dotenv()

client = MongoClient(f'mongodb://{os.getenv("USERNAME_DB")}:{os.getenv("PASSWORD_DB")}@maincluster-shard-00-00.mbqbp.mongodb.net:27017,' \
                     'maincluster-shard-00-01.mbqbp.mongodb.net:27017,' \
                     'maincluster-shard-00-02.mbqbp.mongodb.net:27017/api-monitor?' \
                     'ssl=true&' \
                     'replicaSet=MainCluster-shard-0&' \
                     'authSource=admin&' \
                     'retryWrites=true&' \
                     'w=majority')


def insert_computer(name):
    db = client[os.getenv("NAME_DB")]

    pc_data = {
        'name': name,
    }

    pc = db.computer

    pc_search = pc.find_one(pc_data)

    if pc_search:
        print(pc_search.get('_id'))
        return pc_search.get('_id')
    else:
        result = pc.insert_one(pc_data)
        print('One post: {0}'.format(result.inserted_id))
        return result.inserted_id


def insert_serie(id_computer, data, type, array_serie):
    db = client[os.getenv("NAME_DB")]

    serie_data = {
        'id_computer': id_computer,
        'data': data,
        'type': type,
        'serie': ",".join(map(str, array_serie))
    }

    serie = db.serie

    serie_search = serie.find_one({'id_computer': id_computer, 'data': data, 'type': type})

    if serie_search:
        print(serie_search.get('_id'))
        serie.update_one({'_id': serie_search.get('_id')}, {'$set': {'serie': serie_data.get('serie')}})
        return serie_search.get('_id')
    else:
        result = serie.insert_one(serie_data)
        print('One post: {0}'.format(result.inserted_id))
        return result.inserted_id


def get_series(data, type):
    db = client[os.getenv("NAME_DB")]

    serie_data = {
        'data': data,
        'type': type,
    }

    serie = db.serie
    pc = db.computer

    serie_search = serie.find({'type': type, 'data': data})

    result = []

    for el in serie_search:
        id_computer = el.get('id_computer')
        pc_search = pc.find_one({'_id': id_computer})

        print(el)
        print(id_computer)
        print(pc_search)

        result.append({'serie': el.get('serie'), 'computer': pc_search.get('name')})

    return result