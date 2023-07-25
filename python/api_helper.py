import os
from uuid import uuid4

#function for checking sent data

def check_endpoint_info(sent_data, expected_data):
    try:    
        for data in expected_data:
            if(sent_data.get(data) == None):
                return f'the {data} must be sent!'
    except TypeError:
        print('Invalid entry. (how could this happen?)')
    except:
        print('Something went wrong with endpoint info check.')

#function for saving image files

def save_file(file):

        #setting the file path

    file_path = '/home/cameron/Documents/Photostream/mvp_frontend/public/images'
    
    #if the . in the filename is followed by any of image file extensions, generates a random name and replaces it
    
    if('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ['gif', 'png', 'jpg', 'jpeg', 'webp', 'pdf']):
        filename = uuid4().hex + '.' +file.filename.rsplit('.', 1)[1].lower()
        try:
            
            #saves the file based on the given variables
            
            file.save(os.path.join(file_path, filename))
            
            return filename
        except Exception as error:
            print('file save error: ', error)