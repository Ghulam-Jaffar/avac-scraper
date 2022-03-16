from bson import json_util, ObjectId
from genericpath import exists
from flask import Flask, jsonify, request, Response
from scrapperScript import Scrapper
from productHunter import model
# from scrapper.babaScrapper import BabaScrapper
import pymongo
import requests
import json
import certifi

app = Flask(__name__)

app.config["SECRET_KEY"] = "ef87661fe21afc571439319a"

try:
    # client = pymongo.MongoClient("mongodb://localhost:27017/ScrapedData")
    # client = pymongo.MongoClient("mongodb+srv://Najmi:najmi12345@cluster0.47azh.mongodb.net/myFirstDatabase", tlsCAFile=certifi.where())
    client = pymongo.MongoClient(
        "mongodb+srv://avac:avac7809@avac.f3lnt.mongodb.net/ScrapedData?retryWrites=true&w=majority", tlsCAFile=certifi.where())

    db = client.get_database('myFirstDatabase')
    scrapedCol = pymongo.products.Collection(db, 'scrapedProducts')
    huntedCol = pymongo.recommendedproducts.Collection(
        db, 'recommendedProducts')

except:
    print("didnt work")


@app.route('/')
def simple():
    return "Hello TO AVAC's BACK BONE"


# @app.route('/drop')
# def lulu():
#     db.drop_collection("livetrender")
#     db.lulu.insert_one({'TEST': "PASS"})
#     return "dropped"


try:
    @app.route('/productHunter/<int:cat>/<int:subCat>/<int:lastCategory>/<int:nPages>')
    def productHunter(cat, subCat, lastCategory, nPages):
        sProduct = Scrapper(cat, subCat, lastCategory, nPages)
        for i in range(len(sProduct)):
            check = True
            for x in db.products.find({}, {'ASIN': 1}):
                if sProduct[i]['ASIN'] == x['ASIN']:
                    check = False
                    break
            if check == True:
                db.products.insert_one(
                    json.loads(json_util.dumps(sProduct[i])))
        hunted = model(sProduct)
        print(len(hunted))
        db.db.collection.find_one()
        for i in range(len(hunted)):
            db.recommendedproducts.insert_one(
                json.loads(json_util.dumps(hunted[i])))
        hunted.clear()
        sProduct.clear()
        return "worked"
except:
    print("ended")

try:
    @ app.route('/getDataApi/<int:cat>/<int:subCat>/<int:lastCategory>/<int:nPages>')
    def getDataApi(cat, subCat, lastCategory, nPages):
        # print(Scrapper(cat, subCat, lastCategory, nPages))
        # return Response(json.dumps(Scrapper(cat, subCat, lastCategory, nPages)), mimetype='application/json')

        sProduct = Scrapper(cat, subCat, lastCategory, nPages)
        # to add scraped data in general collection
        for i in range(len(sProduct)):
            check = True
            for x in db.products.find({}, {'ASIN': 1}):
                if sProduct[i]['ASIN'] == x['ASIN']:
                    check = False
                    break
            if check == True:
                db.products.insert_one(
                    json.loads(json_util.dumps(sProduct[i])))

        for i in range(len(sProduct)):
            check = True
            # for new collection everytime, specific for real time
            for x in db.realtimetrender.find({}, {'ASIN': 1}):
                if sProduct[i]['ASIN'] == x['ASIN']:
                    check = False
                    break
            if check == True:
                db.products.insert_one(
                    json.loads(json_util.dumps(sProduct[i])))

        return "worked"
        # data = json.loads(Scrapper(cat, subCat, lastCategory, nPages))
        # return Scrapper(cat, subCat, lastCategory, nPages)
except:
    print("ended")

try:
    @ app.route('/livetrender/<int:cat>/<int:subCat>/<int:lastCategory>/<int:nPages>')
    def livetrender(cat, subCat, lastCategory, nPages):
        # print(Scrapper(cat, subCat, lastCategory, nPages))
        # return Response(json.dumps(Scrapper(cat, subCat, lastCategory, nPages)), mimetype='application/json')

        # scraper
        sProduct = Scrapper(cat, subCat, lastCategory, nPages)

        # drop current live trender collection
        db.drop_collection("livetrender")

        # to add scraped data in general collection
        for i in range(len(sProduct)):
            check = True
            for x in db.livetrender.find({}, {'ASIN': 1}):
                if sProduct[i]['ASIN'] == x['ASIN']:
                    check = False
                    break
            if check == True:
                db.livetrender.insert_one(
                    json.loads(json_util.dumps(sProduct[i])))

        # for updated new real time live trender collection
        for i in range(len(sProduct)):
            check = True
            for x in db.livetrender.find({}, {'ASIN': 1}):
                if sProduct[i]['ASIN'] == x['ASIN']:
                    check = False
                    break
            if check == True:
                db.livetrender.insert_one(
                    json.loads(json_util.dumps(sProduct[i])))

        return "worked"
except:
    print("ended")


if __name__ == '__main__':
    app.run(debug=True)


# response = requests.post("http://127.0.0.1:5000/quarks", json={})
# body = {}
# requests.post('sdlfjsdl', data=body)

# {"value" : [
#     {
#         'prId': 1
#     },
#     {
#         'prId': 1
#     },
#     {
#         'prId': 1
#     },
#     {
#         'prId': 1
#     },
#     {
#         'prId': 1
#     },
#     {
#         'prId': 1
#     },
# ]}
