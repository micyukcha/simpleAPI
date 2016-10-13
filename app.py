
# coding: utf-8

# In[ ]:

#https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/


# In[ ]:

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps


# In[ ]:

#create a engine for connecting to SQLite3
#assuming salaries.db

e = create_engine('sqlite:///salaries.db')

app = Flask(__name__)
api = Api(app)

@app.route('/departments', methods=['GET'])

class Departments_Meta(Resource):
    def get(self):
        
        #Connect to DB
        conn = e.connect()
        
        #Perform query and return JSON
        query = conn.execute("select distinct DEPARTMENT from salaries")
        return {'departments': [i[0] for i in query.cursor.fetchall()]}
    
class Departmental_Salary(Resource):
    def get(self, department_name):
        conn = e.connect()
        query = conn.execute("select * from salaries where Department=? ", (department_name.upper(),))
        
        #Query the result and get cursor. Dump data to JSON is looked by extension
        result = {'data':[dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return result
    
api.add_resource(Departmental_Salary, '/dept/<string:department_name>')
api.add_resource(Departments_Meta, '/departments')
    
if __name__ == '__main__':
    app.run(debug=True)

