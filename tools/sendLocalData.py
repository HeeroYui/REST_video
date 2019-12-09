#!/usr/bin/python
# -*- coding: utf-8 -*-
##
## @author Edouard DUPIN
##
## @copyright 2019, Edouard DUPIN, all right reserved
##
## @license MPL v2.0 (see license file)
##
import os
import copy
import sys
import hashlib
import requests  # pip install requests
import realog.debug as debug


class upload_in_chunks(object):
    def __init__(self, filename, chunksize=1 + 13):
        self.filename = filename
        self.chunksize = chunksize
        self.totalsize = os.path.getsize(filename)
        self.readsofar = 0

    def __iter__(self):
        with open(self.filename, 'rb') as file:
            while True:
                data = file.read(self.chunksize)
                if not data:
                    sys.stderr.write("\n")
                    break
                self.readsofar += len(data)
                percent = self.readsofar * 1e2 / self.totalsize
                sys.stderr.write("\rSendfing data: {percent:3.0f}% {size:14.0f} / {total_size}".format(percent=percent, size=self.readsofar, total_size=self.totalsize))
                yield data

    def __len__(self):
        return self.totalsize

#filename = 'Totally_Spies.mp4'
#result = requests.post("http://127.0.0.1:15080/data", data=upload_in_chunks(filename, chunksize=4096))
#print("result : " + str(result) + "  " + result.text)#str(dir(result)))

"""


static etk::String extractAndRemove(const etk::String& _inputValue, const char _startMark, const char _stopMark, etk::Vector<etk::String>& _values:
	_values.clear();
	etk::String out;
	bool inside=False;
	etk::String insideData;
	for (auto &it : _inputValue:
		if     inside == False
		   and it == _startMark:
			inside = True;
		elif     inside == True
		          and it == _stopMark:
			inside = False;
			_values.pushBack(insideData);
			insideData.clear();
		elif inside == True:
			insideData += it;
		else:
			out += it;
		
	
	return out;


bool progressCall(const etk::String& _value:
	return False;


void progressCallback(const etk::String& _value:
	debug.info("plop " + _value);

"""
def create_directory_of_file(_file):
	path = os.path.dirname(_file)
	try:
		os.stat(path)
	except:
		os.makedirs(path)

##
## @brief Write data in a specific path.
## @param[in] path Path of the data might be written.
## @param[in] data Data To write in the file.
## @param[in] only_if_new (default: False) Write data only if data is different.
## @return True Something has been copied
## @return False Nothing has been copied
##
def file_write_data(_path, _data, _only_if_new=False):
	if _only_if_new == True:
		if os.path.exists(_path) == True:
			old_data = file_read_data(_path)
			if old_data == _data:
				return False
	#real write of data:
	create_directory_of_file(_path)
	file = open(_path, "w")
	file.write(_data)
	file.close()
	return True

def get_modify_time(_path):
	return os.stat(_path).st_mtime

def file_read_data(_path, _binary=False):
	debug.verbose("path= " + _path)
	if not os.path.isfile(_path):
		return ""
	if _binary == True:
		file = open(_path, "rb")
	else:
		file = open(_path, "r")
	data_file = file.read()
	file.close()
	return data_file

def calculate_sha512(_path):
	sha1 = hashlib.sha512()
	file = open(_path, "rb")
	while True:
		body = file.read(4096)
		sha1.update(body)
	file.close()
	return str(sha1.hexdigest())

def push_video_file(_path, _basic_key={}):
	file_name, file_extension = os.path.splitext(_path);
	# internal file_extension ...
	if file_extension == "sha512":
		debug.verbose("file: '" + _path + "' sha512 extention ...")
		return True
	
	debug.info("Add media : '" + _path + "'")
	if     file_extension[1:] not in ["avi", "mkv", "mov", "mp4", "ts"] \
	   and file_name not in ["cover_1.jpg","cover_1.png", "cover_1.till", "cover_1.bmp", "cover_1.tga"]:
		debug.warning("Not send file : " + _path + " Not manage file_extension... " + file_extension)
		return False
	
	if file_name in ["cover_1.jpg","cover_1.png", "cover_1.till", "cover_1.bmp", "cover_1.tga"]:
		# find a cover...
		debug.warning("Not send cover Not managed ... : " + _path + " Not manage ...")
		"""
		debug.info("Send cover for: " + _basic_key["series-name"] + " " + _basic_key["saison"]);
		if _basic_key["series-name"] == "":
			debug.error("    ==> can not asociate at a specific seri");
			return False;
		
		etk::String groupName = _basic_key["series-name"];
		if _basic_key["saison"] != "":
			groupName += ":" + _basic_key["saison"];
		
		auto sending = _srv.setGroupCover(zeus::File::create(_path.getString(), ""), groupName);
		sending.onSignal(progressCallback);
		sending.waitFor(echrono::seconds(20000));
		"""
		return True
	
	"""
	if etk::path::exist(_path + ".sha512") == True:
		debug.verbose("file sha512 exist ==> read it");
		uint64_t time_sha512 = get_modify_time(_path + ".sha512");
		uint64_t time_elem = get_modify_time(_path);
		storedSha512_file = file_read_data(_path + ".sha512")
		debug.verbose("file sha == " + storedSha512_file);
		if time_elem > time_sha512:
			debug.verbose("file time > sha time ==> regenerate new one ...");
			# check the current sha512 
			storedSha512 = calculate_sha512(_path);
			debug.verbose("calculated new sha'" + storedSha512 + "'");
			if storedSha512_file != storedSha512:
				# need to remove the old sha file
				auto idFileToRemove_fut = _srv.getId(storedSha512_file).waitFor(echrono::seconds(2));
				if idFileToRemove_fut.hasError() == True:
					debug.error("can not remove the remote file with sha " + storedSha512_file);
				else:
					debug.info("Remove old deprecated file: " + storedSha512_file);
					_srv.remove(idFileToRemove_fut.get());
					# note, no need to wait the call is async ... and the user does not interested with the result ...
				
			
			# store new sha512 ==> this update tile too ...
			file.open(etk::io::OpenMode::Write);
			file.writeAll(storedSha512);
			file.close();
		else:
			# store new sha512
			/*
			storedSha512 = file.readAllString();
			file.open(etk::io::OpenMode::Read);
			file.writeAll(storedSha512);
			file.close();
			*/
			storedSha512 = storedSha512_file;
			debug.verbose("read all sha from the file'" + storedSha512 + "'");
		
	else:
	"""
	"""
	if True:
		storedSha512 = calculate_sha512(_path)
		file_write_data(_path + ".sha512", storedSha512);
		debug.info("calculate and store sha512 '" + storedSha512 + "'");
	debug.info("check file existance: sha='" + storedSha512 + "'");
	"""
	
	# push only if the file exist
	"""
	# TODO : Check the metadata updating ...
	auto idFile_fut = _srv.getId(storedSha512).waitFor(echrono::seconds(2));
	if idFile_fut.hasError() == False:
		# media already exit ==> stop here ...
		return True;
	
	# TODO: Do it better ==> add the calback to know the push progression ...
	debug.verbose("Add File : " + _path + "    sha='" + storedSha512 + "'");
	auto sending = _srv.add(zeus::File::create(_path, storedSha512));
	sending.onSignal(progressCallback);
	debug.verbose("Add done ... now waiting  ... ");
	uint32_t mediaId = sending.waitFor(echrono::seconds(20000)).get();
	debug.verbose("END WAITING ... ");
	if mediaId == 0:
		debug.error("Get media ID = 0 With no error");
		return False;
	
	"""
	result = requests.post("http://127.0.0.1:15080/data", data=upload_in_chunks(_path, chunksize=4096))
	print("result *********** : " + str(result) + "  " + result.text)#str(dir(result)))
	"""
	# Get the media
	zeus::ProxyMedia media = _srv.get(mediaId).waitFor(echrono::seconds(2000)).get();
	if media.exist() == False:
		debug.error("get media error");
		return False;
	
	
	# TODO: if the media have meta data ==> this mean that the media already added before ...
	debug.info("Find file_name : '" + file_name + "'");
	# Remove Date (XXXX) or other title
	etk::Vector<etk::String> dates;
	file_name = extractAndRemove(file_name, '(', ')', dates);
	bool haveDate = False;
	bool haveTitle = False;
	for (auto &it: dates:
		if it.size() == 0:
			continue;
		
		if     it[0] == '0'
		     or it[0] == '1'
		     or it[0] == '2'
		     or it[0] == '3'
		     or it[0] == '4'
		     or it[0] == '5'
		     or it[0] == '6'
		     or it[0] == '7'
		     or it[0] == '8'
		     or it[0] == '9':
			# find a date ...
			if haveDate == True:
				debug.info("                '" + file_name + "'");
				debug.error("Parse Date error : () : " + it + " ==> multiple date");
				continue;
			
			haveDate = True;
			_basic_key.set("date", it);
		else:
			if haveTitle == True:
				debug.info("                '" + file_name + "'");
				debug.error("Parse Title error : () : " + it + " ==> multiple title");
				continue;
			
			haveTitle = True;
			# Other title
			_basic_key.set("title2", it);
		
	
	# remove unneeded date
	if haveDate == False:
		_basic_key.set("date", "");
	
	# remove unneeded title 2
	if haveTitle == False:
		_basic_key.set("title2", "");
	
	# Remove the actors [XXX YYY][EEE TTT]...
	etk::Vector<etk::String> acthors;
	file_name = extractAndRemove(file_name, '[', ']', acthors);
	if acthors.size() > 0:
		debug.info("                '" + file_name + "'");
		etk::String actorList;
		for (auto &itActor : acthors:
			if actorList != "":
				actorList += ";";
			
			actorList += itActor;
		
		_basic_key.set("acthors", actorList);
	
	
	# remove file_extension
	file_name = etk::String(file_name.begin(), file_name.begin() + file_name.size() - (file_extension.size()+1));
	
	etk::Vector<etk::String> listElementBase = etk::split(file_name, '-');
	
	etk::Vector<etk::String> listElement;
	etk::String tmpStartString;
	for (size_t iii=0; iii<listElementBase.size(); ++iii:
		if     listElementBase[iii][0] != 's'
		   and listElementBase[iii][0] != 'e':
			if tmpStartString != "":
				tmpStartString += '-';
			
			tmpStartString += listElementBase[iii];
		else:
			listElement.pushBack(tmpStartString);
			tmpStartString = "";
			for (/* nothing to do */; iii<listElementBase.size(); ++iii:
				listElement.pushBack(listElementBase[iii]);
			
		
		
	
	if tmpStartString != "":
		listElement.pushBack(tmpStartString);
	
	if listElement.size() == 1:
		# nothing to do , it might be a film ...
		_basic_key.set("title", etk::toString(listElement[0]));
	else:
		/*
		for (auto &itt : listElement:
			debug.info("    " + itt);
		
		*/
		if     listElement.size() > 3
		   and listElement[1][0] == 's'
		   and listElement[2][0] == 'e':
			# internal formalisme ...
			int32_t saison = -1;
			int32_t episode = -1;
			etk::String seriesName = listElement[0];
			
			_basic_key.set("series-name", etk::toString(seriesName));
			etk::String fullEpisodeName = listElement[3];
			for (int32_t yyy=4; yyy<listElement.size(); ++yyy:
				fullEpisodeName += "-" + listElement[yyy];
			
			_basic_key.set("title", etk::toString(fullEpisodeName));
			if etk::String(&listElement[1][1]) == "XX":
				# saison unknow ... ==> nothing to do ...
			else:
				saison = etk::string_to_int32_t(&listElement[1][1]);
			
			if etk::String(&listElement[2][1]) == "XX":
				# episode unknow ... ==> nothing to do ...
			else:
				episode = etk::string_to_int32_t(&listElement[2][1]);
				
				_basic_key.set("episode", etk::toString(episode));
			
			debug.info("Find a internal mode series: :");
			debug.info("    origin       : '" + file_name + "'");
			etk::String saisonPrint = "XX";
			etk::String episodePrint = "XX";
			if saison < 0:
				# nothing to do
			elif saison < 10:
				saisonPrint = "0" + etk::toString(saison);
				_basic_key.set("saison", etk::toString(saison));
			else:
				saisonPrint = etk::toString(saison);
				_basic_key.set("saison", etk::toString(saison));
			
			if episode < 0:
				# nothing to do
			elif episode < 10:
				episodePrint = "0" + etk::toString(episode);
				_basic_key.set("episode", etk::toString(episode));
			else:
				episodePrint = etk::toString(episode);
				_basic_key.set("episode", etk::toString(episode));
			
			debug.info("     ==> '" + seriesName + "-s" + saisonPrint + "-e" + episodePrint + "-" + fullEpisodeName + "'");
		
	
	# send all meta data:
	zeus::FutureGroup group;
	for (auto &itKey : _basic_key:
		if itKey.second != "":
			APPL_WARNING("Set metaData: " + itKey.first + " : " + itKey.second);
		
		group.add(media.setMetadata(itKey.first, itKey.second));
	
	group.wait();
	"""
	return True;


def install_video_path( _path, _basic_key = {}):
	debug.info("Parse : '" + _path + "'");
	list_sub_path = [fff for fff in os.listdir(_path) if os.path.isdir(os.path.join(_path, fff))]
	for it_path in list_sub_path:
		basic_key_tmp = copy.deepcopy(_basic_key)
		debug.info("Add Sub path: '" + it_path + "'");
		if len(basic_key_tmp) == 0:
			debug.info("find A '" + it_path + "' " + str(len(basic_key_tmp)));
			if it_path == "documentary":
				basic_key_tmp["type"] = 0
			elif it_path == "film":
				basic_key_tmp["type"] = 1
			elif it_path == "film-annimation":
				basic_key_tmp["type"] = 2
			elif it_path == "film-short":
				basic_key_tmp["type"] = 3
			elif it_path == "tv-show":
				basic_key_tmp["type"] = 4
			elif it_path == "tv-show-annimation":
				basic_key_tmp["type"] = 5
			elif it_path == "theater":
				basic_key_tmp["type"] = 6
			elif it_path == "one-man":
				basic_key_tmp["type"] = 7
			elif it_path == "concert":
				basic_key_tmp["type"] = 8
			elif it_path == "opera":
				basic_key_tmp["type"] = 9
		else:
			debug.info("find B '" + it_path + "' " + str(len(basic_key_tmp)))
			if it_path == "saison_01":
				basic_key_tmp["saison"] = 1
			elif it_path == "saison_02":
				basic_key_tmp["saison"] = 2
			elif it_path == "saison_03":
				basic_key_tmp["saison"] = 3
			elif it_path == "saison_04":
				basic_key_tmp["saison"] = 4
			elif it_path == "saison_05":
				basic_key_tmp["saison"] = 5
			elif it_path == "saison_06":
				basic_key_tmp["saison"] = 6
			elif it_path == "saison_07":
				basic_key_tmp["saison"] = 7
			elif it_path == "saison_08":
				basic_key_tmp["saison"] = 8
			elif it_path == "saison_09":
				basic_key_tmp["saison"] = 9
			elif it_path == "saison_10":
				basic_key_tmp["saison"] = 10
			elif it_path == "saison_11":
				basic_key_tmp["saison"] = 11
			elif it_path == "saison_12":
				basic_key_tmp["saison"] = 12
			elif it_path == "saison_13":
				basic_key_tmp["saison"] = 13
			elif it_path == "saison_14":
				basic_key_tmp["saison"] = 14
			elif it_path == "saison_15":
				basic_key_tmp["saison"] = 15
			elif it_path == "saison_16":
				basic_key_tmp["saison"] = 16
			elif it_path == "saison_17":
				basic_key_tmp["saison"] = 17
			elif it_path == "saison_18":
				basic_key_tmp["saison"] = 18
			elif it_path == "saison_19":
				basic_key_tmp["saison"] = 19
			elif it_path == "saison_20":
				basic_key_tmp["saison"] = 20
			elif it_path == "saison_21":
				basic_key_tmp["saison"] = 21
			elif it_path == "saison_22":
				basic_key_tmp["saison"] = 22
			elif it_path == "saison_23":
				basic_key_tmp["saison"] = 23
			elif it_path == "saison_24":
				basic_key_tmp["saison"] = 24
			elif it_path == "saison_25":
				basic_key_tmp["saison"] = 25
			elif it_path == "saison_26":
				basic_key_tmp["saison"] = 26
			elif it_path == "saison_27":
				basic_key_tmp["saison"] = 27
			elif it_path == "saison_28":
				basic_key_tmp["saison"] = 28
			elif it_path == "saison_29":
				basic_key_tmp["saison"] = 29
			else:
				basic_key_tmp["series-name"] = it_path
		debug.info("add a path " + os.path.join(_path, it_path) + " with keys " + str(basic_key_tmp))
		install_video_path(os.path.join(_path, it_path), basic_key_tmp);
	
	# Add files :
	list_sub_file = [fff for fff in os.listdir(_path) if os.path.isfile(os.path.join(_path, fff))]
	for it_file in list_sub_file:
		basic_key_tmp = copy.deepcopy(_basic_key)
		push_video_file(os.path.join(_path, it_file), basic_key_tmp);
	




property = {
	"hostname": "127.0.0.1",
	"port": 15080,
	"login": None,
	"password": None,
	
}

import death.Arguments as arguments
import death.ArgElement as arg_element

my_args = arguments.Arguments()
my_args.add_section("option", "Can be set one time in all case")
my_args.add("h", "help", desc="Display this help")
my_args.add("",  "version", desc="Display the application version")
my_args.add("v", "verbose", list=[
								["0","None"],
								["1","error"],
								["2","warning"],
								["3","info"],
								["4","debug"],
								["5","verbose"],
								["6","extreme_verbose"],
								], desc="display debug level (verbose) default =2")
my_args.add("a", "action", list=[
								["list","List all the files"],
								["push","push a single file"],
								["push_path","push a full folder"],
								], desc="possible action")
my_args.add("c", "color", desc="Display message in color")
my_args.add("f", "folder", haveParam=False, desc="Display the folder instead of the git repository name")
local_argument = my_args.parse()

##
## @brief Display the help of this package.
##
def usage():
	color = debug.get_color_set()
	# generic argument displayed : 
	my_args.display()
	exit(0)

##
## @brief Display the version of this package.
##
def version():
	color = debug.get_color_set()
	import pkg_resources
	print("version: 0.0.0")
	foldername = os.path.dirname(__file__)
	print("source folder is: " + foldername)
	exit(0)

folder = "dataPush"
requestAction = "list"

# preparse the argument to get the verbose element for debug mode
def parse_arg(argument):
	debug.warning("parse arg : " + argument.get_option_name() + " " + argument.get_arg())
	if argument.get_option_name() == "help":
		usage()
		return True
	elif argument.get_option_name() == "version":
		version()
		return True
	elif argument.get_option_name() == "verbose":
		debug.set_level(int(argument.get_arg()))
		return True
	elif argument.get_option_name() == "color":
		if check_boolean(argument.get_arg()) == True:
			debug.enable_color()
		else:
			debug.disable_color()
		return True
	elif argument.get_option_name() == "folder":
		folder = argument.get_arg()
		return True
	elif argument.get_option_name() == "action":
		global requestAction
		requestAction = argument.get_arg()
		return True
	return False


# parse default unique argument:
for argument in local_argument:
	parse_arg(argument)

debug.info("==================================");
debug.info("== ZEUS test client start        ==");
debug.info("==================================");

# ****************************************************************************************
# **   Clear All the data base ...
# ****************************************************************************************
if requestAction == "clear":
	debug.info("============================================");
	debug.info("== Clear data base: ");
	debug.info("============================================");
	# TODO : Do it :
	debug.error("NEED to add check in cmd line to execute it ...");
	"""
	uint32_t count = remoteServiceVideo.count().wait().get();
	debug.debug("have " + count + " medias");
	for (uint32_t iii=0; iii<count ; iii += 1024:
		uint32_t tmpMax = etk::min(iii + 1024, count);
		debug.debug("read section " + iii + " -> " + tmpMax);
		etk::Vector<uint32_t> list = remoteServiceVideo.getIds(iii,tmpMax).wait().get();
		zeus::FutureGroup groupWait;
		for (auto& it : list:
			debug.info("remove ELEMENT : " + it);
			groupWait.add(remoteServiceVideo.remove(it));
		groupWait.waitFor(echrono::seconds(2000));
	"""
	debug.info("============================================");
	debug.info("==              DONE                      ==");
	debug.info("============================================");
elif requestAction == "list":
	debug.info("============================================");
	debug.info("== list files: ");
	debug.info("============================================");
	"""
	uint32_t count = remoteServiceVideo.count().wait().get();
	debug.debug("have " + count + " medias");
	for (uint32_t iii=0; iii<count ; iii += 1024:
		uint32_t tmpMax = etk::min(iii + 1024, count);
		debug.debug("read section " + iii + " -> " + tmpMax);
		etk::Vector<uint32_t> list = remoteServiceVideo.getIds(iii, tmpMax).wait().get();
		for (auto& it : list:
			# Get the media
			zeus::ProxyMedia media = remoteServiceVideo.get(it).waitFor(echrono::seconds(2000)).get();
			if media.exist() == False:
				debug.error("get media error");
				return -1;
			debug.debug("    Get title ...");
			etk::String name    = media.getMetadata("title").wait().get();
			debug.debug("    Get series-name ...");
			etk::String serie   = media.getMetadata("series-name").wait().get();
			debug.debug("    Get episode ...");
			etk::String episode = media.getMetadata("episode").wait().get();
			debug.debug("    Get saison ...");
			etk::String saison  = media.getMetadata("saison").wait().get();
			etk::String outputDesc = "";
			if serie != "":
				outputDesc += serie + "-";
			if saison != "":
				outputDesc += "s" + saison + "-";
			if episode != "":
				outputDesc += "e" + episode + "-";
			outputDesc += name;
			debug.info("[" + it + "] '" + outputDesc + "'");
	"""
	debug.info("============================================");
	debug.info("==              DONE                      ==");
	debug.info("============================================");
elif requestAction == "push":
	debug.info("============================================");
	debug.info("== push file: ");
	debug.info("============================================");
	push_video_file(folder);
	debug.info("============================================");
	debug.info("==              DONE                      ==");
	debug.info("============================================");
elif requestAction == "push_path":
	debug.info("============================================");
	debug.info("== push path: ");
	debug.info("============================================");
	install_video_path(folder);
	debug.info("============================================");
	debug.info("==              DONE                      ==");
	debug.info("============================================");
else:
	debug.info("============================================");
	debug.error("== Unknow action: '" + requestAction + "'");
	debug.info("============================================");

