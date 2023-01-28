from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField, URLField
from wtforms.validators import DataRequired
import csv
from csv import DictWriter


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------

class CafeForm(FlaskForm):
    # Choices for coffe, wifi, power_outlet
    coffe_emoji_choices = ['✘ ' if i == 0 else "☕️ " * i for i in range(0, 5)]
    wifi_emoji_choices = ['✘ ' if i == 0 else "💪 " * i for i in range(0, 5)]
    power_outlet_emoji_choices = ['✘ ' if i == 0 else "🔌 " * i for i in range(0, 5)]

    # Form Items
    caffe_name = StringField(label="Caffe Name", validators=[DataRequired()])
    location_url = URLField(label="Location URL", validators=[DataRequired()])
    open_time = StringField(label='Open Time', validators=[DataRequired()])
    closing_time = StringField(label='Closing Time', validators=[DataRequired()])
    coffe_rating = SelectField(label="Coffe Rating", validators=[DataRequired()], choices=coffe_emoji_choices)
    wifi_rating = SelectField(label="Wifi Rating", validators=[DataRequired()], choices=wifi_emoji_choices)
    power_outlet_rating = SelectField(label="Power Outlet Rating", validators=[DataRequired()], choices=power_outlet_emoji_choices)
    submit = SubmitField(label='Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print(form.data)
        with open("cafe-data.csv", 'a+') as csv_file:
            csv_file.write(f"\n{form.caffe_name.data},"
                           f"{form.location_url.data},"
                           f"{form.open_time.data},"
                           f"{form.closing_time.data},"
                           f"{form.coffe_rating.data},"
                           f"{form.wifi_rating.data},"
                           f"{form.power_outlet_rating.data}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
