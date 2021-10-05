from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


# User Table using SQLAlchemy syntax
class KickStarter(DB.Model):
    """Twitter Users that correspond to tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)
    name = DB.Column(DB.String, nullable=False)
    usd_goal = DB.Column(DB.Float, nullable=False)
    country = DB.Column(DB.String, nullable=False)
    

    def __repr__(self):
        return "<Kickstarter name: {}, USD-GOAL: {}, Country: {}>".format(self.name, self.usd_goal, self.country)