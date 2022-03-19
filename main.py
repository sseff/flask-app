from flask import Flask, request
import re
import time
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///registration.db'

db = SQLAlchemy(app)


class Plate(db.Model):
    # create handler id column
    plate_text = db.Column(db.String(10), primary_key=True)

    # create handler name column
    time_stamp = db.Column(db.String(150), nullable=False)


@app.route('/plate', methods=["POST", "GET"])
def peter_parker():
    if request.method == "POST":
        try:
            json_input = request.get_json()
            pattern = "^[A-Z]{1,3}-[A-Z]{1,2}([1-9]{1}[0-9]{0,3}|[8]{0})$"
            candidate_plate = json_input['plate']
        except:
            data = {
                "value": 'request is malformed'
            }
            return data, 400
        if re.search(pattern, candidate_plate):
            time_stamp = str(time.time())
            data = {
                "plate": candidate_plate,
                "timestamp": time_stamp
            }
            current_plate = Plate(plate_text=candidate_plate, time_stamp=time_stamp)
            db.session.add(current_plate)
            db.session.commit()
            return data, 200
        else:
            data = {
                "value": "plate is not valid"
            }
            return data, 422
    if request.method == "GET":
        plates = Plate.query.all()
        data = []
        for i, plate in enumerate(plates):
            datum = {
                "plate": plate.plate_text,
                "timestamp": plate.time_stamp
            }
            data.append(datum)
        return json.dumps(data), 200


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0')

# FROM python:3
# WORKDIR ./purbee_backend/backend_source
# COPY . .
# RUN pip install --no-cache-dir -r requirements.txt
# EXPOSE 5000
# ENV FLASK_ENV=development
# ENV FLASK_APP=./backend_source/app.py
# #CMD ["flask", "run", "--host=0.0.0.0"]
# #CMD ["python", "./backend_source/app.py"]
# #ENTRYPOINT ["flask"]
#
# #CMD ["run", "--host=0.0.0.0"]
# CMD ["python", "./backend_source/app.py"]
