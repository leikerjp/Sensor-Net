'''Defines the models for our database
   Each sensor has a list of measurements (of varying types)'''

from datetime import datetime
from server import db


class Sensor(db.Model):
    # value is assigned automatically because it is primary_key
    id = db.Column(db.Integer, primary_key=True)

    type = db.Column(db.String(20), nullable=False)
    # this relationship will connect a measurement to the sensor
    measurements = db.relationship('Measurement', backref='sensor_controller', lazy=True)

    def __repr__(self):
        return f"Sensor(id='{self.id}', type='{self.type}')"


class Measurement(db.Model):
    # value is assigned automatically because it is primary_key
    id = db.Column(db.Integer, primary_key=True)
    date_taken = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # utcnow NOT utcnow() - function not time
    type = db.Column(db.String(25), nullable=False) # ex. temperature, humidity, atmospheric pressure
    value = db.Column(db.Float, nullable=False)
    # sensor_id is a column that links each measurement to the senor that took it (based on the sensors id)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)

    def __repr__(self):
        return f"Measurement(type='{self.type}', value='{self.value}', date_taken='{self.date_taken}')"