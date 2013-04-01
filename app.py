import os
from flask import Flask
from flask import request

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class WaterTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.String(64))
    test_id = db.Column(db.String(64))
    test_type = db.Column(db.String(64))
    test_time = db.Column(db.DateTime())
    test_result = db.Column(db.String(64))
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())

    def __init__(self, device_id, test_id, test_type, test_time, test_result, latitude, longitude):
        self.device_id = device_id
        self.test_id = test_id
        self.test_type = test_type
        self.test_result = test_result
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return "%r:%r" % (self.device_id, self.test_id)

@app.route('/post', methods=['POST'])
def post():
    device_id = ''
    test_id = ''
    test_type = ''
    test_time = ''
    test_result = ''
    latitude = ''
    longitude = ''
    try:
        device_id = request.form['device_id']
        test_id = request.form['test_id']
        test_type = request.form['test_type']
        test_time = request.form['test_time']
        test_result = request.form['test_result']
        latitude = request.form['latitude']
        longitude = request.form['longitude'] 
    except KeyError:
        pass
    
    try:
        wt = WaterTest(device_id, test_id, test_type, test_time, test_result, long(latitude), long(longitude))
        db.session.add(wt)
        db.session.commit()
    except Exception, e:
        return "error:%r" % str(e)

    return "success"

@app.route('/')
def tests():
    wtests = WaterTest.query.all()

    html = '''
    <!doctype html><html><head><title>Water Tests</title></head>
    <body>
    <table>
    <tr>
      <th>Device ID</th>
      <th>Test ID</th>
      <th>Test Type</th>
      <th>Test Time</th>
      <th>Result</th>
      <th>Location</th>
    </tr>
    '''
    for test in wtests:
        html += '<tr>'
        html += "<td>%s</td>" % test.device_id
        html += "<td>%s</td>" % test.test_id
        html += "<td>%s</td>" % test.test_type
        html += "<td>%s</td>" % test.test_time
        html += "<td>%s</td>" % test.test_result
        html += "<td>%.5f,%.5f</td>" % (test.latitude, test.longitude)
        html += '</tr>'

    html += "</table></body></html>"

    return html

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
