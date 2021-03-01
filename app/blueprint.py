from flask import Blueprint, render_template

blueprint = Blueprint("blueprint", __name__,
                      static_folder="static",
                      template_folder="templates")


@blueprint.route("/")
def home():
    print('blueprint')
    return render_template("habit.html")