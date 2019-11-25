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

from flask import Flask
from flask_restful import Api, Resource, reqparse
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


debug.info("connect BDD interface");



app = Flask(__name__)
api = Api(app)

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

class ThemeList(Resource):
	def __init__(self):
		self.name = API_THEME
	
	# example use:	curl http://127.0.0.1:15080/api/v1/theme
	def get(self):
		return data_global_elements.get_interface(self.name).gets(), 200
	
	"""
	def post(self):
		args = parser.parse_args()
		todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
		todo_id = 'todo%i' % todo_id
		TODOS[todo_id] = {'task': args['task']}
		return TODOS[todo_id], 201
	"""

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
	"""
	def put(self, id):
		ret = data_global_elements.get_interface(self.name).put(id)
		return task, 201
	"""

api.add_resource(ThemeList, "/api/v1/" + API_THEME)
api.add_resource(Theme, "/api/v1/" + API_THEME + "/<int:id>")

#---------------------------------------------------------------------------------------

class GroupList(Resource):
	def __init__(self):
		self.name = API_GROUP
	
	# example use:	curl http://127.0.0.1:15080/api/v1/Group
	def get(self):
		return data_global_elements.get_interface(self.name).gets(), 200
	
	"""
	def post(self):
		args = parser.parse_args()
		todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
		todo_id = 'todo%i' % todo_id
		TODOS[todo_id] = {'task': args['task']}
		return TODOS[todo_id], 201
	"""

class Group(Resource):
	def __init__(self):
		self.name = API_GROUP
		
	# example use:	curl http://127.0.0.1:15080/api/v1/Group/xxx
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
	"""
	def put(self, id):
		ret = data_global_elements.get_interface(self.name).put(id)
		return task, 201
	"""

api.add_resource(GroupList, "/api/v1/" + API_GROUP)
api.add_resource(Group, "/api/v1/" + API_GROUP + "/<int:id>")

#---------------------------------------------------------------------------------------

class SaisonList(Resource):
	def __init__(self):
		self.name = API_SAISON
	
	# example use:	curl http://127.0.0.1:15080/api/v1/Saison
	def get(self):
		return data_global_elements.get_interface(self.name).gets(), 200
	
	"""
	def post(self):
		args = parser.parse_args()
		todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
		todo_id = 'todo%i' % todo_id
		TODOS[todo_id] = {'task': args['task']}
		return TODOS[todo_id], 201
	"""

class Saison(Resource):
	def __init__(self):
		self.name = API_SAISON
		
	# example use:	curl http://127.0.0.1:15080/api/v1/Saison/xxx
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
	"""
	def put(self, id):
		ret = data_global_elements.get_interface(self.name).put(id)
		return task, 201
	"""

api.add_resource(SaisonList, "/api/v1/" + API_SAISON)
api.add_resource(Saison, "/api/v1/" + API_SAISON + "/<int:id>")

#---------------------------------------------------------------------------------------

class VideoList(Resource):
	def __init__(self):
		self.name = API_VIDEO
	
	# example use:	curl http://127.0.0.1:15080/api/v1/Video
	def get(self):
		return data_global_elements.get_interface(self.name).gets(), 200
	
	"""
	def post(self):
		args = parser.parse_args()
		todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
		todo_id = 'todo%i' % todo_id
		TODOS[todo_id] = {'task': args['task']}
		return TODOS[todo_id], 201
	"""

class Video(Resource):
	def __init__(self):
		self.name = API_VIDEO
		
	# example use:	curl http://127.0.0.1:15080/api/v1/Video/xxx
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
	"""
	def put(self, id):
		ret = data_global_elements.get_interface(self.name).put(id)
		return task, 201
	"""

api.add_resource(VideoList, "/api/v1/" + API_VIDEO)
api.add_resource(Video, "/api/v1/" + API_VIDEO + "/<int:id>")


rest_config = config.get_rest_config()

debug.info("Start REST application: " + str(rest_config["host"]) + ":" + str(rest_config["port"]))

app.run(debug=False, host=rest_config["host"], port=str(rest_config["port"]))

debug.info("END program");
sys.exit(0)
