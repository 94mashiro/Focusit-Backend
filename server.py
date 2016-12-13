from flask import Flask
from mongoengine import *
import classes
import json
import pprint

app = Flask(__name__)

connect('Articles', host='127.0.0.1', port=27017)


# Handle Error
@app.errorhandler(404)
def page_not_found(error):
    message = {
        'status': 404,
        'message': 'Page Not Found'
    }
    return json.dumps(message)

@app.errorhandler(500)
def internal_server_error(error):
    message = {
        'status': 500,
        'message': 'Internal Server Error'
    }
    return json.dumps(message)

# Router
@app.route('/topics/newest/')
def newest():
    return classes.Article.objects.order_by('-id').limit(10).to_json()

@app.route('/topics/newest/limit/<int:limit>/')
def newestWithArg(limit):
    return classes.Article.objects.order_by('-id').limit(limit).to_json()

@app.route('/topics/find/tag/<tagname>/')
def findTag(tagname):
    return classes.Article.objects(tag__contains=tagname).to_json()

@app.route('/topics/find/origin/<originname>/')
def findOrigin(originname):
    return classes.Article.objects(origin__contains=originname).to_json()

if __name__ == '__main__':
    app.run()
