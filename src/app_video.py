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
import json
import os
import sys
import datetime
import time, threading
import realog.debug as debug

import config
import tools
import data_interface
import data_global_elements

rest_config = config.get_rest_config()

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
@doc.description("get api system information")
async def test(request):
	return response.json({
			"api-type":"video-broker",
			"api-version": app.config['API_VERSION'],
			"title": app.config['API_TITLE'],
			"description": app.config['API_DESCRIPTION'],
			"contact": app.config['API_CONTACT_EMAIL'],
			"licence": app.config['API_LICENSE_NAME']
		})


def add_interface(_name):
	data_global_elements.add_interface(_name, data_interface.DataInterface(_name, os.path.join(tools.get_run_path(), "data", "bdd_" + _name + ".json")))

API_TYPE = "type"
add_interface(API_TYPE)
API_GROUP = "group"
add_interface(API_GROUP)
API_SAISON = "saison"
add_interface(API_SAISON)
API_VIDEO = "video"
add_interface(API_VIDEO)
API_DATA = "data"

def add_type(_app, _name_api):
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

add_type(app, API_TYPE)

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
	
	@elem_blueprint.post('/' + _name_api + "/find", strict_slashes=True)
	@doc.summary("Create new resource if the name does not already exist")
	@doc.description("Store a newly created resource in storage.")
	@doc.consumes(DataModel, location='body')#, required=True)
	@doc.response_success(status=201, description='If successful created')
	async def find_with_name(request):
		api = data_global_elements.get_interface(_name_api)
		for elem in api.bdd:
			if elem["name"] == request.json["name"]:
				return response.json({"id": elem["id"]})
		raise ServerError("No data found", status_code=404)
	
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
	
	@elem_blueprint.post('/' + _name_api + "/find", strict_slashes=True)
	@doc.summary("find a season existance")
	@doc.description("return the ID of the season table.")
	@doc.consumes(DataModel, location='body')
	@doc.response_success(status=201, description='If successful created')
	async def find_with_name(request):
		api = data_global_elements.get_interface(_name_api)
		for elem in api.bdd:
			if     elem["group_id"] == request.json["group_id"] \
			   and elem["number"] == request.json["number"]:
				return response.json({"id": elem["id"]})
		raise ServerError("No data found", status_code=404)
	
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
		type_id = int
		saison_id = int
		episode = int
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
		"""
		if "group_name" in request.json.keys():
			id_group = data_global_elements.get_interface(API_GROUP).find_or_create_name(request.json["group_name"])
		"""
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

tmp_value = 0

#curl  -F 'file=@Totally_Spies.mp4;type=application/octet-stream' -H 'transfer-encoding:chunked' 127.0.0.1:15080/data -X POST -O; echo ;

def add_data(_app, _name_api):
	elem_blueprint = Blueprint(_name_api)
	"""
	@elem_blueprint.get('/' + _name_api, strict_slashes=True)
	@doc.summary("Show saisons")
	@doc.description("Display a listing of the resource.")
	@doc.produces(content_type='application/json')
	async def list(request):
		return response.json(data_global_elements.get_interface(_name_api).gets())
	"""
	
	@elem_blueprint.post('/' + _name_api, strict_slashes=True, stream=True)
	@doc.summary("send new file data")
	@doc.description("Create a new data file (associated with his sha512.")
	#@doc.consumes(DataModel, location='body')#, required=True)
	@doc.response_success(status=201, description='If successful created')
	async def create(_request):
		debug.info("request streaming " + str(_request));
		args_with_blank_values = _request.headers
		debug.info("List arguments: " + str(args_with_blank_values));
		async def streaming(_response):
			debug.info("streaming " + str(_response));
			total_size = 0
			temporary_file = os.path.join(rest_config["tmp_data"], str(tmp_value) + ".tmp")
			if not os.path.exists(rest_config["tmp_data"]):
				os.makedirs(rest_config["tmp_data"])
			if not os.path.exists(rest_config["data_media"]):
				os.makedirs(rest_config["data_media"])
			file_stream = open(temporary_file,"wb")
			sha1 = hashlib.sha512()
			while True:
				body = await _request.stream.read()
				if body is None:
					debug.warning("empty body");
					break
				total_size += len(body)
				debug.verbose("body " + str(len(body)) + "/" + str(total_size))
				file_stream.write(body)
				sha1.update(body)
			file_stream.close()
			print("SHA512: " + str(sha1.hexdigest()))
			destination_filename = os.path.join(rest_config["data_media"], str(sha1.hexdigest()))
			if os.path.isfile(destination_filename) == True:
				answer_data = {
					"size": total_size,
					"sha512": str(sha1.hexdigest()),
					"already_exist": True,
				}
				
				await _response.write(json.dumps(answer_data, sort_keys=True, indent=4))
				return
			shutil.move(temporary_file, destination_filename)
			data_metafile = {
				"sha512": str(sha1.hexdigest()),
				"size": total_size,
				'filename': _request.headers["filename"],
				'mime-type': _request.headers["mime-type"],
			}
			tools.file_write_data(destination_filename + ".meta", json.dumps(data_metafile, sort_keys=True, indent=4))
			answer_data = {
				"size": total_size,
				"sha512": str(sha1.hexdigest()),
				"already_exist": True,
			}
			await _response.write(json.dumps(answer_data, sort_keys=True, indent=4))
		return response.stream(streaming, content_type='application/json')
	
	"""
	@elem_blueprint.get('/' + _name_api + '/<id:int>', strict_slashes=True)
	@doc.summary("Show resources")
	@doc.description("Display a listing of the resource.")
	@doc.produces(content_type='application/json')
	async def retrive(request, id):
		value = data_global_elements.get_interface(_name_api).get(id)
		if value != None:
			return response.json(value)
		raise ServerError("No data found", status_code=404)
	"""
	
	
	_app.blueprint(elem_blueprint)

add_data(app, API_DATA)

import hashlib
import shutil



if __name__ == "__main__":
	debug.info("Start REST application: " + str(rest_config["host"]) + ":" + str(rest_config["port"]))
	app.config.REQUEST_MAX_SIZE=10*1024*1024*1024
	app.run(host=rest_config["host"], port=int(rest_config["port"]))
	debug.info("END program");
	sys.exit(0)


