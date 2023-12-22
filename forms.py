from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize


from wtforms.fields import StringField, IntegerField, SubmitField, TextAreaField, PasswordField, RadioField, DateField, EmailField, FloatField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired, Length, equal_to, NumberRange



class AddMovieForm(FlaskForm):
    title = StringField("ფილმის დასახელება", validators=[DataRequired(message="სახელი სავალდებულოა"), Length(max=32, message="ფილის სახელის მაქსიმალური ზომაა 32ასო")])
    desc = TextAreaField("ფილმის აღწერა", validators=[DataRequired(message="აღწერა აუცილებელია"), Length(max=512, message="ფილის აღწერის მაქსიმალური ზომაა 512ასო")])
    imbd = FloatField("IMDB შეფასება", validators=[
        DataRequired(),
        NumberRange(min=0.1, max=10.0, message=("Rating should be between 0.1 and 10.0"))
    ])
    imgv = FileField("ვერდიკალური სურათი",
                     validators=[
                         FileRequired(message="ვერდიკალური სურათი აუცილებელია"),
                         FileAllowed(["jpg", "png", "jpeg", ], message="დაშვებულია მხოლოდ jpg png da jpeg ფაილები"),
                         FileSize(max_size=1024 * 1024 * 5, message="ფაილის მაქსიმალური ზომაა 25mb"),
                     ])

    imgh = FileField("ჰორიზონტალური სურათი",
                     validators=[
                         FileRequired(message="ვერდიკალური სურათი აუცილებელია"),
                         FileAllowed(["jpg", "png", "jpeg"], message="დაშვებულია მხოლოდ jpg png da jpeg ფაილები"),
                         FileSize(max_size=1024 * 1024 * 5, message="ფაილის მაქსიმალური ზომაა 25mb")
                     ])

    genre = SelectMultipleField("ჟანრები", choices=[
        ('Action', "Action"),
        ('Adventure', "Adventure"),
        ('Animated', "Animated"),
        ('Comedy', "Comedy"),
        ('Drama', "Drama"),
        ('Horror', "Horror"),
        ('Sci-fi', "Sci-fi"),
        ('Western', "Western")
    ],validators=[
        DataRequired(message="ჟანრის მითითება აუცილებელია")
    ])
    category_id = RadioField("ტიპი", choices=[
        (1, "filmi"),
        (2, "seriali")
    ], validators=[DataRequired(message="კატეგორიის მინიჭება აუცილებელია")])
    submit = SubmitField("დამატება")


class EditMovieForm(FlaskForm):
    title = StringField("ფილმის დასახელება", validators=[
        Length(max=48)
    ])
    desc = TextAreaField("ფილმის აღწერა", validators=[
        Length(max=256)
    ])
    imbd = FloatField("IMDB შეფასება", validators=[
        NumberRange(min=0.1, max=10.0, message=("Rating should be between 0.1 and 10.0"))
    ])
    imgv = FileField("ვერდიკალური სურათი",
                     validators=[
                         FileAllowed(["jpg", "png", "jpeg", ], message="დაშვებულია მხოლოდ jpg png da jpeg ფაილები"),
                         FileSize(max_size=1024 * 1024 * 5, message="ფაილის მაქსიმალური ზომაა 25mb"),
                     ])

    imgh = FileField("ჰორიზონტალური სურათი",
                     validators=[
                         FileAllowed(["jpg", "png", "jpeg"], message="დაშვებულია მხოლოდ jpg png da jpeg ფაილები"),
                         FileSize(max_size=1024 * 1024 * 5, message="ფაილის მაქსიმალური ზომაა 25mb")
                     ])

    genre = SelectMultipleField("ჟანრები", choices=[
        ('Action', "Action"),
        ('Adventure', "Adventure"),
        ('Animated', "Animated"),
        ('Comedy', "Comedy"),
        ('Drama', "Drama"),
        ('Horror', "Horror"),
        ('Sci-fi', "Sci-fi"),
        ('Western', "Western")
    ], validators=[
        DataRequired(message="ჟანრის მითითება აუცილებელია")
    ])

    category_id = RadioField("ტიპი", choices=[
        (1, "filmi"),
        (2, "seriali")
    ])




    submit = SubmitField("დამატება")


class RegisterForm(FlaskForm):
    username = StringField("შეიყვანეთ იუზერნეიმი")
    email = EmailField("შეიყვანეთ მაილი")
    password = PasswordField("შეიყვანეთ პაროლი", validators=[
        Length(min=8, max=64)
    ])
    repeat_password = PasswordField(label="გაიმეორეთ პაროლი", validators=[
        equal_to("password", message="გთხოვთ სწორად გაიმეოროთ პაროლი"),
    ])
    gender = RadioField("მონიშნეთ სქესი", choices=["ქალი", "კაცი", "სხვა"])

    submit = SubmitField('რეგისტრაცია')



class LoginForm(FlaskForm):
    username = StringField("შეიყვანეთ იუზერნეიმი", validators=[DataRequired()])
    password = PasswordField("შეიყვანეთ პაროლი", validators=[
        Length(min=8, max=64),
        DataRequired()
    ])

    submit = SubmitField('ავტორიზაცია')

class CommentForm(FlaskForm):
    text = TextAreaField('დაწერე კომენტარი', validators=[DataRequired(), Length(max=256)])
    submit = SubmitField('დამატება')