from db.connection import insert_computer, insert_serie
from flask import Flask, request, Response, json
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)

@app.route('/monitor', methods=['POST'])
def inser_data():
    content = request.get_json(force=True)
    computer = content['computer']
    date = content['date']
    info_array = content['info_array']

    if content is None or content == {}:
        return Response(response=json.dumps({"Error": "Please provide connection information"}),
                        status=400,
                        mimetype='application/json')

    id = insert_serie(insert_computer(computer), date, info_array)

    return Response(response=json.dumps({'message': 'insert successfully'}),
                    status=200,
                    mimetype='application/json')



if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


