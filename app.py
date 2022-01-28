from flask import Flask, render_template, request, redirect
import csv
from flask.wrappers import Response
import git


app = Flask(__name__)

@app.route('/git_update', methods=['POST'])
def git_update():
  repo = git.Repo('./Sofbog.github.io.')
  origin = repo.remotes.origin
  repo.create_head('main',
  origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
  origin.pull()
  return '', 200


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            write_data_to_file(data)
            write_data_to_csv(data)
            return redirect('/thanks.html')
        except:
            return 'did not save to data base'
    else:
        return 'something went wront. Try again!!!'


def write_data_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\n{email},{subject},{message}')


def write_data_to_csv(data):
    with open('database.csv', 'a', newline='') as database2:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])
