from flask import Flask, request, make_response, send_from_directory, jsonify
import dbhelper,api_helper,dbcreds, uuid

app = Flask(__name__)


try:
   @app.post('/api/admin')
   
   def create_admin():
      
         error=api_helper.check_endpoint_info(request.json, ['username', 'password']) 
         if(error !=None):
            return make_response(jsonify(error), 400)

         results = dbhelper.run_proceedure('CALL create_admin(?,?)', 
               [request.json.get('username'), request.json.get('password')])
         
      
         if(type(results) == list):
            return make_response(jsonify(results), 200)
         else:
            return make_response(jsonify('something has gone wrong'), 500)
         
      
except TypeError:
   print('Invalid entry, try again')
   
except: 
   print('something went wrong')

try:

   @app.post('/api/admin-login')
   def admin_login():
      
         error=api_helper.check_endpoint_info(request.json, ['username','password']) 
         if(error !=None):
            return make_response(jsonify(error), 400)

         token = uuid.uuid4().hex
         results = dbhelper.run_proceedure('CALL admin_login(?,?,?)', 
            [request.json.get('username'), request.json.get('password'), token])

         if(type(results) == list):
            return make_response(jsonify(results), 200)
         else:
            return make_response(jsonify('something has gone wrong'), 500)


except TypeError:
   print('Invalid entry, try again')
   
except: 
   print('something went wrong')



try:
   @app.post('/api/image')
   #function gets called on api request
   def image_upload():
   
      is_valid = api_helper.check_endpoint_info(request.form, ['description'])
      
      if(is_valid != None):
         return make_response(jsonify(is_valid), 400)

      is_valid = api_helper.check_endpoint_info(request.files, ['uploaded_image'])
      if(is_valid != None):
         return make_response(jsonify(is_valid), 400)
      
      filename = api_helper.save_file(request.files['uploaded_image'])
      # If the filename is None something has gone wrong
      if(filename == None):
         return make_response(jsonify("Sorry, something has gone wrong"), 500)
      
      
      results = dbhelper.run_proceedure('CALL image_create(?,?)', [filename, request.form['description']])

      if(type(results) == list):
         return make_response(jsonify('Success'), 200)
      else:
         return make_response(jsonify(str(results)), 500)
         
   
except TypeError:
   print('Invalid entry, try again')
   
except: 
   print('something went wrong')


try:
   @app.get('/api/get-image')
   def get_image():

      # Make sure the image_id is sent
      is_valid = api_helper.check_endpoint_info(request.args, ['image_id'])
      if(is_valid != None):
         return make_response(jsonify(is_valid), 400)
                  
      # Get the image information from the DB
      results = dbhelper.run_proceedure('CALL get_specific_image(?)', [request.args.get('image_id')])
      # Make sure something came back from the DB that wasn't an error
      if(type(results) != list):
         return make_response(jsonify(str(results)), 500)
      elif(len(results) == 0):
         return make_response(jsonify("Invalid image id"), 400)

            
      return send_from_directory('/home/cameron/Documents/images', results[0]['file_name'])

except TypeError:
   print('Invalid entry, try again')
   
except: 
   print('something went wrong')
   
   
try:
   @app.get('/api/images')
   def get_images():

   
                  
      # Get the image information from the DB
      results = dbhelper.run_proceedure('CALL get_all()', [])
      # Make sure something came back from the DB that wasn't an error
      if(type(results) != list):
         return make_response(jsonify(str(results)), 500)
      elif(len(results) == 0):
         return make_response(jsonify("Invalid image id"), 400)

            

      # Use the built in flask function send_from_directory
      # First into the images folder, and then use my results from my DB interaction to get the name of the file
      
      
      
      return send_from_directory('/home/cameron/Documents/images', results[0]['file_name'])

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
