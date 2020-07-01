import json
from datetime import date

from flask import render_template, url_for, flash, redirect, jsonify, request
from flask_restful import Api

from app import app
from app import db
from app.forms import DateActivityReport, ChooseDate, FilterField, ChooseTypeAndDate, CreateMeal, UpdateCategory, \
    UpdateActivity, AddActivity, AddCategory
# from app.forms import New_category, New_habit, Building_habit, Delete_habit, DateHabitReport
from app.models import Category, Activity, Date, DateNew, Meal
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
    },

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
        'name': 'Pieczenie żołądka',
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
        'name': 'pomidor',
        'category_name': 'warzywa'
    },
    {
        'name': 'Jarmuz',
        'category_name': 'warzywa'
    },
    {
        'name': 'Toaleta plus 3',
        'category_name': 'objawy'
    },
    {
        'name': 'Szynka',
        'category_name': 'wysoko białkowe'
    },
    {
        'name': 'Salata',
        'category_name': 'warzywa'
    },
    {
        'name': 'Szpinak',
        'category_name': 'warzywa'
    },
    {
        'name': 'Siemiona',
        'category_name': 'inne'
    },
    {
        'name': 'Chia',
        'category_name': 'inne'
    },
    {
        'name': 'Bańki',
        'category_name': 'stres'
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
        # TODO if not working with empty databasee
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
            print(single_object.name)
            Date.find_date_by_activity_id_and_date(_id=single_object.id, date=choosen_date)[0]
        except IndexError as e:
            print(single_object.name, 'added')
            new_record = Date(date=choosen_date, done=False, activity_id=single_object.id,
                              category_id=single_object.category_id)
            Date.save_to_db(new_record)
            flash('Your update has been created!', 'success')
    for single_category in all_category:
        # print(single_category.category)
        date_object = Date.find_date_by_category_id_and_date(single_category.id, choosen_date)
        # for single in date_object:
        #     print(single.activity.name)
    if request.method == 'POST':
        post_data = request.form.getlist('mycheckbox')
        post_date = request.form.get('choosen_date')
        print(post_date, post_data)
        for id in post_data:
            print(post_date, 'post date czy okej?')
            today = Date.find_date_by_date_id_and_date(_id=int(id), date=post_date)
            today.done = True
            db.session.commit()
            print(id, today.id)
            flash('Your update has been created!', 'success')
        return redirect(url_for('report3', form_done=form_done, date_object=date_object, all_category=all_category,
                                choosen_date=choosen_date))
    if form_done.validate_on_submit():
        today = Date.find_date_by_date_id_and_date(_id=form_done.date_id.data, date=choosen_date)
        today.done = True
        db.session.commit()
        flash('Your update has been created!', 'success')
        return redirect(url_for('report', form_done=form_done, date_object=date_object, all_category=all_category,
                                choosen_date=choosen_date))
    return render_template('report.html',
                           form_done=form_done, date_object=date_object, all_category=all_category, Date=Date,
                           Activity=Activity, Category=Category, choosen_date=choosen_date)


@app.route("/report_new/<choosen_date>", methods=['POST', 'GET', 'DELETE'])
def report_new(choosen_date):
    form = ChooseMultiple()
    print(Activity.filer_activity_objects('eko'))
    if form.validate_on_submit():
        print(form.language.data)
    return render_template('report_new.html', form=form)


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
        return redirect(url_for('report', form_done=form_done, date_object=date_object, all_category=all_category,
                                choosen_date=choosen_date))
    return render_template('report2.html',
                           form_done=form_done, date_object=date_object, all_category=all_category, Date=Date,
                           Activity=Activity, Category=Category, choosen_date=choosen_date)


@app.route("/", methods=['POST', 'GET'])
def report():
    today = str(date.today())
    form_choose_date = ChooseDate()
    form_choose_type_and_date = ChooseTypeAndDate()
    print(form_choose_date.validate_on_submit)
    print(form_choose_type_and_date.submit_type_and_date)
    if form_choose_type_and_date.validate_on_submit():
        date_to_show = form_choose_type_and_date.date_report.data
        type_choice = form_choose_type_and_date.type_of_report.data
        return redirect(url_for('report_new_date', type=type_choice, chosen_date=date_to_show))
    if form_choose_date.validate_on_submit():
        date_to_show = form_choose_date.date_report.data
        return redirect(url_for('report3', choosen_date=date_to_show))
    return render_template('report_base.html',
                           form_choose_date=form_choose_date, today=today,
                           form_choose_type_and_date=form_choose_type_and_date)


@app.route("/reportvuefinal/<choosen_date>", methods=['POST', 'GET', 'DELETE'])
def reportvue(choosen_date):
    form_done = DateActivityReport()
    all_category = Category.query.all()
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
    for single_object in Activity.list_of_activity_objects():
        try:
            Date.find_date_by_activity_id_and_date(_id=single_object.id, date=str(date.today()))[0]
        except IndexError as e:
            new_record = Date(date=date.today(), done=False, activity_id=single_object.id,
                              category_id=single_object.category_id)
            Date.save_to_db(new_record)
            flash('Your update has been created!', 'success')
    for single_category in all_category:
        date_object = Date.find_date_by_category_id_and_date(single_category.id, choosen_date)
    if form_done.validate_on_submit():
        today = Date.find_date_by_date_id_and_date(_id=form_done.date_id.data, date=choosen_date)
        today.done = True
        db.session.commit()
        flash('Your update has been created!', 'success')
        return redirect(url_for('report', form_done=form_done, date_object=date_object, all_category=all_category,
                                choosen_date=choosen_date))
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
    return jsonify(todos)


@app.route("/todos2", methods=['GET'])
def jsonserver2():
    todos = [
        {
            "id": 3,
            "name": "todos2"
        },
        {
            "id": 4,
            "name": "todos2 ohh yea"
        },
        {
            "id": 5,
            "name": "todos2 ohh yea"
        }
    ]
    print(todos)
    return jsonify(todos)


@app.route("/todos3", methods=['POST'])
def jsonserver3():
    post_data = request.args.get('name')
    print(post_data)
    return jsonify(post_data)


@app.route("/todos4", methods=['GET'])
def jsonserver4():
    get = Meal.json_meal()
    return jsonify(get)


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/posilki', methods=['GET'])
def posilki():
    return jsonify('pong!')


@app.route("/api/records", methods=['GET'])
def jsonactivities():
    return jsonify({
        'status': 'success',
        'act': activity_init
    })


@app.route("/records_get", methods=['GET', 'POST'])
def jsongetactivities():
    print('asdf')
    if request.method == 'POST':
        print('jestem w innej roucie!')
        # post_data = request.get_json(force=True)
        # print(post_data)
        return redirect(url_for('report_new_vue'))
    return jsonify({
        'status': 'success',
        'act': activity_init
    })


@app.route("/report_new_vue", methods=['POST', 'GET', 'DELETE'])
def report_new_vue():
    form_filter = FilterField()
    activity_list = Activity.list_of_activity_objects()
    if form_filter.validate_on_submit():
        # filter = request.get_json(force=True)
        filter = form_filter.filter.data
        find_filtered_records = Activity.filer_activity_objects(filter)
        print(find_filtered_records)
        return render_template('report_new_vue.html', form=form_filter, activity_list=find_filtered_records)
    # if form_done.validate_on_submit():
    #     today = Date.find_date_by_date_id_and_date(_id=form_done.date_id.data, date=choosen_date)
    #     today.done = True
    #     db.session.commit()
    #     flash('Your update has been created!', 'success')
    #     return redirect(url_for('report', form_done=form_done, date_object=date_object, all_category=all_category,
    #                             choosen_date=choosen_date))
    return render_template('report_new_vue.html', form=form_filter, activity_list=activity_list)


@app.route("/activity_list/<filter_string>", methods=['GET', 'POST'])
def activity_list(filter_string):
    print('asdf')
    activity_list = Activity.list_of_activity_objects()
    data_to_convert = [{'name': i.name, 'id': i.id} for i in activity_list]
    activity_json = json.dumps(data_to_convert, ensure_ascii=False).encode('utf8')
    print(activity_json)
    if request.method == 'POST':
        print('jestem w innej roucie!')
        # post_data = request.get_json(force=True)
        # print(post_data)
        return redirect(url_for('report_new_vue'))
    return activity_json


@app.route("/report_new_vue1", methods=['POST', 'GET', 'DELETE'])
def report_new_vue1():
    return render_template('report_new_vue0.html')


@app.route("/report/<type>/<chosen_date>", methods=['POST', 'GET'])
def report_new_date(type, chosen_date):
    form_filter = FilterField()
    full_activity_list = Activity.list_of_activity_objects()
    chosen_date_objects = DateNew.find_activitys_by_date(chosen_date)
    type_true_or_false = {single: (True if single == type else False) for single in
                          ['breakfast', 'lunch', 'last_meal', 'morning', 'night']}
    act_json = Activity.json_all()
    meal_dict = Meal.json_meal()
    meal_list = Meal.list_of_meals()
    activity_symptoms = sorted(Activity.json_symptoms(), key=lambda k: k['category_id'])
    activity_meals = sorted(Activity.json_meals(), key=lambda k: k['category_id'])

    if type in ['breakfast', 'lunch', 'last_meal']:
        activity_list = activity_meals
    if type in ['morning', 'night']:
        activity_list = activity_symptoms
    print(activity_list)
    # print([(single['id'], single['category_name']) for single in activity_symptoms])

    # [single['name'] for single in act_json if single['category']]

    if type in ['breakfast', 'lunch', 'last_meal', 'morning', 'night']:
        done_activite_ids = [single.activity_id for single in
                             DateNew.find_activitys_by_date_and_type(chosen_date, **type_true_or_false)]
        if form_filter.validate_on_submit():
            # filter = request.get_json(force=True)
            filter = form_filter.filter.data
            find_filtered_records = Activity.filer_activity_objects(filter)
            # print(find_filtered_records)
            return render_template('report_new_json.html', form=form_filter, activity_list=find_filtered_records,
                                   type=type,
                                   chosen_date=chosen_date, chosen_date_objects=chosen_date_objects,
                                   done_activite_ids=done_activite_ids, meal_dict=meal_dict)
        if request.method == 'POST':
            print('jestem w innej roucie!')
            activity_ids = request.form.getlist('mycheckbox')
            if not activity_ids:
                print('robie finnal!')
                meal_ids = request.form.getlist('mycheckbox2')
                for single_id in meal_ids:
                    activity_ids = []
                    list_of_activity = Meal.find_list_of_ingredients_by_id(single_id)
                    [activity_ids.append(single_act_id) for single_act_id in list_of_activity if
                     single_act_id not in activity_ids]
            for activity_id in activity_ids:
                print(activity_id, 'post date czy okej?')
                print(done_activite_ids)
                category_id = Category.find_by_id(Activity.find_by_id(activity_id).category_id).id
                today = DateNew(date=chosen_date, **type_true_or_false, category_id=category_id,
                                activity_id=activity_id)
                DateNew.save_to_db(today)
                flash('Your update has been created!', 'success')
                done_activite_ids = [single.activity_id for single in
                                     DateNew.find_activitys_by_date_and_type(chosen_date, **type_true_or_false)]
            return render_template('report_new_json.html', form=form_filter, activity_list=activity_list, type=type,
                                   chosen_date=chosen_date, chosen_date_objects=chosen_date_objects,
                                   done_activite_ids=done_activite_ids, meal_list=meal_list, meal_dict=meal_dict,
                                   activity_symptoms=activity_symptoms, activity_meals=activity_meals)

        return render_template('report_new_json.html', type=type, form=form_filter, activity_list=activity_list,
                               chosen_date=chosen_date, chosen_date_objects=chosen_date_objects,
                               done_activite_ids=done_activite_ids, meal_dict=meal_dict,
                               activity_symptoms=activity_symptoms,
                               activity_meals=activity_meals,
                               )
    return '<h1>na spokjnie</h1>'


@app.route("/create_meal", methods=['POST', 'GET'])
def create_meal():
    form_create_meal = CreateMeal()

    if form_create_meal.validate_on_submit():
        ing = {
            'carbs_ingredients': form_create_meal.carbs_ingredients.data,
            'meat_ingredients': form_create_meal.meat_ingredients.data,
            'ingredients': form_create_meal.ingredients.data,
            'warzywa_ingredients': form_create_meal.warzywa_ingredients.data,
        }

        meal_name = form_create_meal.meal_name.data
        ingredients = Meal.ingredients_for_meal(**ing)
        try:
            Meal.query.filter_by(name=meal_name).first().name
            print(f'the {meal_name} is in the menu')
            return render_template('meal.html', form_create_meal=form_create_meal, ingredients=ingredients,
                                   meal_name=meal_name, in_menu=True)
        except AttributeError as e:
            new_meal = Meal(ingredients=ingredients['string_of_ingridients_ids'], name=meal_name)
            Meal.save_to_db(new_meal)
            print(f'we added {new_meal.name} to the menu')
            print(new_meal.name)
            return render_template('meal.html', form_create_meal=form_create_meal, ingredients=ingredients,
                                   meal_name=meal_name, added=True)
    return render_template('meal.html',
                           form_create_meal=form_create_meal)


@app.route("/update", methods=['POST', 'GET'])
def update():
    form_category = UpdateCategory()
    form_activity = UpdateActivity()
    all_cat = Category.json_all()
    choice = [(single['id'], single['name']) for single in all_cat]
    print('form_category', form_category.submit_updated_category.data)
    print('form_category', form_category.category_category_id.data)
    print('form_category', form_category.category_name.data)
    print('form_activity', form_activity.activity_activity_id.data)
    print('form_activity', form_activity.activity_name.data)
    print('form_activity', form_activity.box.data)
    print('form_activity', form_activity.activity_category_id.data)
    print('form_activity', form_activity.submit_updated_activity.data)

    print(form_category.validate_on_submit())
    print(form_activity.validate_on_submit())
    if form_category.validate_on_submit():
        a_category = Category.query.filter_by(id=form_category.category_category_id.data).first()
        print(a_category.category)
        a_category.category = form_category.category_name.data
        db.session.commit()
        # print(f'well done, we changed {form_category.name} into {form_category.category_name.data}')
        print('we have change it')
        return render_template('update.html',
                               form_activity=form_activity, form_category=form_category)
    if form_activity.validate_on_submit():
        a_activity = Activity.query.filter_by(id=form_activity.activity_activity_id.data).first()
        temp_name = a_activity.name
        a_activity.name = form_activity.activity_name.data
        if form_activity.box.data:
            a_activity.category_id = form_activity.activity_category_id.data
        db.session.commit()

        print(f'well done, we changed {temp_name} into {form_activity.activity_name.data}')
        return render_template('update.html',
                               form_activity=form_activity, form_category=form_category)
    return render_template('update.html',
                           form_activity=form_activity, form_category=form_category)


@app.route("/add", methods=['POST', 'GET'])
def add():
    form_category = AddCategory()
    form_activity = AddActivity()
    all_cat = Category.json_all()

    print(form_category.validate_on_submit())
    print(form_activity.submit_new_activity.data)
    print(form_category.submit_new_category.data)
    print(form_activity.validate_on_submit())
    if form_category.validate_on_submit() and form_category.submit_new_category.data:
        a_category = Category(category=form_category.category_name.data)
        db.session.commit()
        # print(f'well done, we changed {form_category.name} into {form_category.category_name.data}')
        print('we have change it')
        return render_template('update.html',
                               form_activity=form_activity, form_category=form_category)
    if form_activity.validate_on_submit() and form_activity.submit_new_activity.data:
        print('im here')
        try:
            print(Activity.find_by_name(form_activity.activity_name.data).name)
            return render_template('add.html',
                                   form_activity=form_activity, form_category=form_category, added_activity=True)
        except:
            a_activity = Activity(name=form_activity.activity_name.data, category_id=form_activity.category_id.data)
            a_activity.name = form_activity.activity_name.data
            # if form_activity.box.data:
            #     a_activity.category_id = form_activity.activity_category_id.data
            db.session.commit()
            print(f'well done, we added {form_activity.activity_name.data}')

        return render_template('add.html',
                               form_activity=form_activity, form_category=form_category, added_activity=True)
    return render_template('add.html',
                           form_activity=form_activity, form_category=form_category)


@app.route("/report2/<chosen_date>", methods=['POST', 'GET'])
def report_new_date2(chosen_date):
    form_filter = FilterField()
    chosen_date_objects = DateNew.find_activitys_by_date(chosen_date)

    meal_dict = Meal.json_meal()
    meal_list = Meal.list_of_meals()
    activity_symptoms = sorted(Activity.json_symptoms(), key=lambda k: k['category_id'])
    activity_meals = sorted(Activity.json_meals(), key=lambda k: k['category_id'])

    type_true_or_false = {single: (True if single == 'breakfast' else False) for single in
                          ['breakfast', 'lunch', 'last_meal', 'morning', 'night']}
    today = DateNew.json_dict_list_of_done_activies_by_date(chosen_date)
    # print(type_true_or_false)
    # print(DateNew.find_activitys_by_date_id_and_type(chosen_date, _id=20, **type_true_or_false))

    done_activite_ids = [single.activity_id for single in
                         DateNew.find_activitys_by_date_and_type(chosen_date, **type_true_or_false)]
    if form_filter.validate_on_submit():
        filter = form_filter.filter.data
        find_filtered_records = Activity.filer_activity_objects(filter)
        # print(find_filtered_records)
        return render_template('report_full_json.html', form=form_filter, activity_list=find_filtered_records,
                               type=type,
                               chosen_date=chosen_date, chosen_date_objects=chosen_date_objects,
                               done_activite_ids=done_activite_ids, meal_dict=meal_dict, today=today)
    if request.method == 'POST':
        checkboxes_breakfast = request.form.getlist('checkbox_breakfast')
        checkboxes_lunch = request.form.getlist('checkbox_lunch')
        checkboxes_last_meal = request.form.getlist('checkbox_last_meal')

        checkboxes = [{'activity_ids': request.form.getlist('checkbox_breakfast'), 'type': 'breakfast'},
                      {'activity_ids': request.form.getlist('checkbox_lunch'), 'type': 'lunch'},
                      {'activity_ids': request.form.getlist('checkbox_last_meal'), 'type': 'last_meal'},
                      {'activity_ids': request.form.getlist('checkbox_morning'), 'type': 'morning'},
                      {'activity_ids': request.form.getlist('checkbox_night'), 'type': 'night'},
                      {'activity_ids': request.form.getlist('checkbox_meal'), 'type': 'meal'}]

        for type_checkbox in checkboxes:
            if type_checkbox['type'] == 'breakfast':
                type_true_or_false = {single: (True if single == type_checkbox['type'] else False) for single in
                                      ['breakfast', 'lunch', 'last_meal', 'morning', 'night']}
            if type_checkbox['type'] == 'lunch':
                type_true_or_false = {single: (True if single == type_checkbox['type'] else False) for single in
                                      ['breakfast', 'lunch', 'last_meal', 'morning', 'night']}
            if type_checkbox['type'] == 'last_meal':
                type_true_or_false = {single: (True if single == type_checkbox['type'] else False) for single in
                                      ['breakfast', 'lunch', 'last_meal', 'morning', 'night']}
            if type_checkbox['type'] == 'morning':
                type_true_or_false = {single: (True if single == type_checkbox['type'] else False) for single in
                                      ['breakfast', 'lunch', 'last_meal', 'morning', 'night']}
            if type_checkbox['type'] == 'night':
                type_true_or_false = {single: (True if single == type_checkbox['type'] else False) for single in
                                      ['breakfast', 'lunch', 'last_meal', 'morning', 'night']}

            for activity_id in type_checkbox['activity_ids']:
                try:
                    print(
                        DateNew.find_activitys_by_date_id_and_type(chosen_date, activity_id, **type_true_or_false).date)
                    _k = DateNew.find_activitys_by_date_id_and_type(chosen_date, activity_id, **type_true_or_false).date
                    continue
                except:
                    category_id = Category.find_by_id(Activity.find_by_id(activity_id).category_id).id
                    today = DateNew(date=chosen_date, **type_true_or_false, category_id=category_id,
                                    activity_id=activity_id)
                    DateNew.save_to_db(today)
        print(type_checkbox['type'])
        print(type_checkbox['activity_ids'])

        if type_checkbox['type'] == 'meal':
            list_time_of_meal = request.form.getlist('meal_time')

            #
            #     activity_ids = []
            #     list_of_activity = Meal.find_list_of_ingredients_by_id(single_id)
            #     [activity_ids.append(single_act_id) for single_act_id in list_of_activity if
            #      single_act_id not in activity_ids]
            # for activity_id in activity_ids:
            #     print(activity_id, 'post date czy okej?')
            #     print(done_activite_ids)
            #     category_id = Category.find_by_id(Activity.find_by_id(activity_id).category_id).id
            #     today = DateNew(date=chosen_date, **type_true_or_false, category_id=category_id,
            #                     activity_id=activity_id)
            #     DateNew.save_to_db(today)
            #     flash('Your update has been created!', 'success')
        today = DateNew.json_dict_list_of_done_activies_by_date(chosen_date)

        return render_template('report_full_json.html', form=form_filter,
                               chosen_date=chosen_date, chosen_date_objects=chosen_date_objects,
                               done_activite_ids=done_activite_ids, meal_dict=meal_dict,
                               activity_symptoms=activity_symptoms,
                               activity_meals=activity_meals, today=today
                               )
    return render_template('report_full_json.html', form=form_filter,
                           chosen_date=chosen_date, chosen_date_objects=chosen_date_objects,
                           done_activite_ids=done_activite_ids, meal_dict=meal_dict,
                           activity_symptoms=activity_symptoms,
                           activity_meals=activity_meals, today=today
                           )
