#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2019, Edouard DUPIN, all right reserved
##
## @license MPL v2.0 (see license file)
##
#pip install flask --user
#pip install flask_restful --user
#pip install python-dateutil --user

from sanic import Sanic
from sanic import response
from sanic import views
from sanic import Blueprint
from sanic.exceptions import ServerError
from sanic_simple_swagger import swagger_blueprint, openapi_blueprint
from sanic_simple_swagger import doc

import dateutil.parser


import time
import os
import sys
import datetime
import time, threading
import realog.debug as debug

import config
import tools
import data_interface
import data_global_elements


app = Sanic("REST_video")

app.config['API_VERSION'] = '1.0.0'
app.config['API_TITLE'] = 'Rest personal video API'
app.config['API_DESCRIPTION'] = 'Simple API for the Video broker.'
app.config['API_CONTACT_EMAIL'] = "yui.heero@gmail.com"
app.config['API_LICENSE_NAME'] = 'MPL 2.0'
app.config['API_LICENSE_URL'] = 'https://www.mozilla.org/en-US/MPL/2.0/'
app.config['schemes'] = ['http', 'https']


app.blueprint(openapi_blueprint)
app.blueprint(swagger_blueprint)

@app.route("/")
@doc.description("Get all the Theme elements")
async def test(request):
  return response.json({"hello": "world"})


def add_interface(_name):
	data_global_elements.add_interface(_name, data_interface.DataInterface(_name, os.path.join(tools.get_run_path(), "data", "bdd_" + _name + ".json")))

API_THEME = "theme"
add_interface(API_THEME)
API_GROUP = "group"
add_interface(API_GROUP)
API_SAISON = "saison"
add_interface(API_SAISON)
API_VIDEO = "video"
add_interface(API_VIDEO)

"""
class ThemeListView(views.HTTPMethodView):
	def __init__(self):
		self.name = API_THEME
	@doc.description("Get all the Theme elements")
	async def get(self, request):
		return response.json(data_global_elements.get_interface(self.name).gets())
	async def post(self, request):
		return response.json(data_global_elements.get_interface(self.name).post(request.json))

class ThemeView(views.HTTPMethodView):
	def __init__(self):
		self.name = API_THEME
	async def get(self, request, id):
		value = data_global_elements.get_interface(self.name).get(id)
		if value != None:
			return response.json(value)
		raise ServerError("No data found", status_code=404)
	async def put(self, request, id):
		ret = data_global_elements.get_interface(self.name).put(id)
		return response.json({})
	" ""
	async def patch(self, request, id):
		return response.text('I am patch method')
	"" "
	async def delete(self, request, id):
		return response.text('I am delete method')
		ret = data_global_elements.get_interface(self.name).delete(id)
		if ret == True:
			return response.json({})
		raise ServerError("No data found", status_code=404)

theme_blueprint = Blueprint(API_THEME)
theme_blueprint.add_route(ThemeListView.as_view(), '/' + API_THEME + '/', strict_slashes=True)
theme_blueprint.add_route(ThemeView.as_view(), '/' + API_THEME + '/<id:int>', strict_slashes=True)
app.blueprint(theme_blueprint)
"""

def add_theme(_app, _name_api):
	elem_blueprint = Blueprint(_name_api)
	
	class DataModel:
		name = str
		description = str
	
	@elem_blueprint.get('/' + _name_api, strict_slashes=True)
	@doc.summary("Show resources")
	@doc.description("Display a listing of the resource.")
	@doc.produces(content_type='application/json')
	async def list(request):
		return response.json(data_global_elements.get_interface(_name_api).gets())
	
	@elem_blueprint.post('/' + _name_api, strict_slashes=True)
	@doc.summary("Create new resource")
	@doc.description("Store a newly created resource in storage.")
	@doc.consumes(DataModel, location='body')#, required=True)
	@doc.response_success(status=201, description='If successful created')
	async def create(request):
		return response.json(data_global_elements.get_interface(_name_api).post(request.json))
	
	@elem_blueprint.get('/' + _name_api + '/<id:int>', strict_slashes=True)
	@doc.summary("Show resources")
	@doc.description("Display a listing of the resource.")
	@doc.produces(content_type='application/json')
	async def retrive(request, id):
		value = data_global_elements.get_interface(_name_api).get(id)
		if value != None:
			return response.json(value)
		raise ServerError("No data found", status_code=404)
	
	@elem_blueprint.put('/' + _name_api + '/<id:int>', strict_slashes=True)
	@doc.summary("Update resource")
	@doc.description("Update the specified resource in storage.")
	@doc.response_success(status=201, description='If successful updated')
	async def update(request, id):
		ret = data_global_elements.get_interface(_name_api).put(id)
		return response.json({})
	
	@elem_blueprint.delete('/' + _name_api + '/<id:int>', strict_slashes=True)
	@doc.summary("Remove resource")
	@doc.description("Remove the specified resource from storage.")
	@doc.response_success(status=201, description='If successful deleted')
	async def delete(request, id):
		ret = data_global_elements.get_interface(_name_api).delete(id)
		if ret == True:
			return response.json({})
		raise ServerError("No data found", status_code=404)
	
	_app.blueprint(elem_blueprint)

add_theme(app, API_THEME)

def add_group(_app, _name_api):
	elem_blueprint = Blueprint(_name_api)
	
	class DataModel:
		name = str
	
	@elem_blueprint.get('/' + _name_api, strict_slashes=True)
	@doc.summary("Show resources")
	@doc.description("Display a listing of the resource.")
	@doc.produces(content_type='application/json')
	async def list(request):
		return response.json(data_global_elements.get_interface(_name_api).gets())
	
	@elem_blueprint.post('/' + _name_api, strict_slashes=True)
	@doc.summary("Create new resource")
	@doc.description("Store a newly created resource in storage.")
	@doc.consumes(DataModel, location='body')#, required=True)
	@doc.response_success(status=201, description='If successful created')
	async def create(request):
		return response.json(data_global_elements.get_interface(_name_api).post(request.json))
	
	@elem_blueprint.get('/' + _name_api + '/<id:int>', strict_slashes=True)
	@doc.summary("Show resources")
	@doc.description("Display a listing of the resource.")
	@doc.produces(content_type='application/json')
	async def retrive(request, id):
		value = data_global_elements.get_interface(_name_api).get(id)
		if value != None:
			return response.json(value)
		raise ServerError("No data found", status_code=404)
	
	@elem_blueprint.put('/' + _name_api + '/<id:int>', strict_slashes=True)
	@doc.summary("Update resource")
	@doc.description("Update the specified resource in storage.")
	@doc.response_success(status=201, description='If successful updated')
	async def update(request, id):
		ret = data_global_elements.get_interface(_name_api).put(id)
		return response.json({})
	
	@elem_blueprint.delete('/' + _name_api + '/<id:int>', strict_slashes=True)
	@doc.summary("Remove resource")
	@doc.description("Remove the specified resource from storage.")
	@doc.response_success(status=201, description='If successful deleted')
	async def delete(request, id):
		ret = data_global_elements.get_interface(_name_api).delete(id)
		if ret == True:
			return response.json({})
		raise ServerError("No data found", status_code=404)
	
	_app.blueprint(elem_blueprint)

add_group(app, API_GROUP)

def add_saison(_app, _name_api):
	elem_blueprint = Blueprint(_name_api)
	
	class DataModel:
		number = int
		group_id = int
	
	@elem_blueprint.get('/' + _name_api, strict_slashes=True)
	@doc.summary("Show saisons")
	@doc.description("Display a listing of the resource.")
	@doc.produces(content_type='application/json')
	async def list(request):
		return response.json(data_global_elements.get_interface(_name_api).gets())
	
	@elem_blueprint.post('/' + _name_api, strict_slashes=True)
	@doc.summary("Create new saison")
	@doc.description("Create a new saison for a aspecific group id.")
	@doc.consumes(DataModel, location='body')#, required=True)
	@doc.response_success(status=201, description='If successful created')
	async def create(request):
		return response.json(data_global_elements.get_interface(_name_api).post(request.json))
	
	@elem_blueprint.get('/' + _name_api + '/<id:int>', strict_slashes=True)
	@doc.summary("Show resources")
	@doc.description("Display a listing of the resource.")
	@doc.produces(content_type='application/json')
	async def retrive(request, id):
		value = data_global_elements.get_interface(_name_api).get(id)
		if value != None:
			return response.json(value)
		raise ServerError("No data found", status_code=404)
	
	@elem_blueprint.put('/' + _name_api + '/<id:int>', strict_slashes=True)
	@doc.summary("Update resource")
	@doc.description("Update the specified resource in storage.")
	@doc.response_success(status=201, description='If successful updated')
	async def update(request, id):
		ret = data_global_elements.get_interface(_name_api).put(id)
		return response.json({})
	
	@elem_blueprint.delete('/' + _name_api + '/<id:int>', strict_slashes=True)
	@doc.summary("Remove resource")
	@doc.description("Remove the specified resource from storage.")
	@doc.response_success(status=201, description='If successful deleted')
	async def delete(request, id):
		ret = data_global_elements.get_interface(_name_api).delete(id)
		if ret == True:
			return response.json({})
		raise ServerError("No data found", status_code=404)
	
	_app.blueprint(elem_blueprint)

add_saison(app, API_SAISON)

def add_video(_app, _name_api):
	elem_blueprint = Blueprint(_name_api)
	
	class DataModel:
		saison_id = int
		group_id = int
		name = str
		description = str
		# creating time
		date = str
		# number of second
		time = int
	
	@elem_blueprint.get('/' + _name_api, strict_slashes=True)
	@doc.summary("Show saisons")
	@doc.description("Display a listing of the resource.")
	@doc.produces(content_type='application/json')
	async def list(request):
		return response.json(data_global_elements.get_interface(_name_api).gets())
	
	@elem_blueprint.post('/' + _name_api, strict_slashes=True)
	@doc.summary("Create new saison")
	@doc.description("Create a new saison for a aspecific group id.")
	@doc.consumes(DataModel, location='body')#, required=True)
	@doc.response_success(status=201, description='If successful created')
	async def create(request):
		return response.json(data_global_elements.get_interface(_name_api).post(request.json))
	
	@elem_blueprint.get('/' + _name_api + '/<id:int>', strict_slashes=True)
	@doc.summary("Show resources")
	@doc.description("Display a listing of the resource.")
	@doc.produces(content_type='application/json')
	async def retrive(request, id):
		value = data_global_elements.get_interface(_name_api).get(id)
		if value != None:
			return response.json(value)
		raise ServerError("No data found", status_code=404)
	
	@elem_blueprint.put('/' + _name_api + '/<id:int>', strict_slashes=True)
	@doc.summary("Update resource")
	@doc.description("Update the specified resource in storage.")
	@doc.response_success(status=201, description='If successful updated')
	async def update(request, id):
		ret = data_global_elements.get_interface(_name_api).put(id)
		return response.json({})
	
	@elem_blueprint.delete('/' + _name_api + '/<id:int>', strict_slashes=True)
	@doc.summary("Remove resource")
	@doc.description("Remove the specified resource from storage.")
	@doc.response_success(status=201, description='If successful deleted')
	async def delete(request, id):
		ret = data_global_elements.get_interface(_name_api).delete(id)
		if ret == True:
			return response.json({})
		raise ServerError("No data found", status_code=404)
	
	_app.blueprint(elem_blueprint)

add_video(app, API_VIDEO)

"""
def add_group(_group_name):
	@app.route("/qsdqd")
	@doc.description("Get all the Theme " + _group_name)
	@doc.consumes({'name': str}, location='query', description='Student name', example={'name': 'john'})
	async def test(request):
		return response.json({"hello": "world"})
		

add_group("sqdfqsdfqsfgqsdf")
"""
def add_student(_app):
	student_blueprint = Blueprint("student")
	
	class Student:
	    name = str
	    address = str
	
	@student_blueprint.get('/student', strict_slashes=True)
	@doc.summary("Show resources")
	@doc.description("Display a listing of the resource.")
	@doc.deprecated(True) #if the api is deprecated
	@doc.produces(content_type='application/json')
	@doc.consumes({'name': str}, location='query', description='Student name', example={'name': 'john'})
	async def index(request):
	    pass
	
	@student_blueprint.post('/student', strict_slashes=True)
	@doc.summary("Create new resource")
	@doc.description("Store a newly created resource in storage.")
	@doc.consumes(Student, location='body', required=True)
	@doc.response_success(status=201, description='If successful created')
	async def store(request):
	    pass
	
	@student_blueprint.put('/student/<id:int>', strict_slashes=True)
	@doc.summary("Update resource")
	@doc.description("Update the specified resource in storage.")
	@doc.response_success(status=201, description='If successful updated')
	async def update(request, id):
	    pass
	
	@student_blueprint.delete('/student/<id:int>', strict_slashes=True)
	@doc.summary("Remove resource")
	@doc.description("Remove the specified resource from storage.")
	@doc.response_success(status=201, description='If successful deleted')
	async def delete(request, id):
	    pass
	
	_app.blueprint(student_blueprint)

add_student(app)

"""
LIST_themes = [
	{
		'id': 0,
		'name': 'Documentary',
		'description': 'Documentary (annimals, space, earth...)',
	},{
		'id': 1,
		'name': 'Movie',
		'description': 'Movie with real humans (film)',
	},{
		'id': 2,
		'name': 'Annimation',
		'description': 'Annimation movies (film)',
	},{
		'id': 3,
		'name': 'Short Films',
		'description': 'Small movies (less 2 minutes)',
	},{
		'id': 4,
		'name': 'tv show',
		'description': 'Tv show form old peoples',
	}, {
		'id': 5,
		'name': 'Anniation tv show',
		'description': 'Tv show form young peoples',
	},
]


class ThemeList(Resource):
	# example use:	curl http://127.0.0.1:15080/api/v1/theme
	def get(self):
		debug.info("Request temes: " + str(time))
		return LIST_themes, 200

class Theme(Resource):
	# example use:	curl http://127.0.0.1:15080/api/v1/theme/xxx
	def get(self, id):
		debug.info("Request theme: " + str(id))
		for elem in LIST_themes:
			if     'id' in elem.keys() \
			   and elem["id"] == id:
				return elem, 200
		return "No data found in list of element: " + str(len(LIST_themes)), 404
"""
"""
class ThemeList(Resource):
	def __init__(self):
		self.name = API_THEME
	
	# example use:	curl http://127.0.0.1:15080/api/v1/theme
	def get(self):
		return data_global_elements.get_interface(self.name).gets(), 200
	
	" ""
	def post(self):
		args = parser.parse_args()
		todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
		todo_id = 'todo%i' % todo_id
		TODOS[todo_id] = {'task': args['task']}
		return TODOS[todo_id], 201
	"" "

class Theme(Resource):
	def __init__(self):
		self.name = API_THEME
		
	# example use:	curl http://127.0.0.1:15080/api/v1/theme/xxx
	def get(self, id):
		value = data_global_elements.get_interface(self.name).get(id)
		if value != None:
			return value, 200
		return "No data found", 404
	
	def delete(self, id):
		ret = data_global_elements.get_interface(self.name).delete(id)
		if ret == True:
			return '', 204
		return "No data found", 404
	"" "
	def put(self, id):
		ret = data_global_elements.get_interface(self.name).put(id)
		return task, 201
	" ""

api.add_resource(ThemeList, "/api/v1/" + API_THEME)
api.add_resource(Theme, "/api/v1/" + API_THEME + "/<int:id>")
"""



if __name__ == "__main__":
	rest_config = config.get_rest_config()
	debug.info("Start REST application: " + str(rest_config["host"]) + ":" + str(rest_config["port"]))
	app.run(host=rest_config["host"], port=int(rest_config["port"]))
	debug.info("END program");
	
	