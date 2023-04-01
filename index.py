try:
    from flask import Flask, jsonify, request
    from pymongo import MongoClient
    from bson.json_util import dumps
    from bson.objectid import ObjectId
    import json
    from datetime import datetime
    from bson import json_util
    from flask_socketio import SocketIO
    from flask_cors import CORS
except Exception as e:
    print("Some Modules are Missing :{}".format(e))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# database connection
def databaseConnection():
   CONNECTION_STRING = "mongodb+srv://emseccomandcenter:TUXnEN09VNM1drh3@cluster0.psiqanw.mongodb.net/?retryWrites=true&w=majority"
   client = MongoClient(CONNECTION_STRING)
   return client['Main_ForumFilter_Data']
db = databaseConnection()

# XPATH collection 
xpath_collection = db["Xpath_forum"]

# LoginCredential collection 
login_collection = db["login_credentials"]

# ForumLink collection 
link_collection = db["forum_Links"]

# socket send data
@app.route('/sendData',methods=['POST'])
def sendData():
    data=request.json['data']
    socketio.emit('data',data)
    return jsonify({'result':'OK'})

# socket send log
@app.route('/sendLog',methods=['POST'])
def sendLog():
    data=request.json['msg']
    socketio.emit('log',data)
    return jsonify({'result':'OK'})

# Fetch all data (forum XPATH)
@app.route('/forum',methods=['GET','POST'])
def xpaths():
    if request.method =='GET':
        XPATH = xpath_collection.find()
        resp = dumps(XPATH)
        return resp
    site=request.json['site']
    sectionPath =request.json['sectionPath'] 
    urlPath=request.json['urlPath']
    lastModPath=request.json['lastModPath']
    path_of_sectionNext_btn=request.json['path_of_sectionNext_btn']
    title_path=request.json['title_path']
    iterator_path=request.json['iterator_path']
    author_name_path = request.json['author_name_path']
    profile_link_path=request.json['profile_link_path']
    date_path=request.json['date_path']
    body_path=request.json['body_path']
    media_path=request.json['media_path']
    path_of_next_btn=request.json['path_of_next_btn']
    expand_btn=request.json['expand_btn']
    failed_count = 0
    status = None
    time = datetime.strptime(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), "%Y-%m-%dT%H:%M:%S")
    isUrgent = False
    
    if xpath_collection.count_documents({'site':site})>0:
        return jsonify("url Already exist.. Update the field if you need")
    if request.method == "POST":
        xpath_collection.insert_one({'site':site,'sectionPath':sectionPath,'urlPath':urlPath,'lastModPath':lastModPath,'path_of_sectionNext_btn':path_of_sectionNext_btn,'title_path':title_path,'iterator_path':iterator_path,'author_name_path':author_name_path,'profile_link_path':profile_link_path,'date_path':date_path,'body_path':body_path,'media_path':media_path,'failedCount':failed_count,'path_of_next_btn':path_of_next_btn,'expand_btn':expand_btn,'failed_count':failed_count,'status':status,'time':time,'isUrgent':isUrgent})
        resp = jsonify("Data added successfully!!")
        resp.status_code = 200
        return resp
    else:
        return not_found()

# GET , PUT and UPDATE ForumXPATH
@app.route('/forum/<id>', methods=['GET','DELETE','PUT'])
def Forum(id):
    if request.method=='GET':
        if(xpath_collection.count_documents({'_id':ObjectId(id)})>0):
            data =xpath_collection.find_one({'_id':ObjectId(id)})
            user = dumps(data)
            return user
        else:
            resp = jsonify("No Data")
            resp.status_code = 204
            return resp
        
    if request.method=='DELETE':
        if(xpath_collection.count_documents({"_id": ObjectId(id)})>0):
            query = {"_id": ObjectId(id)}
            xpath_collection.delete_one(query)
            resp = jsonify("Field Deleted!!")
            resp.status_code = 200
            return resp
        else:
            resp = jsonify("Already Deleted!!")
            resp.status_code = 200
            return resp

    if request.method =='PUT':
        _site=request.json['site']
        _sectionPath =request.json['sectionPath'] 
        _urlPath=request.json['urlPath']
        _lastModPath=request.json['lastModPath']
        _path_of_sectionNext_btn=request.json['path_of_sectionNext_btn']
        _title_path=request.json['title_path']
        _iterator_path=request.json['iterator_path']
        _author_name_path = request.json['author_name_path']
        _profile_link_path=request.json['profile_link_path']
        _date_path=request.json['date_path']
        _body_path=request.json['body_path']
        _media_path=request.json['media_path']
        _path_of_next_btn=request.json['path_of_next_btn']
        _expand_btn=request.json['expand_btn']
        _failed_count = 0
        _status = "not started"
        _time = datetime.strptime(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), "%Y-%m-%dT%H:%M:%S")
        _isUrgent = False
        
        dict = {}
        if(len(str(_site))>0):
            dict['site'] = _site
        if(len(str(_sectionPath))>0):
            dict['sectionPath'] = _sectionPath 
        if(len(str(_urlPath))>0):
            dict['urlPath'] = _urlPath
        if(len(str(_lastModPath))>0):
            dict['lastModPath'] = _lastModPath
        if(len(str(_path_of_sectionNext_btn))>0):
            dict['path_of_sectionNext_btn'] = _path_of_sectionNext_btn
        if(len(str(_title_path))>0):
            dict['title_path'] = _title_path
        if(len(str(_iterator_path))>0):
            dict['iterator_path'] = _iterator_path
        if(len(str(_author_name_path))>0):
            dict['author_name_path'] = _author_name_path
        if(len(str(_profile_link_path))>0):
            dict['profile_link_path'] = _profile_link_path
        if(len(str(_date_path))>0):
            dict['date_path'] = _date_path
        if(len(str(_body_path))>0):
            dict['body_path'] = _body_path
        if(len(str(_media_path))>0):
            dict['media_path'] = _media_path
        if(len(str(_path_of_next_btn))>0):
            dict['path_of_next_btn'] = _path_of_next_btn
        if(len(str(_expand_btn))>0):
            dict['expand_btn'] = _expand_btn
        if(len(str(_status))>0):
            dict['status'] = _status    
        if(len(str(_isUrgent))>0):
            dict['isUrgent'] = _isUrgent
            
        # update values in database
        xpath_collection.find_one_and_update({"_id":ObjectId(id)},{"$set":dict})
                
        resp = jsonify("Website updated")
        resp.status_code = 200
        return resp

# ----------------------------LOGIN----------------------------
# Fetch all data (forum loginCredentials)
@app.route('/forumLogin',methods =['GET'])
def logins():
    if(request.method =='GET'):
        try:
            loginsdata = login_collection.find()
            resp = dumps(loginsdata)
            return resp
        except:
            resp = jsonify("No Data")
            resp.status_code = 204
            return resp
    
    site=request.json['site']
    loginId =request.json['loginId']
    password=request.json['password']
        
    if login_collection.count_documents({'site':site})>0:
        return jsonify("Already exist!!")
    if request.method == "POST":
        login_collection.insert_one({'site':site,'loginId':loginId,'password':password})
        resp = jsonify("Data added successfully!!")
        resp.status_code = 200
        return resp
    else:
        return not_found()
         
# GET , PUT and UPDATE LoginCredential
@app.route('/forumLogin/<id>',methods=['GET','DELETE','PUT'])
def LoginID(id):
    if (request.method =='GET'):
        try:
            login_data =login_collection.find_one({'_id':ObjectId(id)})
            user_login = dumps(login_data)
            return user_login
        except:
            resp = jsonify("No Data")
            resp.status_code = 204
            return resp
        
    if request.method=='DELETE':
        try:
            query = {"_id": ObjectId(id)}
            login_collection.delete_one(query)
            resp = jsonify("Field Deleted!!")
            resp.status_code = 200
            return resp
        except:
            resp = jsonify("Already Deleted!!")
            resp.status_code = 208
            return resp

    if request.method =='PUT':
        _site=request.json['site']
        _loginId =request.json['loginId']
        _password=request.json['password']
                
        dict = {}
        if(len(str(_site))>0):
            dict['site'] = _site
        if(len(str(_loginId))>0):
            dict['loginId'] = _loginId
        if(len(str(_password))>0):
            dict['password'] = _password        
        
        # update values in database
        login_collection.find_one_and_update({"_id":ObjectId(id)},{"$set":dict})
                
        resp = jsonify("Website updated")
        resp.status_code = 200
        return resp    


# ----------------------------------Forum LINKS--------------------------------

#ALL Links
@app.route('/forumLinks',methods =['GET','POST'])
def ForumLinks():
    if(request.method=='GET'):
        try:    
            fLinks =link_collection.find()
            linksData =dumps(fLinks)
            return linksData
        except:
            resp = jsonify("No Data")
            resp.status_code = 204
            return resp
        
# GET , PUT and UPDATE LoginCredential
@app.route('/forumLinks/<id>',methods=['GET','DELETE','PATCH'])
def ForumLink(id):
    if (request.method =='GET'):
        try:
            fLink =link_collection.find_one({'_id':ObjectId(id)})
            link_data = dumps(fLink)
            return link_data
        except:
            resp = jsonify("No Data")
            resp.status_code = 204
            return resp
        
    if (request.method=='DELETE'):
        try:
            query = {"_id": ObjectId(id)}
            link_collection.delete_one(query)
            resp = jsonify("Field Deleted!!")
            resp.status_code = 200
            return resp
        except:
            resp = jsonify("Already Deleted!!")
            resp.status_code = 208
            return resp
    
    if( request.method =='PATCH'):
        _isUrgent=request.json['isUrgent']
        dict ={}
        dict['isUrgent'] = _isUrgent
        if(link_collection.find_one({"_id":ObjectId(id),'isUrgent':False})):

            # update values in database
            link_collection.find_one_and_update({"_id":ObjectId(id)},{"$set":dict})
            resp = jsonify("Website updated")
            resp.status_code = 200
            return resp    
        else:
            resp = jsonify("Already Updated!!")
            resp.status_code = 208
            return resp        

        

# Error Handling...
@app.errorhandler(404)
def not_found(error = None):
    message = {
        'status': 404,
        'message' : 'Not Found' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp    


if __name__=='__main__':
    app.run(debug=True)






















 # if (request.method =='GET'):
    #     try:
    #         fLink =link_collection.find_one({'_':url})
    #         link_data = dumps(fLink)
    #         return link_data
    #     except:
    #         resp = jsonify("No Data")
    #         resp.status_code = 204
    #         return resp
        
    # if request.method=='DELETE':
    #     try:
    #         query = {"url": url}
    #         link_collection.delete_one(query)
    #         resp = jsonify("Field Deleted!!")
    #         resp.status_code = 200
    #         return resp
    #     except:
    #         resp = jsonify("Already Deleted!!")
    #         resp.status_code = 208
    #         return resp

    # if request.method =='PATCH':
    #     try:
    #         # update values in database
    #         login_collection.find_one_and_update({'url':url},{"$set":{'isUrgent':True}})    
    #         resp = jsonify("Site updated!!")
    #         resp.status_code = 200
    #         return resp    
    #     except:
    #         resp = jsonify("Already Updated!!")
    #         resp.status_code = 200
    #         return resp