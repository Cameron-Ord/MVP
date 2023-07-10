import os
from uuid import uuid4

def check_endpoint_info(sent_data, expected_data):
    try:    
        for data in expected_data:
            if(sent_data.get(data) == None):
                return f'the {data} must be sent!'
    except TypeError:
        print('Invalid entry. (how could this happen?)')
    except:
        print('Something went wrong with endpoint info check.')


def save_file(file):

    file_path = '/home/cameron/Documents/Photostream/mvp_frontend/public/images'
    
    if('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in ['gif', 'png', 'jpg', 'jpeg', 'webp', 'pdf']):
        filename = uuid4().hex + '.' +file.filename.rsplit('.', 1)[1].lower()
        try:
            file.save(os.path.join(file_path, filename))
            
            return filename
        except Exception as error:
            print('file save error: ', error)