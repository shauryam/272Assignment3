from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify, request, Response
from sqlalchemy import desc
import flask
import json

app=Flask(__name__)
db=SQLAlchemy(app)
DATABASE = 'TESTDB'
PASSWORD = 'test123'
USER = 'testuser'
HOSTNAME = 'localhost'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s/%s'%(USER, PASSWORD, HOSTNAME, DATABASE)

	
				
def datetimeserial(value):
	if value is None:
		return None
	return value.strftime("%Y-%m-%d")



class data(db.Model):
	__tablename__='server2'
	id=db.Column('id',db.Integer,primary_key=True,autoincrement=False)
	name=db.Column(db.String(50))
	email=db.Column(db.String(320))
	category=db.Column(db.String(100))
	description=db.Column(db.String(200))
	link=db.Column(db.String(100))
	estimated_costs=db.Column(db.String(10))
	submit_date=db.Column(db.String(50))
	status=db.Column(db.String(20))
	decision_date=db.Column(db.Date)

	def serialize(self):
		return {
	'id' : self.id,	
	'name' : self.name,
	'email' : self.email,
	'category' : self.category,
	'description' : self.description,
	'link' : self.link,
	'estimated_costs' : self.estimated_costs,
	'submit_date' : self.submit_date,
	'status' : self.status,
	'decision_date' : datetimeserial(self.decision_date)
			}
	
	
def __init__(self,id,name,email,category,description,link,estimated_costs,submit_date,status,decision_date):
	self.id=id
	self.name=name
	self.email=email
	self.category=category
	self.description=description
	self.link=link
	self.estimated_costs=estimated_costs
	self.submit_date=submit_date
	self.status=status
	self.decision_date=decision_date


@app.route('/v1/expenses/<expense_id>',methods=["POST"])
def insertrecords(expense_id):

	entry=data()
	reqdata=request.get_json('id')
	entry.id=int(reqdata['id'])	
	entry.name=reqdata['name']
	entry.email=reqdata['email']
	entry.category=reqdata['category']
	entry.description=reqdata['description']
	entry.link=reqdata['link']
	entry.estimated_costs=reqdata['estimated_costs']
	entry.submit_date=reqdata['submit_date']
	entry.status='pending'
	entry.decision_date=""
	db.session.add(entry)
	db.session.commit()
	return jsonify((data.query.order_by(data.id.desc()).first()).serialize()), 201
	
	

@app.route('/v1/expenses/<expense_id>',methods=["GET"])
def selectrecords(expense_id):
	no_object=data.query.filter_by(id=expense_id).first()
	if no_object is None:
		return 'Error Invalid Id', 404
	return jsonify(data.query.filter_by(id=expense_id).first().serialize()), 200

@app.route('/v1/expenses/<expense_id>',methods=["PUT"])
def editrecords(expense_id):
	update=data()	
	reqdata=request.get_json('estimated_costs')
	update.estimated_costs=reqdata['estimated_costs']
	data.query.filter_by(id=expense_id).update({data.estimated_costs:update.estimated_costs})
	db.session.commit()	
	return 'Sucess', 202

@app.route('/v1/expenses/<expense_id>',methods=["DELETE"])
def deleterecords(expense_id):
	data.query.filter_by(id=expense_id).delete()
	db.session.commit()	
	return 'Deleted', 204




if __name__ == '__main__':
	db.create_all()	
	app.run(host="0.0.0.0",port=4000)

	

