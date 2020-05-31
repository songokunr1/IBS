from datetime import date

from flask import render_template, url_for, flash, redirect, jsonify,request
from flask_restful import Api

from app import app
from app import db
from app.forms import DateActivityReport, ChooseDate
# from app.forms import New_category, New_habit, Building_habit, Delete_habit, DateHabitReport
from app.models import Category, Activity, Date
from app.resources import CategoryResource

# todo change model to done/not done, category name in date

category_init = [
    {
        'category': 'objawy',
    },
    {
        'category': 'leki',
    },
    {
        'category': 'stres',
    },
    {
        'category': 'uzywki',
    },
    {
        'category': 'gluten',
    },
    {
        'category': 'bezglutenowe',
    },
    {
        'category': 'laktoza',
    },
    {
        'category': 'białka mleka',
    },
    {
        'category': 'wysoko białkowe',
    },
    {
        'category': 'wysoko weglowodanowe',
    },
    {
        'category': 'cukier',
    },
    {
        'category': 'inne',
    },
    {
        'category': 'warzywa',
    },
    {
        'category': 'owoce',
    }
]

activity_init = [
    {
        'name': 'Bol zoladka',
        'category_name': 'objawy'
    },
    {
        'name': 'Bol jelit',
        'category_name': 'objawy'
    },
    {
        'name': 'Zgaga',
        'category_name': 'objawy'
    },
    {
        'name': 'Wzdecia',
        'category_name': 'objawy'
    },
    {
        'name': 'Rozwolnienie',
        'category_name': 'objawy'
    },
    {
        'name': 'Zaparcia',
        'category_name': 'objawy'
    },
    {
        'name': 'Odbijanie',
        'category_name': 'objawy'
    },
    {
        'name': 'stres',
        'category_name': 'stres'
    },
    {
        'name': 'Working day?',
        'category_name': 'stres'
    },
    {
        'name': 'sport 20 min',
        'category_name': 'stres'
    },
    {
        'name': 'Okres',
        'category_name': 'stres'
    },
    {
        'name': 'Tribux',
        'category_name': 'leki'
    },
    {
        'name': 'Węgiel aktywny',
        'category_name': 'leki'
    },
    {
        'name': 'Nifuroksazyd',
        'category_name': 'leki'
    },
    {
        'name': 'Kawa',
        'category_name': 'uzywki'
    },
    {
        'name': 'Alkohol',
        'category_name': 'uzywki'
    },
    {
        'name': 'Papierosy',
        'category_name': 'uzywki'
    },
    {
        'name': 'Alkohol',
        'category_name': 'uzywki'
    },
    {
        'name': 'jedzenie na miescie',
        'category_name': 'uzywki'
    },
    {
        'name': 'fastfood',
        'category_name': 'uzywki'
    },
    {
        'name': 'Jenczmien',
        'category_name': 'gluten'
    },
    {
        'name': 'Żyto',
        'category_name': 'gluten'
    },
    {
        'name': 'pszenica',
        'category_name': 'gluten'
    },
    {
        'name': 'Makaron glutenowy',
        'category_name': 'gluten'
    },
    {
        'name': 'Makaron bez glutenowy',
        'category_name': 'bezglutenowe'
    },
    {
        'name': 'Owies',
        'category_name': 'bezglutenowe'
    },
    {
        'name': 'Kukurudza',
        'category_name': 'bezglutenowe'
    },
    {
        'name': 'Ryż',
        'category_name': 'bezglutenowe'
    },
    {
        'name': 'Quino',
        'category_name': 'bezglutenowe'
    },
    {
        'name': 'Gryka',
        'category_name': 'bezglutenowe'
    },
    {
        'name': 'Jaglana',
        'category_name': 'bezglutenowe'
    },
    {
        'name': 'Ser biały',
        'category_name': 'laktoza'
    },
    {
        'name': 'Mleko',
        'category_name': 'laktoza'
    },
    {
        'name': 'smietana smietanka',
        'category_name': 'laktoza'
    },
    {
        'name': 'Jogut',
        'category_name': 'białka mleka'
    },
    {
        'name': 'Kefir',
        'category_name': 'białka mleka'
    },
    {
        'name': 'ser żółty',
        'category_name': 'białka mleka'
    }, {
        'name': 'Inne sery',
        'category_name': 'białka mleka'
    },
    {
        'name': 'Mięso drobiowe',
        'category_name': 'wysoko białkowe'
    },
    {
        'name': 'Mięso wieprzowe',
        'category_name': 'wysoko białkowe'
    },
    {
        'name': 'Mięso wołowe',
        'category_name': 'wysoko białkowe'
    },
    {
        'name': 'Ryba',
        'category_name': 'wysoko białkowe'
    },
    {
        'name': 'Ziemniaki',
        'category_name': 'wysoko weglowodanowe'
    },
    {
        'name': 'Słodycze',
        'category_name': 'cukier'
    },
    {
        'name': 'Czekolada +70',
        'category_name': 'cukier'
    },
    {
        'name': 'Miód',
        'category_name': 'cukier'
    },
    {
        'name': 'Dzem',
        'category_name': 'cukier'
    },
    {
        'name': 'Owoce',
        'category_name': 'cukier'
    },
    {
        'name': 'Lody',
        'category_name': 'cukier'
    },
    {
        'name': 'Owoce suszone',
        'category_name': 'cukier'
    },
    {
        'name': 'Drożdże',
        'category_name': 'inne'
    },
    {
        'name': 'Orzechy',
        'category_name': 'inne'
    },
    {
        'name': 'Kakao',
        'category_name': 'inne'
    },
    {
        'name': 'Zaparcia',
        'category_name': 'inne'
    },
    {
        'name': 'Strączkowe',
        'category_name': 'warzywa'
    },
    {
        'name': 'Kapustne',
        'category_name': 'warzywa'
    },
    {
        'name': 'Kalafior',
        'category_name': 'warzywa'
    },
    {
        'name': 'Zaparcia',
        'category_name': 'warzywa'
    },
    {
        'name': 'Brokuł',
        'category_name': 'warzywa'
    },
    {
        'name': 'Kapusta',
        'category_name': 'warzywa'
    },
    {
        'name': 'Jarmuz',
        'category_name': 'warzywa'
    },

]

todo = {
    "todos": [
        {
            "id": 0,
            "name": "Go to the gym"
        },
        {
            "id": 1,
            "name": "Walk the dog"
        },
        {
            "id": 2,
            "name": "Get some pizza"
        }
    ]
}

api = Api(app)

api.add_resource(CategoryResource, '/category1/<string:name>')


@app.route("/home")
@app.route("/")
def about():
    return render_template('home.html', title='About')


@app.route("/cat")
def init_category():
    for category in category_init:
        print(Category.find_by_category(category['category']))
        if Category.find_by_category(category['category']) == None:
            new_record = Category(category=category['category'])
            Category.save_to_db(new_record)
    return render_template('habit.html')


@app.route("/act")
def init_activity():
    for each_record in activity_init:
        print(Activity.find_by_name(each_record['name']))
        if Activity.find_by_name(each_record['name']) == None:
            category_id_for_new_record = (Category.find_by_category(each_record['category_name']).id)
            new_record = Activity(name=each_record['name'], category_id=category_id_for_new_record)
            Activity.save_to_db(new_record)
    return render_template('habit.html')


@app.route("/today")
def init_date_today():
    print(type(date.today()))
    for single_object in Activity.list_of_activity_objects():
        #TODO if not working with empty databasee
        try:
            Date.find_date_by_activity_id_and_date(_id=single_object.id, date=str(date.today()))[0]
        except IndexError as e:
            new_record = Date(date=date.today(), done=False, activity_id=single_object.id,
                              category_id=single_object.category_id)
            Date.save_to_db(new_record)
            flash('Your update has been created!', 'success')
    return render_template('habit.html')


# @app.route("/report", methods=['POST', 'GET', 'DELETE'])
# def report():
#     form_done = DateActivityReport()
#     choosen_date = date.today()
#     all_category = Category.query.all()
#     if form_done.validate_on_submit():
#         choosen_date = Date.find_date_by_date_id_and_date(_id=form_done.date_id.data, date='2020-05-29')
#         choosen_date.done = True
#         db.session.commit()
#         flash('Your update has been created!', 'success')
#         return redirect(url_for('report', form_done=form_done, all_category=all_category))
#     return render_template('report.html',
#                            form_done=form_done, date_object=Date, all_category=all_category, Date=Date,
#                            Activity=Activity, Category=Category, choosen_date=choosen_date)

@app.route("/report/<choosen_date>", methods=['POST', 'GET', 'DELETE'])
def report3(choosen_date):
    form_done = DateActivityReport()
    all_category = Category.query.all()
    for single_object in Activity.list_of_activity_objects():
        try:
            Date.find_date_by_activity_id_and_date(_id=single_object.id, date=str(date.today()))[0]
        except IndexError as e:
            new_record = Date(date=date.today(), done=False, activity_id=single_object.id,
                              category_id=single_object.category_id)
            Date.save_to_db(new_record)
            flash('Your update has been created!', 'success')
    for single_category in all_category:
        print(single_category.category)
        date_object = Date.find_date_by_category_id_and_date(single_category.id, choosen_date)
        for single in date_object:
            print(single.activity.name)
    if form_done.validate_on_submit():
        today = Date.find_date_by_date_id_and_date(_id=form_done.date_id.data, date=choosen_date)
        today.done = True
        db.session.commit()
        flash('Your update has been created!', 'success')
        return redirect(url_for('report', form_done=form_done, date_object=date_object, all_category=all_category, choosen_date=choosen_date))
    return render_template('report.html',
                           form_done=form_done, date_object=date_object, all_category=all_category, Date=Date,
                           Activity=Activity, Category=Category, choosen_date=choosen_date)

@app.route("/reportvue/<choosen_date>", methods=['POST', 'GET', 'DELETE'])
def report4(choosen_date):
    form_done = DateActivityReport()
    all_category = Category.query.all()
    for single_object in Activity.list_of_activity_objects():
        try:
            Date.find_date_by_activity_id_and_date(_id=single_object.id, date=str(date.today()))[0]
        except IndexError as e:
            new_record = Date(date=date.today(), done=False, activity_id=single_object.id,
                              category_id=single_object.category_id)
            Date.save_to_db(new_record)
            flash('Your update has been created!', 'success')
    for single_category in all_category:
        print(single_category.category)
        date_object = Date.find_date_by_category_id_and_date(single_category.id, choosen_date)
        for single in date_object:
            print(single.activity.name)
    if form_done.validate_on_submit():
        today = Date.find_date_by_date_id_and_date(_id=form_done.date_id.data, date=choosen_date)
        today.done = True
        db.session.commit()
        flash('Your update has been created!', 'success')
        return redirect(url_for('report', form_done=form_done, date_object=date_object, all_category=all_category, choosen_date=choosen_date))
    return render_template('report2.html',
                           form_done=form_done, date_object=date_object, all_category=all_category, Date=Date,
                           Activity=Activity, Category=Category, choosen_date=choosen_date)

@app.route("/report", methods=['POST', 'GET', 'DELETE'])
def report():
    today = str(date.today())
    form_choose_date = ChooseDate()
    if form_choose_date.validate_on_submit():
        date_to_show = form_choose_date.date_report.data
        return redirect(url_for('report3', choosen_date=date_to_show))
    return render_template('report_base.html',
                           form_choose_date=form_choose_date, today=today)


@app.route("/reportvuefinal/<choosen_date>", methods=['POST', 'GET', 'DELETE'])
def reportvue(choosen_date):
    form_done = DateActivityReport()
    all_category = Category.query.all()
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        print(post_data)
    for single_object in Activity.list_of_activity_objects():
        try:
            Date.find_date_by_activity_id_and_date(_id=single_object.id, date=str(date.today()))[0]
        except IndexError as e:
            new_record = Date(date=date.today(), done=False, activity_id=single_object.id,
                              category_id=single_object.category_id)
            Date.save_to_db(new_record)
            flash('Your update has been created!', 'success')
    for single_category in all_category:
        print(single_category.category)
        date_object = Date.find_date_by_category_id_and_date(single_category.id, choosen_date)
        for single in date_object:
            print(single.activity.name)
    if form_done.validate_on_submit():
        today = Date.find_date_by_date_id_and_date(_id=form_done.date_id.data, date=choosen_date)
        today.done = True
        db.session.commit()
        flash('Your update has been created!', 'success')
        return redirect(url_for('report', form_done=form_done, date_object=date_object, all_category=all_category, choosen_date=choosen_date))
    return render_template('reportvue.html',
                           form_done=form_done, date_object=date_object, all_category=all_category, Date=Date,
                           Activity=Activity, Category=Category, choosen_date=choosen_date)

@app.route("/todos", methods=['GET'])
def jsonserver():
    todos = [
        {
            "id": 0,
            "name": "Go to the gym"
        },
        {
            "id": 1,
            "name": "Walk the dog"
        },
        {
            "id": 2,
            "name": "Get some pizza"
        }
    ]
    return jsonify(todos
    )


@app.route("/records", methods=['GET'])
def jsonactivities():
    return jsonify({
        'status': 'success',
        'act': activity_init
    })

@app.route("/records_get", methods=['GET', 'POST'])
def jsongetactivities():
    print(request.get_json())
