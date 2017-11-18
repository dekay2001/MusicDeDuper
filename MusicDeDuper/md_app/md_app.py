from flask import Flask
from md_blueprint import simple_page

app = Flask(__name__)
app.register_blueprint(simple_page, url_prefix='/mdd')

@app.route('/')
def welcome():
	return "Hello, welcome to the Music DeDuper!"

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=12419, debug=True, threaded=True)