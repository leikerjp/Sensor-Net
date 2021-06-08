# sqalchemy notes:
# sensorList = Sensor.query.all()       : gets list of all sensors in database
# sensorFirst = Sensor.query.first()    : gets first item from list
# sensorFilter = Sensor.query.filter_by(id=<integer>).first() : get the sensor with id equal to <integer>
# sensor.measurements       : list of measurements with relationship to sensor
# NOTE: primary_keys are autogenerated unless provided (which there needs to be a guarantee they are unique if provided)

from flask import render_template, request, jsonify, make_response, Markup, url_for
from server import app, db
from server.models import Sensor, Measurement
import logging
import datetime
from plotly.offline import plot
from plotly.graph_objs import Scatter


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', datetime=datetime.datetime.now().strftime('%m/%d/%Y at %I:%M:%S %p'))


@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/sensors")
def sensors():
    # Get all sensors (which are unique by id)
    sensors = Sensor.query.all()
    return render_template('sensors.html', sensors=sensors)

# @app.route("/measurements/<id>")
# def measurements(id):
#     # Get all sensors (which are unique by id)
#     sensors = Sensor.query.all()
#     ids = [sensor.id for sensor in sensors]
#
#     if int(id) in ids:
#         return render_template('measurement.html', name=id)
#     else:
#         logging.error(f"[ERROR] Tried accessing measurements/<id> of non-existent id: {id}")
#         return '', 404

@app.route("/measurements/<id>")
def measurements(id):
    # Get sensor by ID (which we will use to get all measurments for that sensor)
    sensor = Sensor.query.filter_by(id=id).first()

    # Create Figure
    values = [measurement.value for measurement in sensor.measurements]
    times = [measurement.date_taken for measurement in sensor.measurements]
    fig = plot([Scatter(x=times, y=values)], output_type='div')

    return render_template('measurement.html', name=id, graph=Markup(fig))



@app.route("/record_data", methods=['POST'])
def record_data():
    if request.method == 'POST':
        data = request.json
        resp = make_response('', 200)

        # Create sensor if it does not already exist
        sensor = Sensor.query.filter_by(id=data['ctrlr_id']).first()
        if not sensor:
            # New sensor, create entry for sensor and then save measurement
            sensor = Sensor(type=data['ctrlr_type'])
            db.session.add(sensor)
            db.session.commit()
            logging.info(f"New Sensor : {sensor.id}")

            respDict = dict()
            respDict['ctrlr_id'] = sensor.id
            respDict['ctrlr_name'] = f"{data['ctrlr_type']}-{sensor.id}" # TBD
            resp = make_response(respDict, 200)


        # Log measurement
        # NOTE: can use sensor_controller=sensor OR sensor_id=int(data['ctrlr_id'])
        measurement = Measurement(type=str(data['type']), value=float(data['value']), sensor_controller=sensor)
        db.session.add(measurement)
        db.session.commit()

        return resp
    else:
        logging.warning("[WARNING] GET request to /log")
        return '', 404  # no-one should've been able to get here! Return error


@app.route("/graph_data")
def graph_data():
    # Get all sensors (which are unique by id)
    sensors = Sensor.query.all()
    for sensor in sensors:
        measurements = Sensor.query.filter_by(id=sensor.id).first()

    fig = plot([Scatter(x=[0,1,2,3,4,5],y=[1,2,3,1,2,3])], output_type='div')
    return render_template('graph.html', graph_div=Markup(fig))



# @app.route("/log_data", methods=['POST'])
# def log_data():
#     if request.method == 'POST':
#         data = request.json
#         print(data)
#         sensor = Sensor.query.filter_by(id=data['ctrlr_id']).first()
#         if sensor == None:
#             # New sensor, create entry for sensor and then save measurement
#             print(f"New Sensor - Adding sensor \"{data['ctrlr_id']}\" now")
#             sensor = Sensor(type="TBD-parse-id")
#             db.session.add(sensor)
#             db.session.commit()
#         else:
#             print(sensor)
#
#         print(f"Logging measurement \"{data['data_id']}\" to sensor \"{data['ctrlr_id']}\"")
#         # Save measurement
#         measurement = Measurement(type=str(data['type']),
#                                   value=float(data['value']),
#                                   sensor_controller=sensor) # ALSO WORKS: sensor_id=int(data['ctrlr_id'])
#
#         db.session.add(measurement)
#         db.session.commit()
#
#         resp = make_response("cat",200)
#         idNumIs = 23
#         resp = f'id#{idNumIs}'
#         return resp,200
#         #return r'kitten',200
#         #return resp
#         #return r'', 200 # respond good - HTML unnecessary
#     else:
#         return '', 404 # no-one should've been able to get here! Return error


@app.route("/print_data", methods=['POST'])
def print_data():
    if request.method == 'POST':
        data = request.json
        # Query returns list, so use .first() to get just first item (list should only be one long sense
        # we are sorting by ctrl_id's anyways).
        sensor = Sensor.query.filter_by(id=data['ctrlr_id']).first()
        print(sensor.measurements)
        # for measurement in sensor.measurements:
        #     print(measurement.value)

        return r'', 200 # respond good - HTML unnecessary
    else:
        return '', 404 # no-one should've been able to get here! Return error

# @app.route("/send_sensor_data", methods=['POST'])
# def send_sensor_data():
#     if request.method == 'POST':
#         data = request.form.to_dict(flat=False)
#         timeString = data['time']
#         print(data)
#         return r'', 200 # respond good - HTML unnecessary
#     else:
#         return '', 404 # no-one should've been able to get here! Return error