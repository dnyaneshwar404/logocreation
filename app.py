"""
Author      : Suraj Nanavare
Created At  : 26 June 2019
Description : This is sample flask application with sample API 
              to get current date and time.

Forked By   : Dnyaneshwar Harer
Modified At : 29 June 2019 10pm
Description : Hackathon Assignement 2 
Dependancies: Data file "data/companyData.json" which contain company details.

"""

from flask import Flask, request, jsonify, render_template
import operator, collections
import json
import os

app = Flask(__name__)
app.config["DEBUG"] = True

dataSource = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/companyData.json")

def readJsonData(dataSource):
    fp = open(dataSource,'r')
    data = json.loads(fp.read())
    return data

def getLogoCharecters(company):
    oCompanyName =company['Company Name']
    """
    The special charecters like space( ), dot(.) and amper(&) sign will be eliminated
    the Upper case company name will be used for processing
    """
    companyName = company['Company Name'].upper().replace(' ', '').replace('.', '').replace('&', '')
    print("C_Name = ",companyName)
    companyId = company['CompanyId']
    print("in logo charecters")
    #process company name
    logoCharectorsDict={}
    tempCompanyNameDict = {}  # Create empty hash 

    """
    If keywords of the company less than 3 then will show the message to user
    """
    if len(companyName)<3:
        result = {
            "statusCode" : "500",
            "message" : "Company Name is having less than 3 charecters"
        }

    """
    Creating temparary dict to store string charecters later will use it for pricessing (sorting)
    """
    for ch in companyName: 
        if ch in tempCompanyNameDict:
            tempCompanyNameDict[ch]+=1
            isRepeated = True
        else:
            tempCompanyNameDict[ch]=1

    #sorting values based on charecters occurance in string
    valuesSortedList = sorted(tempCompanyNameDict.items(), key=operator.itemgetter(1), reverse = True)
    print("Max Occured charecter :: ",valuesSortedList[0][0])
    logoCharectorsDict["0"] = valuesSortedList[0][0];

    #sorting keys based on alhpabetical order

    keysSortedList = sorted(tempCompanyNameDict.items(), key=operator.itemgetter(0))
    print("key Sorted ::",keysSortedList)

    #adjusting the charecters required for output

    if valuesSortedList[0][1] > 1:
        logoCharectorsDict["0"] = valuesSortedList[0][0];
        if valuesSortedList[0][0]==keysSortedList[0][0]:
            logoCharectorsDict["1"] = keysSortedList[1][0];
            logoCharectorsDict["2"] = keysSortedList[2][0];
        else:
            logoCharectorsDict["1"] = keysSortedList[0][0];
            logoCharectorsDict["2"] = keysSortedList[1][0];
    else:
        logoCharectorsDict["0"] = keysSortedList[0][0];
        logoCharectorsDict["1"] = keysSortedList[1][0];
        logoCharectorsDict["2"] = keysSortedList[2][0];

    print("logo chars=== ", logoCharectorsDict)
    logoCharecters = logoCharectorsDict["0"]+','+logoCharectorsDict["1"]+','+logoCharectorsDict["2"]
    print(logoCharecters)

    result = {
        "statusCode" : "200",
        "data":{
            "companyId":companyId , 
            "companyName":oCompanyName,
            "logoCharacters": logoCharecters
        }
    }
    return result

# @app.route('/testX', methods=['GET'])
def getCompanyDetails(companyId):
    companyData = readJsonData(dataSource)
    companyList = companyData['companyList']
    filteredComapanyData=[]
    for company in companyList:
        if company['CompanyId'] == companyId:
            print("in if")
            filteredComapanyData = getLogoCharecters(company)
    
    if filteredComapanyData:
        print("ok")
    else:
        filteredComapanyData = {
            "statusCode" : "404",
            "message":"Comapny not found for given ID" , 
            "data":"",
        }
    
    return jsonify(filteredComapanyData)
    

@app.route('/', methods=['GET'])
def home():
    homeData = {
        "status" : "200",
        "data" : "Welcome, This is home Page"
    }
    return render_template('home.html')

@app.route('/getCompanyLogo', methods=['POST'])
def getCompanyLogo():
    companyId = request.form.get('companyId')
    print(request.form.get('companyId'))
    companyResult = getCompanyDetails(companyId)
    return companyResult

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({ "status": "404","data" : "Page Not Found!" })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
