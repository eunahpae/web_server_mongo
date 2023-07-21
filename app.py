from flask import Flask, render_template, request
from data import Articles
from models import MyMongo

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    data = Articles()
    return render_template('index.html', data = data)




if __name__ == '__main__':
    app.run(debug=True, port=9999)
