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

class DataInterface():
	def __init__(self, _name, _file):
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
		self.bdd.append(value)
		self.need_save = True
		return value


