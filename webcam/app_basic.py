#!/usr/bin/python3

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)
PICTURE_DIRECTORY = '/home/anton/Desktop'
@app.route('/')
def index():
    return send_from_directory(PICTURE_DIRECTORY , 'test.jpg')

@app.route('/test')
def test():
    return render_template('test.html', picture_files=['test.jpg'])

@app.route('/pictures/<filename>')
def render_picture(filename):
    return send_from_directory(PICTURE_DIRECTORY , filename)

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode
