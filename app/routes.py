import json

from flask import render_template, url_for, flash, redirect, jsonify, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_restful import Api

from app import app
from app import db, bcrypt
from app import engine
from app import graphs
from app.forms import DateActivityReport, ChooseDate, FilterField, ChooseTypeAndDate, CreateMeal, UpdateCategory, \
    UpdateActivity, AddActivity, AddCategory, DeleteActivity, DeleteCategory, ChooseDateNewReport, DeleteMeal, \
    LoginForm, RegistrationForm, GetNameForBackupForm, FormGuestLogin
from app.helpers import *
from app.models import Category, Activity, Date, DateNew, Meal, Stats, User, Template
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
            new_record = Category(category=category['category'], username_id=current_user.id)
            Category.save_to_db(new_record)
    return render_template('habit.html')


@app.route("/act")
def init_activity():
    for each_record in activity_init:
        print(Activity.find_by_name(each_record['name']))
        if Activity.find_by_name(each_record['name']) == None:
            category_id_for_new_record = (Category.find_by_category(each_record['category_name']).id)
            new_record = Activity(name=each_record['name'], category_id=category_id_for_new_record,
                                  username_id=current_user.id)
            Activity.save_to_db(new_record)
    return render_template('habit.html')


@app.route("/", methods=['POST', 'GET'])
def report():
    db.create_all()
    today = str(date.today())
    new_report_form = ChooseDateNewReport()
    if new_report_form.validate_on_submit():
        date_to_show = new_report_form.date_report.data
        return redirect(url_for('report_new_date2', chosen_date=date_to_show))
    return render_template('report_base.html', today=today,
                           new_report_form=new_report_form)


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


@app.route("/todos3", methods=['POST'])
def jsonserver3():
    post_data = request.args.get('name')
    print(post_data)
    return jsonify(post_data)


@app.route('/ping', methods=['GET'])
def ping_pong():
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


    #TODO List of intresting points
    # Activity.filer_activity_objects('eko')
    # if request.method == 'POST':
    #     post_data = request.form.getlist('mycheckbox')
    #     post_date = request.form.get('choosen_date')
    # meal_ids = request.form.getlist('mycheckbox2')
    #         post_data = request.get_json()
    #
    # if request.method == 'POST':
    #    post_data = request.get_json()
    #    activity_ids = request.form.getlist('mycheckbox')
    # if form_filter.validate_on_submit():
    #     # filter = request.get_json(force=True)
    #     filter = form_filter.filter.data
    #     find_filtered_records = Activity.filer_activity_objects(filter)
    #
    # activity_symptoms = sorted(Activity.json_symptoms(), key=lambda k: k['category_id'])
    # activity_meals = sorted(Activity.json_meals(), key=lambda k: k['category_id'])



    #TODO
    # create new application where you can experiment with vue, requests, charts?
    # could be copy of this application -> with copy of this database it will be like -> development -> applaying it into
    # or maybe start to use different eviroment to test? and branch out changes instead of pushing it all the time to master


@app.route("/create_meal", methods=['POST', 'GET'])
@login_required
def create_meal():
    form_create_meal = CreateMeal()
    print(Activity.find_activities_by_x_category('cukier'))
    if form_create_meal.validate_on_submit():
        ing = {
            'carbs_ingredients': form_create_meal.carbs_ingredients.data,
            'meat_ingredients': form_create_meal.meat_ingredients.data,
            'ingredients': form_create_meal.ingredients.data,
            'warzywa_ingredients': form_create_meal.warzywa_ingredients.data,
        }
        print(ing, 'whole data with ingredients')
        meal_name = form_create_meal.meal_name.data
        ingredients = Meal.ingredients_for_meal(**ing)
        try:
            assert (Meal.query.filter_by(name=meal_name).first().name, f' good, {meal_name} meal not exist in database')
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
@login_required
def update():
    form_category = UpdateCategory()
    form_activity = UpdateActivity()
    all_cat = Category.json_all()
    choice = [(single['id'], single['name']) for single in all_cat]
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
@login_required
def add():
    form_category = AddCategory()
    form_activity = AddActivity()
    all_cat = Category.json_all()

    print(form_category.validate_on_submit())
    print(form_activity.submit_new_activity.data)
    print(form_category.submit_new_category.data)
    print(form_activity.validate_on_submit())
    if form_category.validate_on_submit() and form_category.submit_new_category.data:
        a_category = Category(category=form_category.category_name.data, username_id=current_user.id)
        Category.save_to_db(a_category)
        # print(f'well done, we changed {form_category.name} into {form_category.category_name.data}')
        print('we have change it')
        return render_template('add.html',
                               form_activity=form_activity, form_category=form_category)
    if form_activity.validate_on_submit() and form_activity.submit_new_activity.data:
        print('im here')
        try:
            print('1')
            print(Activity.find_by_name(form_activity.activity_name.data).name)
            print('2')
            return render_template('add.html',
                                   form_activity=form_activity, form_category=form_category, added_activity=True)
        except:
            print('except')
            print(form_activity.activity_name.data, "form_activity.activity_name.data")
            a_activity = Activity(name=form_activity.activity_name.data, category_id=form_activity.category_id.data,
                                  username_id=current_user.id)
            # if form_activity.box.data:
            #     a_activity.category_id = form_activity.activity_category_id.data
            Activity.save_to_db(a_activity)
            print(f'well done, we added {form_activity.activity_name.data}')

        return render_template('add.html',
                               form_activity=form_activity, form_category=form_category, added_activity=True)
    return render_template('add.html',
                           form_activity=form_activity, form_category=form_category)


@app.route("/delete", methods=['POST', 'GET'])
@login_required
def delete():
    form_category = DeleteCategory()
    form_activity = DeleteActivity()
    form_meal = DeleteMeal()

    all_cat = Category.json_all()

    if form_category.validate_on_submit() and form_category.submit_delete_category.data:
        a_category = Category.find_by_id(_id=form_category.category_id.data)
        Category.delete_from_db(a_category)
        # print(f'well done, we changed {form_category.name} into {form_category.category_name.data}')
        print(f'Successful deleted category')
        return render_template('delete.html',
                               form_activity=form_activity, form_category=form_category, form_meal=form_meal)
    if form_activity.validate_on_submit() and form_activity.submit_delete_activity.data:
        print('im here in activity form')
        try:
            a_activity = Activity.find_by_id(form_activity.activity_id.data)
            print(form_activity.activity_id.data)
            print(a_activity)
        except:
            print('except, we could delete activity')
            #     a_activity.category_id = form_activity.activity_category_id.data
            print(f'well done, we added {form_activity.activity_id.data}')
        Activity.delete_from_db(a_activity)
        print(f'Successful deleted category')
        return render_template('delete.html',
                               form_activity=form_activity, form_category=form_category, form_meal=form_meal,
                               added_activity=True)
    if form_meal.validate_on_submit() and form_meal.submit_delete_meal.data:
        a_meal = Meal.find_by_id(_id=form_meal.meal_id.data)
        Meal.delete_from_db(a_meal)
        # print(f'well done, we changed {form_category.name} into {form_category.category_name.data}')
        print(f'Successful deleted category')
        return redirect(
            url_for('delete', form_activity=form_activity, form_category=form_category, form_meal=form_meal))
    return render_template('delete.html',
                           form_activity=form_activity, form_category=form_category, form_meal=form_meal)


@app.route("/report2/<chosen_date>", methods=['POST', 'GET'])
@login_required
def report_new_date2(chosen_date):
    date_info = get_date_info(chosen_date)
    form_filter = FilterField()
    chosen_date_objects = DateNew.find_activitys_by_date(chosen_date)

    meal_dict = Meal.json_meal()
    meal_list = Meal.list_of_meals()
    activity_symptoms = sorted(Activity.json_symptoms(), key=lambda k: k['category_id'])
    activity_meals = sorted(Activity.json_meals(), key=lambda k: k['category_id'])

    type_true_or_false = {single: (True if single == 'breakfast' else False) for single in
                          ['breakfast', 'lunch', 'last_meal', 'morning', 'night']}
    today = DateNew.json_dict_list_of_done_activies_by_date(chosen_date)
    print(today)
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


    all_date_records_for_chosen_date = DateNew.json_full_info_by_date(chosen_date)

    # if FormPredictionGuess.submit_prediction():
    #     id_of_prediction = form_prediction.prediction.data
    #     data_object = DateNew.find_object_by_id_and_date(id_of_prediction, chosen_date)
    #     data_object.prediction = True
    #     db.session.commit()
    #     return render_template('report_full_json.html', form=form_filter,
    #                            chosen_date=chosen_date, chosen_date_objects=chosen_date_objects,
    #                            done_activite_ids=done_activite_ids, meal_dict=meal_dict,
    #                            activity_symptoms=activity_symptoms,
    #                            activity_meals=activity_meals, today=today,
    #                            date_info=date_info
    #                            , form_prediction=form_prediction
    #                            )

    if request.method == 'POST':
        checkboxes_breakfast = request.form.getlist('checkbox_breakfast')
        checkboxes_lunch = request.form.getlist('checkbox_lunch')
        checkboxes_last_meal = request.form.getlist('checkbox_last_meal')
        prediction_choice_id = request.form.get('prediction_choice')
        if prediction_choice_id:
            data_object = DateNew.find_by_id(prediction_choice_id)
            print(data_object.id,' im hereeeeeeeeeeeeeeeee')
            data_object.prediction = True
            db.session.commit()
            flash(f'{data_object.activity.name} is your prediction for stomach problems, we added it to database')

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
                                    activity_id=activity_id, username_id=current_user.id)
                    DateNew.save_to_db(today)
                    flash('Looks like you added new records into database!')
        print(type_checkbox['type'])
        print(type_checkbox['activity_ids'])

        if type_checkbox['type'] == 'meal':
            list_time_of_meal = request.form.getlist('meal_time')
            list_meal_checkboxes = request.form.getlist('checkbox_meal')
            try:
                json_list_activity_from_meal = Meal.get_activities_by_time_of_meal_and_meal_id(list_time_of_meal,
                                                                                               list_meal_checkboxes)
                for single_type in DateNew.list_of_types():
                    try:
                        DateNew.add_to_db_by_list_and_type(list_of_activities=json_list_activity_from_meal[single_type],
                                                           type=single_type, chosen_date=chosen_date)
                    except KeyError as e:
                        error = ('you have to fill form correctly')
                        continue
            except UnboundLocalError as e:
                error = ('you have to fill form correctly')
            except IndexError as e:
                error = ('you have to fill form correctly')

        today = DateNew.json_dict_list_of_done_activies_by_date(chosen_date)
        return render_template('report_full_json.html', form=form_filter,
                               chosen_date=chosen_date, chosen_date_objects=chosen_date_objects,
                               done_activite_ids=done_activite_ids, meal_dict=meal_dict,
                               activity_symptoms=activity_symptoms,
                               activity_meals=activity_meals, today=today, error=error,
                               date_info=date_info,
                               all_date_records_for_chosen_date=all_date_records_for_chosen_date
                               )
    return render_template('report_full_json.html', form=form_filter,
                           chosen_date=chosen_date, chosen_date_objects=chosen_date_objects,
                           done_activite_ids=done_activite_ids, meal_dict=meal_dict,
                           activity_symptoms=activity_symptoms,
                           activity_meals=activity_meals, today=today,
                           date_info=date_info,
                           all_date_records_for_chosen_date=all_date_records_for_chosen_date
                           )

@app.route("/CV", methods=['POST', 'GET'])
def CV_count():
    db.create_all()
    today = str(dt.datetime.now())[:10]
    a = Stats.is_date_in_database(today)
    if a:
        object = Stats.get_object_by_date(today)
        object.visits += 1
        Stats.save_to_db(object)
    else:
        new = Stats(date=today, visits=1)
        Stats.save_to_db(new)
    return redirect(url_for('report'))


@app.route("/CV2", methods=['POST', 'GET'])
def CV_count2():
    # db.create_all()
    today = str(dt.datetime.now())[:9] + '4'
    ip_address = request.remote_addr
    access_token = 'a2f936dd1cc48c'
    print(ip_address)
    handler = ipinfo.getHandler(access_token)
    details_info = handler.getDetails(ip_address)
    new = Stats(ip=details_info.ip, location=details_info.city, date=today, country=details_info.country)
    Stats.save_to_db(new)

    return jsonify({'ip': details_info.ip,
                    'country': details_info.country,
                    'location': details_info.city})


@app.route("/show_stats", methods=['POST', 'GET'])
def show_stats():
    response = jsonify(Stats.data_json())
    return response


@app.route("/json/date", methods=['GET'])
def get_date():
    return jsonify(DateNew.json_date())


@app.route("/json/activity", methods=['GET'])
def get_activity():
    return jsonify(Activity.json_all())


@app.route("/json/category", methods=['GET'])
def get_category():
    return jsonify(Category.json_all())


@app.route("/delete/day/<chosen_date>", methods=['POST'])
@login_required
def remove_whole_day(chosen_date):
    DateNew.delete_activitys_by_date(chosen_date)
    # chosen_date_objects = DateNew.query.filter(DateNew.date == chosen_date)
    # or User.query.filter(DateNew.date == chosen_date).delete() ! powerful
    # chosen_date_objects.delete()
    db.session.commit()
    return redirect(url_for('report_new_date2', chosen_date=chosen_date))


@app.route("/drop/stats", methods=['GET'])
def drop_stats():
    db.metadata.drop_all(bind=engine, tables=[Stats.__table__])
    return redirect(url_for('report'))


@app.route("/drop/stats", methods=['GET'])
def create_all():
    db.create_all()
    return redirect(url_for('report'))


labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.route("/charts", methods=['GET'])
def charts():
    bar_labels = labels
    bar_values = values
    bar = graphs.create_plot()
    return render_template('charts.html', title='Bitcoin Monthly Price in USD', plot=bar, max=17000, labels=bar_labels,
                           values=bar_values)


@app.route("/api/chart", methods=['GET', 'POST'])
def small_api():
    di = [{'x': [1, 2, 3, 4, 5, 6],
           'y': [1, 2, 4, 8, 15, 33]}]
    return jsonify(di)


@app.route("/register", methods=['GET', 'POST'])
def register():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('report'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'hello account has been created! you are {form.username.data}', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('report'))
    form = LoginForm()
    form_guest = FormGuestLogin()
    if form_guest.validate_on_submit() and form_guest.click_here_to_test_as_guest.data:
        user = User.query.filter_by(email='guest@gmail.com').first()
        login_user(user)
        flash(f'you logged in!', 'success')
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('report'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'you logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('report'))
        else:
            flash(f'Login Unsuccessful!', 'success')
    return render_template('login.html', form=form, form_guest=form_guest)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('report'))


@app.route("/account")
@login_required
def account():
    db.create_all()
    return render_template('account.html')


@app.route("/db/backup", methods=['GET', 'POST'])
def backup_structure_of_db():
    form = GetNameForBackupForm()
    if form.validate_on_submit():
        all_records = Activity.json_all()
        print(form.backup_name)
        Template.create_new_record_from_template(name=form.backup_name.data, instances=all_records)
        return redirect(url_for('backup_structure_of_db'))
    return render_template('backup.html', form=form)


@app.route("/db/restore", methods=['GET', 'POST'])
def restore_structure_of_db():
    full_backup_to_restore = Template.find_by_name('full_Ewa').json_template['instances']
    Activity.delete_all_objects_by_current_user()
    Category.delete_all_objects_by_current_user()
    # new_category = Category(category='gluten', username_id=current_user.id)
    # db.session.add(new_category)
    # db.session.commit()
    for single_record in full_backup_to_restore:
        print(Category.find_by_name(single_record['category']))
        print(not Category.find_by_name(single_record['category']))
        if not Category.find_by_name(single_record['category']):
            print(single_record['category'])
            new_category = Category(category=single_record['category'], username_id=current_user.id)
            db.session.add(new_category)
            db.session.commit()
        new_activity = Activity(name=single_record['activity'],
                                category_id=Category.find_by_name(single_record['category']).id,
                                username_id=current_user.id)
        db.session.add(new_activity)
        db.session.commit()
    return redirect(url_for('backup_structure_of_db'))
