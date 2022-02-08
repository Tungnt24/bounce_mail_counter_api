from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient

from settings import Config

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def _get_collection():
    mongo_client = MongoClient(Config.MONGODB_URI)
    db = mongo_client.get_database(Config.MONGODB_DB)
    collection = db.get_collection(Config.MONGODB_COLLECTION)
    return collection


def get_result(records):
    results = {"records": []}
    for record in records:
        results['records'].append({
            "Queue_Id": record.get("QueueId"),
            "From": record.get("From"),
            "To": record.get("To"),
            "Message_Id": record.get("MessageId"),
            "Recipient_Smtp_Ip": record.get("RecipientSmtpIp"),
            "Recipient_Smtp_Domain": record.get("RecipientSmtpDomain"),
            "Status": record.get("Status"),
            "Message": record.get("Message"),
            "Sent_At": record.get("SentAt")
        })
    return results


@app.route("/mail-bounce", methods=['POST'])
@cross_origin()
def get_info_by_mail_from():
    limit = 20
    data = request.get_json()
    email = data.get('email', '')
    collection = _get_collection()
    filter = {
        'Status': 'bounced', 
        'From': f'{email}'
    }
    sort = list({'SentAt': -1}.items())
    records = collection.find(
        filter = filter,
        sort = sort,
        limit = limit
    )
    result = get_result(records)
    return jsonify(result), 200


if __name__ == "__main__": 
    app.run(port=Config.PORT, host=Config.HOST)
