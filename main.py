from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from key_file import getsecretkey, getemail_key
from datetime import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = getsecretkey()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "gbpyapps@gmail.com"
app.config["MAIL_PASSWORD"] = getemail_key()

db = SQLAlchemy(app)

mail = Mail(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        form = Form(first_name=first_name, last_name=last_name, email=email,
                    date=date_obj, occupation=occupation)
        db.session.add(form)
        db.session.commit()

        message_body = f"Dear {first_name} \n" \
                       f"Thanks you for your submission \n" \
                       f"Here is the information you submitted: \n{first_name}\n{last_name}\n{date}" \
                       f"Best Regards"

        message = Message(subject="New form has been submitted",
                          sender=app.config["MAIL_USERNAME"],
                          recipients=[email],
                          body=message_body)

        flash(f"Thanks {first_name}, Your form was submitted successfully!", "success")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
