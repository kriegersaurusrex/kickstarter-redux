import pandas as pd 
import numpy as np 
import pickle
from flask import Flask, redirect, url_for, render_template
from flask_bootstrap import Bootstrap
import sqlite3
import os
from joblib import dump, load
from .forms import KickStarterForm
from sklearn.model_selection import train_test_split
from category_encoders import OneHotEncoder, OrdinalEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, plot_confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from .models import DB, KickStarter
import seaborn as sns
from dotenv import load_dotenv


load_dotenv()


def create_app():
	app = Flask(__name__)
	# Set secret key in your environment variables #
	app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
	Bootstrap(app) # Trying out Bootstrap for styling forms
	DATABASE = 'sqlite:///db.sqlite3'
	app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	DB.init_app(app)
	
	
		
	@app.route('/')
	def index():
		return redirect(url_for('home'))

	@app.route('/home')
	def home():
		DB.drop_all()
		DB.create_all()
		return render_template('home.html')


	@app.route('/run_model', methods=['GET','POST'])
	def run_model():
		proceed_flag = True
		form = KickStarterForm()
		
		for fieldname, value in form.data.items():
			print(fieldname, value)
			if value == None:
				proceed_flag = False
		
		if proceed_flag:
			data_input = prepare_input_data(form)
			result = make_prediction(data_input)
			# This is where you enter all of this data into your model    #
			# Note, still testing entry data to see what output types are #
			return render_template('display_success.html', form=form, result=result)
		
		return render_template('run_model_styled.html', form=form)



	@app.route('/about')
	def about_page():
		return render_template('about.html')


	def prepare_input_data(form):
		

		dict_keys = ['id', 'name', 'blurb', 'currency', 'created_at', 'launched_at',
				'deadline', 'usd_goal', 'country_displayable_name', 'slug',
				'creator_name', 'category_id', 'category_name', 'category_slug',
				'category_position', 'category_parent_id', 'location_displayable_name',
				'location_state', 'location_type', 'location_expanded_country',
				'days_for_project']
		name = form.kickstarter_name.data
		ks_id = form.kickstarter_id.data
		ks_blurb = form.kickstarter_blurb.data
		ks_created = form.kickstarter_created.data
		ks_launched = form.kickstarter_launched.data
		ks_deadline = form.kickstarter_deadline.data
		ks_staffpick = form.kickstarter_staffpick.data
		ks_locationtype = form.kickstarter_locationtype.data
		ks_locationstate = form.kickstarter_locationstate.data
		ks_country = form.kickstarter_country.data
		ks_countrydisp = form.kickstarter_countrydisplayable.data
		ks_currency = form.kickstarter_currency.data
		ks_creatorid = form.kickstarter_creatorid.data
		ks_usdgoal = form.kickstarter_usdgoal.data
		ks_usdpledge = form.kickstarter_usdpledge.data
		ks_creatorid = form.kickstarter_creatorid.data
		ks_creatorname = form.kickstarter_creatorname.data
		ks_locationid = form.kickstarter_locationid.data
		ks_locationdisplayable = form.kickstarter_locationdisplayable.data
		ks_spotlight = form.kickstarter_spotlight.data
		ks_categoryid = form.kickstarter_categoryid.data
		ks_categoryname = form.kickstarter_categoryname.data
		ks_categoryslug = form.kickstarter_categoryslug.data
		ks_slug = form.kickstarter_slug.data
		ks_categoryparentid = form.kickstarter_categoryparentid.data
		ks_categoryposition = form.kickstarter_categoryposition.data

		input_dict = {'id': [ks_id],
					  'name': [name],
					  'blurb': [ks_blurb],
					  'currency': [ks_currency],
					  'created_at': [ks_created],
					  'launched_at': [ks_launched],
					  'deadline': [ks_deadline],
					  'usd_goal': [ks_usdgoal],
					  'country_displayable_name': [ks_countrydisp],
					  'slug': [ks_slug],
					  'creator_name': [ks_creatorname],
					  'category_id': [ks_categoryid],
					  'category_name': [ks_categoryname],
					  'category_slug': [ks_categoryslug],
					  'category_position': [ks_categoryposition],
					  'category_parent_id': [ks_categoryparentid],
					  'location_displayable_name': [ks_locationdisplayable],
					  'location_state': [ks_locationstate],
					  'location_type': [ks_locationtype],
					  'location_expanded_country': [ks_country]
					   }
		print('Input Dict:',input_dict)
		df = pd.DataFrame.from_dict(input_dict)
		df['created_at2'] = pd.to_datetime(df['created_at'], format='%m/%d/%Y')
		df['launched_at2'] = pd.to_datetime(df['launched_at'], format='%m/%d/%Y')
		df['deadline2'] = pd.to_datetime(df['deadline'], format='%m/%d/%Y')
		#New columns
		df['days_for_project'] = df['deadline2']-df['launched_at2']
		df['days_for_project'] = pd.to_numeric(df['days_for_project'].dt.days, downcast='integer')
		df.drop(columns=['created_at2', 'launched_at2', 'deadline2'], inplace=True)
		print(df[['launched_at','deadline','created_at']])
		# Write minimal data to sql database #

		ks_row = KickStarter(id=ks_id, name=name, usd_goal=ks_usdgoal, country=ks_country)
		DB.session.add(ks_row)
		DB.session.commit()
		print(df.head())
		return df

	def make_prediction(X_data):
		predictions= {0: 'Fail', 1: 'Succeed'}
		model = load('./kickstarter/static/kickstarter_model.sav')
		prediction = model.predict(X_data)
		print('Your Prediction is: ',prediction)
		return predictions[prediction[0]]




	return app

if __name__ == "__main__":
	create_app()

