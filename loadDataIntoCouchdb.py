from sentiment import sentiment_score
import requests
import json
import re
# print sentiment_score(u'i hate you')

# class twitter_utils:
#     def __init__(self)


class couchDb_utils:
    headers = {
        'Content-Type': 'application/json',
    }

    def __init__(self, server_admin, password, ip_address):
        self.server_admin = server_admin
        self.password = password
        self.ip_address = ip_address
        self.auth = (server_admin, password)

    def insert_document(self, dbs_name, data):
        url = 'http://{ip_address}:5984/{dbs_name}'.format(ip_address=self.ip_address, dbs_name=dbs_name)

        response = requests.post(url, headers=self.headers, data=json.dumps(data), auth=self.auth)
        return response.json()

    def get_document(self, dbs_name, document_id):
        url = 'http://{ip_address}:5984/{dbs_name}/{document_id}'.format(ip_address=self.ip_address,
                                                                         dbs_name=dbs_name, document_id=document_id)

        response = requests.get(url, auth=self.auth)
        return response.json()

    def delete_document(self, dbs_name, document_id, rev):
        url = 'http://{ip_address}:5984/{dbs_name}/{document_id}?rev={rev}'.format(ip_address=self.ip_address,
                                        dbs_name=dbs_name, document_id=document_id, rev=rev)

        response = requests.delete(url, auth=self.auth)
        return response.json()


if __name__ == '__main__':
    my_couchdb = couchDb_utils('admin', 'password', 'localhost')
    # res = my_couchdb.insert_document('demo', {'_id': 'second_record', 'init_balance': 1500})
    # res = my_couchdb.get_document('demo', 'second_record')
    # res = my_couchdb.delete_document('demo', 'second_record', "1-9528dce32655253d363029732a718a23")
    # print res
    with open('tinyTwitter.json', 'r') as f:
        tiny_twitter = json.loads(f.read())
        twitters = tiny_twitter['rows']
        for twitter in twitters:
            text = twitter['doc']['text']
            matched = re.findall(r'https?://t\.co/.{10}', text, re.MULTILINE)
            if matched:
                for strip_str in matched:
                    text = text.replace(strip_str, '')

            score = sentiment_score(text)
            data = {
                'positiveness': score,
                'tweet': text
            }
            my_couchdb.insert_document('demo', data)


