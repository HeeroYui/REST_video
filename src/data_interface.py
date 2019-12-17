#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2019, Edouard DUPIN, all right reserved
##
## @license MPL v2.0 (see license file)
##

import tools
import json
from realog import debug

from sanic.exceptions import ServerError

class DataInterface():
	def __init__(self, _name, _file):
		self.model = None
		self.name = _name
		self.file = _file
		self.bdd = []
		self.need_save = False
		self.last_id = 0
		if tools.exist(self.file) == False:
			self.need_save = True
		else:
			data = tools.file_read_data(self.file)
			self.bdd = json.loads(data)
		self.upgrade_global_bdd_id();
	
	def set_data_model(self, _data_model):
		self.model = _data_model
	
	def check_with_model(self, _data):
		if self.model == None:
			return True
		values = []
		for elem in dir(self.model):
			if elem[:2] == "__":
				continue
			values.append(elem)
		have_error = False
		for key in _data.keys():
			if key not in values:
				have_error = True
				# TODO: ...
				debug.warning("Add element that is not allowed " + key + " not in " + str(values))
		for elem in values:
			if key not in _data.keys():
				have_error = True
				# TODO: ...
				debug.warning("Missing key " + elem + " not in " + str(_data.keys()))
		if have_error == True:
			return False
		for key in _data.keys():
			elem = getattr(self.model, key)
			if type(elem) == list:
				find_error = True
				for my_type in elem:
					if type(_data[key]) == my_type:
						find_error = False
						break
				if find_error == True:
					debug.warning("data : " + str(_data))
					tmp_list = []
					for my_type in elem:
						tmp_list.append(my_type.__name__)
					debug.warning("[key='" + key + "'] try to add wrong type in BDD " + type(_data[key]).__name__ + " is not: " + str(my_type))
			else:
				if type(_data[key]) != getattr(self.model, key):
					debug.warning("data : " + str(_data))
					debug.warning("[key='" + key + "'] try to add wrong type in BDD " + type(_data[key]).__name__ + " is not: " + getattr(self.model, key).__name__)
					return False
		return True
	
	def upgrade_global_bdd_id(self):
		for elem in self.bdd:
			if 'id' not in elem.keys():
				continue
			if elem["id"] >= self.last_id:
				self.last_id = elem["id"] + 1
	
	def get_table_index(id):
		id_in_bdd = 0
		for elem in self.bdd:
			if     'id' in elem.keys() \
			   and elem["id"] == id:
				return id_in_bdd
			id_in_bdd += 1
		return None
	
	def check_save(self):
		if self.need_save == False:
			return
		debug.warning("Save bdd: " + self.file)
		data = json.dumps(self.bdd, sort_keys=True, indent=4)
		self.need_save = False
		tools.file_write_data_safe(self.file, data)
	
	def gets(self):
		debug.info("gets " + self.name)
		return self.bdd
	
	def get(self, id):
		debug.info("get " + self.name + ": " + str(id))
		for elem in self.bdd:
			if     'id' in elem.keys() \
			   and elem["id"] == id:
				return elem
		return None
	
	def delete(self, id):
		debug.info("delete " + self.name + ": " + str(id))
		id_in_bdd = self.get_table_index(id)
		if id_in_bdd == None:
			return False
		del self.bdd[id_in_bdd]
		self.need_save = True
		return True
	
	def put(self, id, value):
		debug.info("put " + self.name + ": " + str(id))
		id_in_bdd = self.get_table_index(id)
		if id_in_bdd == None:
			return False
		value["id"] = id
		self.bdd[id_in_bdd] = value
		self.need_save = True
		return True
	
	def post(self, value):
		debug.info("post " + self.name)
		value["id"] = self.last_id
		self.last_id += 1
		if self.check_with_model(value) == False:
			raise ServerError("Corelation with BDD error", status_code=404)
		self.bdd.append(value)
		self.need_save = True
		return value


