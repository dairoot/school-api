from flask import Flask
from school_api import SchoolClient
from flask import jsonify


app = Flask(__name__)
GdstApi = SchoolClient('http://61.142.33.204')


@app.route('/')
def get_schedule():
    student = GdstApi.user_login('user', 'password', timeout=2)
    schedule = student.get_schedule()
    return jsonify(schedule)


if __name__ == '__main__':
    app.run()
