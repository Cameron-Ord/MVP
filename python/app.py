#importing
import json
from flask import Flask,request, make_response, jsonify
import dbhelper, api_helper
app = Flask(__name__)

@app.post('placeholder')
#function gets called on api request
def placeholder():
   try:
      #calls the function in api_helper to loop through the information sent
         error=api_helper.check_endpoint_info(request.json, ['']) 
         if(error !=None):
            return make_response(jsonify(error), 400)
         #calls the proceedure to insert sent information into the DB
         results = dbhelper.run_proceedure('CALL placeholder(?)', [request.json.get('')])
         #returns results from db run_proceedure
         if(type(results) == list):
            return make_response(jsonify(results), 200)
         else:
            return make_response(jsonify('something has gone wrong'), 500)

   except TypeError:
      print('Invalid entry, try again')
      
   except: 
      print('something went wrong')

if(dbcreds.production_mode == True):
   print()
   print('----Running in Production Mode----')
   print()
   import bjoern #type: ignore
   bjoern.run(app,'0.0.0.0', 5000)
else:
   from flask_cors import CORS
   CORS(app)
   print()
   print('----Running in Testing Mode----')
   print()
   app.run(debug=True)
