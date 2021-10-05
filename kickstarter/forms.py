import pandas as pd
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField,\
				StringField, SelectField, DecimalField,\
				DateField
from wtforms.validators import DataRequired, ValidationError
from flask_bootstrap import Bootstrap
import os
import pickle



BOOLEAN = ['YES','NO']
LOCATION_TYPE = ['Town', 'Zip', 'County', 'Suburb', 'LocalAdmin', 'Island']
LOCATION_COUNTRY = ['United States', 'United Kingdom', 'Canada', 'New Zealand',
       'Sweden', 'Germany', 'Taiwan', 'Greece', 'Netherlands',
       'Australia', 'Japan', 'Thailand', 'Switzerland', 'Mexico', 'Kenya',
       'Italy', 'Denmark', 'China', 'Singapore', 'Hong Kong', 'France',
       'Argentina', 'Norway', "Cote d'Ivoire", 'Ireland', 'Spain',
       'Ecuador', 'Russia', 'Belgium', 'Nigeria', 'Haiti', 'South Korea',
       'Hungary', 'Guatemala', 'Egypt', 'Jamaica', 'Nicaragua', 'Peru',
       'Viet Nam', 'Dominican Republic', 'Myanmar', 'Austria', 'Lebanon',
       'India', 'Puerto Rico', 'Iceland', 'Czech Republic', 'Nepal',
       'Svalbard and Jan Mayen', 'Bulgaria', 'Poland', 'Romania',
       'Malaysia', 'Lithuania', 'Belize', 'Belarus', 'Ukraine',
       'Portugal', 'Chile', 'Philippines', 'South Africa', 'Serbia',
       'Estonia', 'Costa Rica']

COUNTRY_DISPLAYABLE_NAME= ['United States', 'United Kingdom', 'Canada', 'New Zealand',
       'Germany', 'the Netherlands', 'Australia', 'Italy', 'Switzerland',
       'Mexico', 'France', 'Denmark', 'Singapore', 'Hong Kong', 'Norway',
       'Ireland', 'Spain', 'Japan', 'Sweden', 'Belgium', 'Austria',
       'Luxembourg', 'Poland', 'Greece', 'Slovenia']

CURRENCY = ['USD', 'GBP', 'CAD', 'NZD', 'EUR', 'AUD', 'CHF', 'MXN', 'DKK',
       'SGD', 'HKD', 'NOK', 'JPY', 'SEK']

CATEGORY_PARENTID = [14.0, 1.0, 10.0, 9.0, 16.0, 7.0,
 11.0, 12.0, 18.0, 6.0, 15.0, 17.0, 13.0, 26.0, 3.0]

CATEGORY_POSITION = [18, 8, 11, 4, 10, 5, 3, 17, 6, 13, 1, 15, 7, 9, 14, 2, 12, 19, 16]

def validate_currency(form, field):
	if field.data < 10.2:
		print('Validation Error encountered')
		raise ValidationError('You need to enter currency data only')

with open('./kickstarter/static/location_state.pickle', 'rb') as handle:
    LOCATION_STATE = pickle.load(handle)

with open('./kickstarter/static/category_slug.pickle', 'rb') as handle:
    CATEGORY_SLUG = pickle.load(handle)

with open('./kickstarter/static/category_name.pickle', 'rb') as handle:
    CATEGORY_NAME = pickle.load(handle)


with open('./kickstarter/static/slug.pickle', 'rb') as handle:
    SLUG = pickle.load(handle)


with open('./kickstarter/static/category_id.pickle', 'rb') as handle:
    CAT_ID = pickle.load(handle)

with open('./kickstarter/static/location_displayable.pickle', 'rb') as handle:
    LOC_DISP = pickle.load(handle)

# KickStarter info form class definition
class KickStarterForm(FlaskForm):
	kickstarter_name = StringField(
		label='Name of Kickstarter Campaign')
	kickstarter_id = StringField(label='Campaign ID')
	kickstarter_blurb = StringField(label='Blurb')
	kickstarter_created = StringField(label='Created At', render_kw={"placeholder": "mm/dd/YY"})
	kickstarter_launched = StringField(label='Launched At', render_kw={"placeholder": "mm/dd/YY"})
	kickstarter_deadline = StringField(label='Deadline', render_kw={"placeholder": "mm/dd/YY"})
	kickstarter_staffpick = SelectField(label='Staff Pick', choices=BOOLEAN)
	kickstarter_slug = SelectField(label='Slug', choices=SLUG)
	kickstarter_locationtype= SelectField(label='Location Type', choices=LOCATION_TYPE)
	kickstarter_locationstate = SelectField(label='Location State', choices=LOCATION_STATE)
	kickstarter_country= SelectField(label='Country', choices=LOCATION_COUNTRY)
	kickstarter_locationdisplayable = SelectField(label='location displayable name',
		choices=LOC_DISP)
	kickstarter_countrydisplayable = SelectField(label='Country Displayable Name', choices=COUNTRY_DISPLAYABLE_NAME)
	kickstarter_currency= SelectField(label='Currency', choices=CURRENCY)
	kickstarter_creatorid = StringField(label='Creator ID')
	kickstarter_usdgoal = DecimalField(
		label='USD Goal  ', render_kw={"placeholder": "$00.00"})
	kickstarter_usdpledge = DecimalField(
		label='USD Pledge  ',render_kw={"placeholder": "$00.00"})
	kickstarter_creatorid = StringField(label='Creator ID')
	kickstarter_creatorname = StringField(label='Creator name')
	kickstarter_locationid = StringField(label='Location ID')
	kickstarter_spotlight = SelectField(label='Spot Light', choices=BOOLEAN)
	kickstarter_categoryid = SelectField(label='Category ID', choices=CAT_ID)
	kickstarter_categoryname = SelectField(label='Category Name', choices=CATEGORY_NAME)
	kickstarter_categoryslug = SelectField(label='Category Slug', choices=CATEGORY_SLUG)
	kickstarter_categoryparentid = SelectField(label='Category ParentID', choices=sorted(CATEGORY_PARENTID))
	kickstarter_categoryposition = SelectField(label='Category Position', choices=sorted(CATEGORY_POSITION))
	submit = SubmitField('SUBMIT')


   