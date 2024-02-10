from flask import Flask, send_from_directory
import datetime
 
x = datetime.datetime.now()
 
# Initializing flask app
app = Flask(__name__, static_folder="frontend/build")
 
 # Serve React App
@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

# Route for seeing a data
@app.route('/api/data')
def get_time():
    # Returning an api for showing in  reactjs
    return {
        'Name':"geek", 
        "Age":"22",
        "Date":x, 
        "programming":"python"
        }
 
     
# Running app
if __name__ == '__main__':
    app.run(debug=True)