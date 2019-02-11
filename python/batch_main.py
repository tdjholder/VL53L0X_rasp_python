import csv
import smtplib
import io
import pytz
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import datetime
from email.utils import COMMASPACE
from email import encoders

from sqlalchemy import and_, desc, func

from models.models import Measurement, Sensor
from storage.base import get_session


def run(idx1, idx2, cob_date):
    """Get the previous day's readings, convert to pdf and send."""

    readings = get_readings_by_date(idx1, idx2, cob_date=cob_date)
    csv_file = build_csv(readings)
    send_email(csv_file, cob_date)


def send_email(csv_file, cob_date):
    subject = "Pi readings for date: %s" % cob_date
    filename = "%s-readings.csv" % cob_date
    from_email = os.environ['FLOWRIGHT_FROM_EMAIL']
    password = os.environ['FLOWRIGHT_EMAIL_PASSWORD']
    to_email = os.environ['FLOWRIGHT_TO_EMAIL']
    smtp_server = 'smtp.gmail.com'
    smpt_port = 587
    to_list = to_email.split(',')
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = COMMASPACE.join(to_list)
    msg['Subject'] = subject

    part = MIMEBase('application', "octet-stream")
    part.set_payload(csv_file.getvalue())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % filename)
    msg.attach(part)

    smtpObj = smtplib.SMTP(smtp_server, smpt_port)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(from_email, password)
    smtpObj.sendmail(from_email, to_list, msg.as_string())
    smtpObj.quit()


def build_csv(readings):
    csv_file = io.StringIO()
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Sensor Id', 'Distance (mm)', 'Time'])
    for reading in readings:
        csv_writer.writerow([reading.sensor_id, reading.distance, reading.created_date])
    return csv_file


def get_readings_by_date(*ids, cob_date):
    session = get_session()
    return session.query(Measurement).filter(
        and_(
            Measurement.sensor_id.in_(ids),
            func.date(Measurement.created_date) == cob_date)
        ).order_by(desc(Measurement.created_date)).all()


if __name__ == "__main__":
    session = get_session()
    id1, id2 = [sensor.id for sensor in session.query(Sensor).all()]
    u = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).date()

    run(id1, id2, u)
