from flask import Flask, request, make_response, jsonify
import dbhelper,api_helper,dbcreds, uuid

app = Flask(__name__)

try:

#on post, checks data and inserts data into the DB 

   @app.post('/api/contact')
   def send_contact():
      
      #checking send data
         error=api_helper.check_endpoint_info(request.json, ['name', 'email', 'content']) 
         if(error !=None):
            return make_response(jsonify(error), 400)


            #connecting to DB and calling the procedure that inputs the data sent

         results = dbhelper.run_proceedure('CALL content_send(?,?,?)', 
            [request.json.get('name'),request.json.get('email'),request.json.get('content')])

            #returning the results

         if(type(results) == list):
            return make_response(jsonify(results), 200)
         else:
            return make_response(jsonify('something has gone wrong'), 500)


except TypeError:
   print('Invalid entry, try again')
   
except: 
   print('something went wrong')



try:
   @app.post('/api/admin')
   
   def create_admin():
      #checking send data
      
         error=api_helper.check_endpoint_info(request.json, ['username', 'password']) 
         if(error !=None):
            return make_response(jsonify(error), 400)
            
            #connecting to DB and calling the procedure that inputs the data sent

         results = dbhelper.run_proceedure('CALL create_admin(?,?)', 
               [request.json.get('username'), request.json.get('password')])
         
            #returning the results
         
      
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
      
      #checking send data
      
         error=api_helper.check_endpoint_info(request.json, ['username','password']) 
         if(error !=None):
            return make_response(jsonify(error), 400)
         
            #connecting to DB and calling the procedure that inputs the data sent
         
            #also generates a random token that is used in the procedure

         token = uuid.uuid4().hex
         results = dbhelper.run_proceedure('CALL admin_login(?,?,?)', 
            [request.json.get('username'), request.json.get('password'), token])

            #returning the results


         if(type(results) == list):
            return make_response(jsonify(results), 200)
         else:
            return make_response(jsonify('something has gone wrong'), 500)


except TypeError:
   print('Invalid entry, try again')
   
except: 
   print('something went wrong')



try:
   @app.post('/api/image_upload')

   def image_upload():
      
      #checking send data
      
   
      is_valid = api_helper.check_endpoint_info(request.form, ['description', 'type', 'token'])
      
      if(is_valid != None):
         return make_response(jsonify(is_valid), 400)

      is_valid = api_helper.check_endpoint_info(request.files, ['uploaded_image'])
      if(is_valid != None):
         return make_response(jsonify(is_valid), 400)
      
      
      
      
      results = []

      #iterates over each file, calls the fucntion to save it, then inserts the filename and other data into the DB.

      for file in request.files.getlist('uploaded_image'):
         filename = api_helper.save_file(file)
         if filename is None:
               return make_response(jsonify("Sorry, something has gone wrong"), 500)
         
         result = dbhelper.run_proceedure('CALL image_create(?,?,?,?)', [filename, request.form['description'], request.form['type'], request.form['token']])
         
         #if the task is sucessful, appends a success message to the empty results list and then returns the results
         
         if (type(results)==list):
               results.append('Success')
         else:
               results.append(str(result))
      
      return make_response(jsonify(results), 200)
         
   
except TypeError:
   print('Invalid entry, try again')
   
except: 
   print('something went wrong')


  
try:
   @app.get('/api/images')
   def get_images():
      #checking sent data
      is_valid = api_helper.check_endpoint_info(request.args, ['type'])
      if(is_valid != None):
         return make_response(jsonify(is_valid), 400)

      results = dbhelper.run_proceedure('CALL get_all(?)', [request.args.get('type')])
      # Make sure something came back from the DB that wasn't an error
      if(type(results) != list):
         return make_response(jsonify(str(results)), 500)
      elif(len(results) == 0):
         return make_response(jsonify("Invalid image id"), 400)

            
      
      images = []

      # Iterates over each result and create an image object
      for result in results:
         
         image = {
            
            'file_name': result['file_name'],
            'file_path': '/images/' + result['file_name'],
            'created_at': result['created_at'],
            'type':  result['type']
         }

         #pushes the created object into the images list

         images.append(image)
    
    #returns the results
      return make_response(jsonify(images), 200)

except TypeError:
   print('Invalid entry, try again')
   
except: 
   print('something went wrong')   
if(dbcreds.production_mode == True):
   print()
   print('----Running in Production Mode----')
   print()
   import bjoern #type: ignore
   bjoern.run(app,'0.0.0.0', 5450)
else:
   from flask_cors import CORS
   CORS(app)
   print()
   print('----Running in Testing Mode----')
   print()
   app.run(debug=True)
