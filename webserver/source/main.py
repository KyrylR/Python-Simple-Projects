import csv
import os

from flask import Flask, render_template, send_from_directory, request, redirect

app = Flask(__name__)


@app.route("/")
def root_page():
    return render_template('index.html')


@app.route("/<string:page_name>")
def home_page(page_name):
    return render_template(f'{page_name}')


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('/thankyou.html')
    return 'Error!'


def write_to_file(data: dict):
    with open('database.txt', mode='a') as database:
        name = data['name']
        subject = data['subject']
        email = data['email']
        message = data['message']
        file = database.write(f'\n{name},{email},{subject},{message}')


def write_to_csv(data: dict):
    with open('database.csv', mode='a', newline='') as database:
        name = data['name']
        subject = data['subject']
        email = data['email']
        message = data['message']
        csv_writer = csv.writer(database, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name, email, subject, message])


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/icon.png', mimetype='image/vnd.microsoft.icon')
