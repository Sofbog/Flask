from flask import Flask, render_template, request, redirect
import csv


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


@app.route('/submit_form', methods=['POST', 'GET'])
def Submit_form():
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
       subject = data ['subject']
       message = data['message']
       csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
       csv_writer.writerow([email, subject, message])

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=80, DEBUG=True)