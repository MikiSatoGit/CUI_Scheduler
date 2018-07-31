# coding: utf-8
#
#	schedule.py
#	CUI Task Scheduler
#	Create on: 2018.07.19
#	Author   : Miki Sato <miki.sam.sato@gmail.com>
#
#	ARGUMENT:
#	python schedule.py [None]
#

import sys
import os.path
import ConfigParser
import json
from collections import OrderedDict
import datetime
from time import sleep
import gantt
import copy
import webbrowser
#TEST		from selenium import webdriver

class GlobalParameter(object):
	def __init__(self):
		self.g_jsonfile_path = ""	#db_schedule.json"
		self.g_json_file = ""		#open(self.g_jsonfile_path, "r")
		self.g_json_obj = ""		#json.load( self.g_json_file, object_pairs_hook=OrderedDict )
		self.g_keytype = ""
		self.g_keyword = ""
		self.g_latest_ID = 0
		self.g_jsfile_path = ""		#schedule.js"
		self.g_js_file = ""			#open(self.g_jsfile_path, "r")
		self.g_jsonlock_path = ""
		self.g_jslock_path = ""
#TEST	self.g_web_driver = webdriver.Chrome("./opt/chromedriver.exe")
#TEST	self.g_web_driver = webdriver.Ie("./opt/IEDriverServer.exe")
#TEST	local_path = os.path.dirname(os.path.abspath(__file__))
#TEST	self.g_url = "file:///" + local_path + "/schedule.html"

##### Functions #####
def IsLockDB():
	ret = False
	if os.path.exists(gp.g_jsonlock_path):
		ret = True
	return ret

def LockDB():
	count = 0
	while IsLockDB():
		sleep(0.01)
		count += 1
		print("."),
		if count > 10:
			print("Someone updating DB file. Please try again later.")
			break
	with open(gp.g_jsonlock_path, mode='w') as f:
		f.write(datetime.datetime.now().strftime("%Y-%m-%d %X")) 
		f.close()

def UnlockDB():
	if os.path.exists(gp.g_jsonlock_path):
		os.remove(gp.g_jsonlock_path)

def UpdateDB():
	# Lock DB file
	LockDB()
	# write data
	gp.g_json_file = open(gp.g_jsonfile_path, "w")
	json.dump(gp.g_json_obj, gp.g_json_file)
	gp.g_json_file.close()
	# Unlock DB file
	UnlockDB()

def IsLockJS():
	ret = False
	if os.path.exists(gp.g_jslock_path):
		ret = True
	return ret

def LockJS():
	count = 0
	while IsLockJS():
		sleep(0.01)
		count += 1
		print("."),
		if count > 10:
			print("Someone updating Chart file. Please try again later.")
			break
	with open(gp.g_jslock_path, mode='w') as f:
		f.write(datetime.datetime.now().strftime("%Y-%m-%d %X")) 
		f.close()

def UnlockJS():
	if os.path.exists(gp.g_jslock_path):
		os.remove(gp.g_jslock_path)

def Initialize(db_filename):
	# read ini
	config = ConfigParser.SafeConfigParser()
	if os.path.exists("config.ini"):
		config.read("./config.ini")
		if db_filename=="":
			gp.g_jsonfile_path = config.get('DATABASE', 'dbfile')
		else:
			gp.g_jsonfile_path = db_filename
		gp.g_jsfile_path = config.get('DATABASE', 'jsfile')
	else:
		logger.info("[ERROR] Could not find:config.ini. Use default value.")
	print("Datalist: %s" % gp.g_jsonfile_path)

	gp.g_jsonfile_path = gp.g_jsonfile_path.replace("\\", "/")
	gp.g_jsonlock_path = gp.g_jsonfile_path[:gp.g_jsonfile_path.rfind("/")]
	gp.g_jsonlock_path += "/.lock"

	gp.g_jsfile_path = gp.g_jsfile_path.replace("\\","/")
	gp.g_jslock_path = gp.g_jsfile_path[:gp.g_jsfile_path.rfind("/")]
	gp.g_jslock_path += "/.lock"
	# read data
	if not os.path.exists(gp.g_jsonfile_path):
		with open(gp.g_jsonfile_path, mode='w') as f:
			f.write("{\"latestID\": 0}") 
			print("created new DB file")
			f.close()

	gp.g_json_file = open(gp.g_jsonfile_path, "r")
	gp.g_json_obj = json.load( gp.g_json_file, object_pairs_hook=OrderedDict )
	gp.g_json_file.close()
	gp.g_keytype = ""
	gp.g_keyword = ""
	gp.g_latest_ID =  gp.g_json_obj["latestID"]
#TEST	gp.g_web_driver.get(gp.g_url)

def ShowTask(datalist):
	datalist = OrderedDict(datalist)
	print("----------")
	print(" id : %s" % ( datalist["id"] ) )
	print(" title : %s" % ( datalist["title"] ) )
	print(" type : %s" % ( datalist["type"] ) )
	print(" member : %s" % ( datalist["member"] ) )
#TBD	print(" co-member : %s" % ( datalist["co-member"] ) )
	print(" created : %s" % ( datalist["created"] ) )
	print(" due : %s" % ( datalist["due"] ) )
	print(" open : %s" % ( datalist["open"] ) )
	print(" close : %s" % ( datalist["close"] ) )
	print(" description : %s" % ( datalist["description"] ) )
	print(" status : %s" % ( datalist["status"] ) )
	print(" progress : %s" % ( datalist["progress"] ) )

def ShowTaskList(datalist):
	datalist = OrderedDict(datalist)
	for key in datalist.keys():
		if key == "latestID":
			continue
		item = OrderedDict(datalist[key])
		print("<%s> " % item["type"]),
		print("(%s) " % item["id"]),
		print("%s" % item["title"]),
		print("[%s]" % item["member"])

		if isinstance(datalist[key], dict):
			datalist[key] = subShowTaskList(datalist[key])

def subShowTaskList(datalist):
	datalist = OrderedDict(datalist)
	for key in datalist.keys():
		if key == "latestID":
			continue
		if isinstance(datalist[key], dict):
			item = OrderedDict(datalist[key])
			print(" -> sub "),
			print("(%s) " % item["id"]),
			print("%s" % item["title"]),
			print("[%s]" % item["member"])
			datalist[key] = subShowTaskList(datalist[key])
	return datalist

def ShowAllTasks(datalist):
	datalist = OrderedDict(datalist)
	for key in datalist.keys():
		if key == "latestID":
			continue
		ShowTask(datalist[key])
		if isinstance(datalist[key], dict):
			datalist[key] = subShowAllTasks(datalist[key])

def subShowAllTasks(datalist):
	datalist = OrderedDict(datalist)
	for key in datalist.keys():
		if key == "latestID":
			continue
		if isinstance(datalist[key], dict):
			ShowTask(datalist[key])
			datalist[key] = subShowAllTasks(datalist[key])
	return datalist

def UpdateLatestID(datalist):
	max_id = 0
	datalist = OrderedDict(datalist)
	for key in datalist.keys():
		if key == "latestID":
			continue
		tmp_id, datalist[key] = subUpdateLatestID(datalist[key])
		if tmp_id > max_id:
			max_id = tmp_id

	gp.g_json_obj["latestID"] = max_id
	gp.g_json_file = open(gp.g_jsonfile_path, "w")
	json.dump(gp.g_json_obj, gp.g_json_file)
	gp.g_json_file.close()
	return max_id

def subUpdateLatestID(datalist):
	max_id = 0
	datalist = OrderedDict(datalist)
	for key in datalist.keys():
		if key == "latestID":
			continue
		if key == "id":
			if int(datalist["id"]) > max_id:
				max_id = int(datalist["id"])
		if isinstance(datalist[key], dict):
			tmp_id, datalist[key] = subUpdateLatestID(datalist[key])
			if tmp_id > max_id:
				max_id = tmp_id
	return max_id, datalist

def GetNewID(datalist):
	LockDB()
	datalist = OrderedDict(datalist)
	new_id = gp.g_json_obj["latestID"] + 1 
	gp.g_json_obj["latestID"] = new_id
	gp.g_json_file = open(gp.g_jsonfile_path, "w")
	json.dump(gp.g_json_obj, gp.g_json_file)
	gp.g_json_file.close()
	gp.g_latest_ID = gp.g_json_obj["latestID"]
	UnlockDB()
	return new_id

def GetTaskID(taskname, datalist):
	ret_id = 0
	datalist = OrderedDict(datalist)
	if  taskname.isdigit():
		gp.g_keytype = "id"
		gp.g_keyword = taskname
	else:
		gp.g_keytype = "title"
		gp.g_keyword = taskname

	for key in datalist.keys():
		if key == "latestID":
			continue
		if isinstance(datalist[key], dict):
			ret_id, datalist[key] = subGetTaskID(datalist[key])
			if ret_id != 0:
				break
	gp.g_keytype = ""
	gp.g_keyword = ""
	return str(ret_id)

def subGetTaskID(datalist):
	ret_id = 0
	datalist = OrderedDict(datalist)
	for key in datalist.keys():
		if key == "latestID":
			continue
		if isinstance(datalist[key], dict):
			ret_id, datalist[key] = subGetTaskID(datalist[key])
			if ret_id != 0:
				break
		elif gp.g_keyword == str(datalist[gp.g_keytype]):
			ret_id = datalist["id"]
			break
	return ret_id, datalist

def CreateNewTask(id, title, type, member, due):
	# create new element
	new_task = OrderedDict()
	new_task["id"] = new_ID
	new_task["title"] = task_name
	new_task["type"] = type_name 
	new_task["member"] = member_name 
	new_task["co-member"] = "" 
	new_task["created"] = datetime.datetime.now().strftime("%Y-%m-%d") 
	new_task["due"] = due_date 
	new_task["open"] = ""
	new_task["close"] = "" 
	new_task["description"] = "\n[" + datetime.datetime.now().strftime("%Y-%m-%d") + "] " + "created:" + description 
	new_task["status"] = "todo"
	new_task["progress"] = "0%"

	# add new element
	new_data = OrderedDict()
	new_data = {str(new_ID):new_task}
	print("--> Create Task ID %s" % str(new_ID))
	return new_data

def SearchTaskbyID(datalist):
	ret_id = []
	datalist = OrderedDict(datalist)
	for key in datalist.keys():
		if key == "latestID":
			continue
		if isinstance(datalist[key], dict):
			tmp_id, datalist[key] = subSearchTaskbyID(datalist[key])
			if len(tmp_id) != 0:
				ret_id.extend(tmp_id)
	return ret_id

def subSearchTaskbyID(datalist):
	ret_id = []
	datalist = OrderedDict(datalist)
	for key in datalist.keys():
		if key == "latestID":
			continue
		if isinstance(datalist[key], dict):
			tmp_id, datalist[key] = subSearchTaskbyID(datalist[key])
			if len(tmp_id) != 0:
				ret_id.extend(tmp_id)
				ret_id.append(datalist["id"])
		elif key == "id" and gp.g_keyword == str(datalist[key]):
			ret_id.append(datalist["id"])
	return ret_id, datalist

def AddSubTask(new_task, task_id_order, datalist):
	datalist = OrderedDict(datalist)
	depth = len(task_id_order)
	if depth != 0:
		tmp_task_id_order = task_id_order
		tmp_id = tmp_task_id_order[depth-1]
		if depth == 1:
			datalist[str(tmp_id)].update(new_task)
			return datalist
		else:
			tmp_task_id_order.pop()
			datalist[str(tmp_id)] = AddSubTask(new_task, tmp_task_id_order, datalist[str(tmp_id)])
	return datalist

def DeleteTask(task_id_order, datalist):
	datalist = OrderedDict(datalist)
	depth = len(task_id_order)
	if depth != 0:
		tmp_task_id_order = task_id_order
		tmp_id = tmp_task_id_order[depth-1]
		if depth ==1:
			datalist.pop(str(tmp_id))
			return datalist
		else:
			tmp_task_id_order.pop()
			datalist[str(tmp_id)] = DeleteTask(tmp_task_id_order, datalist[str(tmp_id)])
	return datalist

def SearchKey(datalist):
	ret_id = []
	datalist = OrderedDict(datalist)
	for key in datalist.keys():
		if key == "latestID":
			continue
		if isinstance(datalist[key], dict):
			tmp_id, datalist[key] = subSearchKey(datalist[key])
			if len(tmp_id) != 0:
				ret_id.extend(tmp_id)
	return ret_id

def subSearchKey(datalist):
	ret_id = []
	datalist = OrderedDict(datalist)
	for key in datalist.keys():
		if key == "latestID":
			continue
		if isinstance(datalist[key], dict):
			tmp_id, datalist[key] = subSearchKey(datalist[key])
			if len(tmp_id) != 0:
				ret_id.extend(tmp_id)
		elif gp.g_keytype == "" or key == gp.g_keytype:
			if gp.g_keyword in str(datalist[key]):
				print("-----[%s] found in [%s]" % (gp.g_keyword, key))
				ShowTask(datalist)
				ret_id.append(datalist["id"])
	return ret_id, datalist

def SearchMytask(datalist, member_name):
	datalist = OrderedDict(datalist)
	ret_id = []
	gp.g_keytype = "member"
	gp.g_keyword = member_name
	print("---------- Task of %s" % member_name)
	ret_id = SearchKey(datalist)

#TBD	gp.g_keytype = "co-member"
#TBD	print "----- as co-member"
#TBD	ret_id = SearchKey(datalist)

	gp.g_keytype = ""
	gp.g_keyword = ""

def ChangeStatus(new_status, new_date, task_id_order, datalist):
	datalist = OrderedDict(datalist)
	# set default date
	if new_date == "":
		new_date = datetime.datetime.now().strftime("%Y-%m-%d") 
	depth = len(task_id_order)
	if depth != 0:
		tmp_task_id_order = task_id_order
		tmp_id = tmp_task_id_order[depth-1]
		if depth ==1:
			update_data = datalist[str(tmp_id)]

			# update status
			update_data["status"] = new_status
			if new_status=="open":
				update_data["open"] = new_date
				update_data["close"] = ""
			elif new_status=="close":
				update_data["close"] = new_date
			elif new_status=="pending":
				update_data["close"] = ""

			# update description
			note_now = update_data["description"]
			note_add = "status changed to %s" % new_status
			update_data["description"] = note_now + "\n[" + datetime.datetime.now().strftime("%Y-%m-%d") + "] " + note_add

			# update element
			datalist[str(tmp_id)].update(update_data)
			return datalist
		else:
			tmp_task_id_order.pop()
			datalist[str(tmp_id)] = ChangeStatus(new_status, new_date, tmp_task_id_order, datalist[str(tmp_id)])
	return datalist

def ChangeItem(updating_type, new_data, task_id_order, datalist):
	datalist = OrderedDict(datalist)
	depth = len(task_id_order)
	if depth != 0:
		tmp_task_id_order = task_id_order
		tmp_id = tmp_task_id_order[depth-1]
		if depth ==1:
			update_data = datalist[str(tmp_id)]

			# update due
			data_now = update_data[updating_type]
			update_data[updating_type] = new_data

			# update description
			note_now = update_data["description"]
			note_add = "%s changed from %s to %s" % (updating_type, data_now, new_data)
			update_data["description"] = note_now + "\n[" + datetime.datetime.now().strftime("%Y-%m-%d") + "] " + note_add

			# update element
			datalist[str(tmp_id)].update(update_data)
			return datalist
		else:
			tmp_task_id_order.pop()
			datalist[str(tmp_id)] = ChangeItem(updating_type, new_data, tmp_task_id_order, datalist[str(tmp_id)])
	return datalist

def ChangeNote(new_note, task_id_order, datalist):
	datalist = OrderedDict(datalist)
	# set default date
	if new_note == "":
		return datalist
	depth = len(task_id_order)
	if depth != 0:
		tmp_task_id_order = task_id_order
		tmp_id = tmp_task_id_order[depth-1]
		if depth ==1:
			update_data = datalist[str(tmp_id)]

			# update description
			note_now = update_data["description"]
			update_data["description"] = note_now + "\n[" + datetime.datetime.now().strftime("%Y-%m-%d") + "] " + new_note
			datalist[str(tmp_id)].update(update_data)
			return datalist
		else:
			tmp_task_id_order.pop()
			datalist[str(tmp_id)] = ChangeNote(new_note, tmp_task_id_order, datalist[str(tmp_id)])
	return datalist

def CheckDelay(today_date, datalist):
	datalist = OrderedDict(datalist)
	for key in datalist.keys():
		if key == "latestID":
			continue
		if isinstance(datalist[key], dict):
			datalist[key] = subCheckDelay(today_date, datalist[key])
	return datalist

def subCheckDelay(today_date, datalist):
	datalist = OrderedDict(datalist)
	for key in datalist.keys():
		if key == "latestID":
			continue
		if isinstance(datalist[key], dict):
			datalist[key] = subCheckDelay(today_date, datalist[key])
		elif key == "due":
			current_due = datalist[key]
			if current_due < today_date and datalist["status"]!="close":
				update_data = datalist
				update_data["status"] = "delayed"
				ShowTask(update_data)
				# update element
				datalist.update(update_data)
			else:
				if datalist["status"] == "delayed":
					update_data = datalist
					if update_data["open"]=="":
						update_data["status"] = "todo"
					else:
						update_data["status"] = "open"
					if update_data["close"]!="":
						update_data["status"] = "close"
					ShowTask(update_data)
					# update element
					datalist.update(update_data)
	return datalist



##### Test Sample for Drawing Gantt Chart #####
def DrawPythonGantt():
	# set font
	gantt.define_font_attributes(
		fill='black',
		stroke='black',
		stroke_width=0,
		font_family="Verdana"
	)

	# create project (type)
	p1 = gantt.Project(name='Projet 1')

	# create resource (member)
	rChart1 = gantt.Resource('Chart1')
	rChart2 = gantt.Resource('Chart2')

	# create task
	t1 = gantt.Task(
		name='T1',
		start=datetime.date(2018, 7, 1),	# open
		duration=4,							# open - due
		percent_done=44,					# (open-today) / (open-due)
		resources=[rChart1],				# member
		color="#FF8080")					# member color

	t2 = gantt.Task(
		name='T2',
		start=datetime.date(2018, 7, 10),
		duration=4,
		percent_done=44,
		resources=[rChart2],
		color="#FF8080")

	#create milestone
	ms1 = gantt.Milestone(
		name=' ',
		depends_of=[t1, t2])


	# add task to project
	p1.add_task(t1)
	p1.add_task(t2)
	p1.add_task(ms1)

	# draw chart
	p1.make_svg_for_tasks(
		filename='test.svg',
		today=datetime.date(2018, 7, 12),
		start=datetime.date(2018, 6, 25),
		end=datetime.date(2018, 12, 31)
	)


def updateAnyGanttJS(datalist):
	LockJS()
	gp.g_js_file = open(gp.g_jsfile_path, "w")
	txt_header = "var chart;\n"
	txt_header += "anychart.onDocumentReady(function () {\n"
	txt_header += "var json = {\n"
	txt_header += "    \"gantt\": {\n"
	txt_header += "        \"type\": \"project\",\n"
	txt_header += "        \"controller\": {\n"
	txt_header += "            \"treeData\": {\n"
	txt_header += "                \"children\": [\n"
	txt_header += "                    {\n"
	gp.g_js_file.write(txt_header)

	txt_body = CreateJSTaskList(datalist)
	gp.g_js_file.write(txt_body)

	txt_footer = "                    }\n"
	txt_footer += "                ]\n"
	txt_footer += "            }\n"
	txt_footer += "        }\n"
	txt_footer += "    }\n"
	txt_footer += "};\n"
	txt_footer += "chart = anychart.fromJson(json);\n"
	txt_footer += "var dataGrid = chart.dataGrid();\n"
	txt_footer += "var thirdColumn = dataGrid.column(2);\n"
	txt_footer += "thirdColumn.labels().hAlign(\"left\");\n"
	txt_footer += "thirdColumn.title(\"Type\");\n"
	txt_footer += "thirdColumn.labels().format(\"{%type}\");\n"
	txt_footer += "var forthColumn = dataGrid.column(3);\n"
	txt_footer += "forthColumn.labels().hAlign(\"left\");\n"
	txt_footer += "forthColumn.title(\"Member\");\n"
	txt_footer += "forthColumn.labels().format(\"{%member}\");\n"
	txt_footer += "chart.rowSelectedFill('#FFFFCC');\n"
	txt_footer += "var tooltip = dataGrid.tooltip();\n"
	txt_footer += "tooltip.format(\"{%description}\");\n"
	txt_footer += "chart.getTimeline().elements().selected().fill('#CCFF99');\n"
	txt_footer += "var t1 = chart.getTimeline().lineMarker(0).value(\"current\");\n"
	txt_footer += "chart.container(\'container\');\n"
	txt_footer += "chart.draw();\n"
	txt_footer += "chart.fitAll();\n"
	txt_footer += "});"

	gp.g_js_file.write(txt_footer)

	gp.g_js_file.close()
	UnlockJS()
	return

def CreateJSTaskList(datalist):
	datalist = OrderedDict(datalist)
	out_txt = ""
	ret_txt = ""
	ret_txt_list = []
	parent_txt = ""
	child_txt_list = []
	datalist = OrderedDict(datalist)
	for key in datalist.keys():
		if key == "latestID":
			continue
		if isinstance(datalist[key], dict):
			parent_txt = CreateJSTask(datalist[key], )
			if parent_txt != "":
				ret_txt_list.append(parent_txt)

			child_txt_list, datalist[key] = copy.deepcopy(subCreateJSTaskList(datalist[key]))
			child_size = len(child_txt_list)
			if child_size != 0:
				ret_txt = "\"children\": [\n"
				for i in range(0,child_size):
					ret_txt += "{\n"
					ret_txt += child_txt_list[i]
					ret_txt += "}"
					if i != child_size-1:
						ret_txt += ",\n"
					else:
						ret_txt += "\n"
				ret_txt += "]\n"
				ret_txt_list.append(ret_txt)
		ret_txt_list.append("},{\n")

	for tmp_txt in ret_txt_list:
		out_txt += tmp_txt
	out_txt = out_txt[:out_txt.rfind('},{')]
	out_txt = out_txt.replace("},\n{\n\"children\"", "\"children\"")

	return out_txt

def subCreateJSTaskList(datalist):
	datalist = OrderedDict(datalist)
	ret_txt = ""
	ret_txt_list = []
	child_txt_list = []
	for key in datalist.keys():
		if key == "latestID":
			continue
		if isinstance(datalist[key], dict):
			ret_txt = CreateJSTask(datalist[key])
			ret_txt_list.append(ret_txt)
			child_txt_list, datalist[key] = copy.deepcopy(subCreateJSTaskList(datalist[key]))
			child_size = len(child_txt_list)
			if child_size != 0:
				ret_txt = "\"children\": [\n"
				for i in range(0,child_size):
					ret_txt += "{\n"
					ret_txt += child_txt_list[i]
					ret_txt += "}"
					if i != child_size-1:
						ret_txt += ",\n"
					else:
						ret_txt += "\n"
				ret_txt += "]\n"
				ret_txt_list.append(ret_txt)
	return ret_txt_list, datalist

def CreateJSTask(datalist):
	ret_txt = ""
	ret_txt += "\"treeDataItemData\": {\n"
	ret_txt += "    \"id\":" + str(datalist["id"]) + ",\n"
	ret_txt += "    \"name\": \"[" +str(datalist["id"]) + "] " + datalist["title"] + "\",\n"
	ret_txt += "    \"type\": \"" + datalist["type"] + "\",\n"
	ret_txt += "    \"member\": \"" + datalist["member"] + "\",\n"
	if datalist["open"]=="":
		ret_txt += "    \"actualStart\": \"" + datalist["due"] + "\",\n"
	else:
		ret_txt += "    \"actualStart\": \"" + datalist["open"] + "\",\n"
	ret_txt += "    \"actualEnd\": \"" + datalist["due"] + "\",\n"
	if datalist["progress"]!= "0%":
		ret_txt += "    \"progressValue\": \"" + datalist["progress"] + "\",\n"
	desc_txt = "    \"description\": \"" + datalist["description"]
	desc_txt = desc_txt.replace("\n", "\\n")
	desc_txt += "\"\n"
	ret_txt += desc_txt
	ret_txt += " },\n"
	return ret_txt


#################### Main Process ####################

#argvs = sys.argv
#argc = len(argvs)
#new_data = ""
#if argc==2 :
#	command = argvs[1]

if __name__ == '__main__':

	argvs = sys.argv
	argc = len(argvs)
	db_filename = ""
	if argc==2 :
		db_filename = argvs[1]
	if db_filename != "":
		if db_filename.find(".json")==-1:
			db_filename = "./db/" + db_filename + ".json"

	gp = GlobalParameter()
	Initialize(db_filename)

	command = ""
	isRun = True
	print "Please enter command (-h : command list)"
	while isRun:
		command = raw_input(">> ")

		if command=="-h":
			print "<ARGUMENTS (Option)>"
			print "# ARG1 : Task DB file name (json)"
			print "  - Op1 ) Full file path of Task DB file ended in \".json\" -> Use/Create the specified json file."
			print "  - Op2 ) Task DB name without \".json\" -> Use/Create the specified json file in ./db folder."
			print "<COMMAND LIST>"
			print "# -h : show command list"
			print "# key? : show key of task item"
			print "# type? : show available types of task"
			print "# all : show all tasks"
			print "# list : show title list"
			print "# add : add main task"
			print "# sub : add sub task"
			print "# del : delete task"
			print "# open : set status as [doing] and set start date"
			print "# close : set status as [done] and set completion date"
			print "# pending : set status as [pending]"
			print "# progress : change progress"
			print "# title : change title"
			print "# member : change member"
			print "# due : change due date"
			print "# note : add note in description."
			print "# chart : create ganntchart and open in browser"
			print "# update : update ganntchart"
			print "# search : search task by keyword"
			print "# mytask : show tasks for the specified member"
			print "# delay? : check delayed task"
			print "# quit : exit application"

		if command=="quit" or command=="exit":
#TEST		gp.g_web_driver.close()
			sys.exit()

		elif command=="key?":
			print("id : ID of task")
			print("title : title of task")
			print("type : type os task")
			print("member : responsible of task")
#TBD		print("co-member : co-member of task")
			print("created : creation date")
			print("due : due date")
			print("open : start date")
			print("close : completion date")
			print("description : description of task")
			print("status : current status(todo, open, close, pending, delayed)")
			print("progress : progress of task (%)")

		elif command=="type?":
			type_list = []
			for key in gp.g_json_obj.keys():
				if key == "latestID":
					continue
				add_flag = True
				item = OrderedDict(gp.g_json_obj[key])
				for tmp_type in type_list:
					if item["type"] == tmp_type:
						add_flag = False
						break
				if add_flag:
					type_list.append(item["type"])
			for tmp_type in type_list:
				print("[%s]" % tmp_type)

		elif command=="all":
			LockDB()
			ShowAllTasks(gp.g_json_obj)
			UnlockDB()

		elif command=="list":
			LockDB()
			ShowTaskList(gp.g_json_obj)
			UnlockDB()

		elif command=="add":
			print "[add] Task name?"
			task_name = raw_input("[add] >> ")
			print "[add] Type?"
			type_name = raw_input("[add] >> ")
			print "[add] Whose task?"
			member_name = raw_input("[add] >> ")
			print "[add] Due date? (YYYY-MM-DD)"
			due_date = raw_input("[add] >> ")
			due_date = due_date.replace("/","-")
			print "[add] Any description?"
			description = raw_input("[add] >> ")
			# Create New ID
			new_ID = GetNewID(gp.g_json_obj)
			# add new element
			new_data = CreateNewTask( new_ID, task_name, type_name, member_name, due_date)
			gp.g_json_obj.update(new_data)
			# write data
			UpdateDB()

		elif command=="sub":
			print "[sub] Parent task name?"
			parent_task_name = raw_input("[sub] >> ")
			parent_task_name = GetTaskID(parent_task_name, gp.g_json_obj)
			print("->Parent Task ID: %s" % parent_task_name)
			if parent_task_name == str(0):
				print("Parent task does not exist.")
				continue
			print "[sub] Sub task name?"
			task_name = raw_input("[sub] >> ")
			print "[sub] Whose task?"
			member_name = raw_input("[sub] >> ")
			print "[sub] Due date? (YYYY-MM-DD)"
			due_date = raw_input("[sub] >> ")
			due_date = due_date.replace("/","-")
			print "[sub] Any description?"
			description = raw_input("[sub] >> ")
			# check Task ID layer
			gp.g_keyword = parent_task_name
			ret_id = SearchTaskbyID(gp.g_json_obj)
			gp.g_keyword = ""
	
			# check task type
			tmp_ret_id = copy.deepcopy(ret_id)
			tmp_datalist = gp.g_json_obj
			while len(tmp_ret_id)>1:
				tmp_datalist = tmp_datalist[str(tmp_ret_id[-1])]
				tmp_ret_id.pop()
			type_name = tmp_datalist[str(tmp_ret_id[-1])]["type"]
			# Create New ID
			new_ID = GetNewID(gp.g_json_obj)
			# add new element
			new_task = CreateNewTask( new_ID, task_name, type_name, member_name, due_date)
			gp.g_json_obj = AddSubTask(new_task, ret_id, gp.g_json_obj)
			# write data
			UpdateDB()

		elif command=="del":
			print "[del] Task name?"
			task_name = raw_input("[del] >> ")
			task_name = GetTaskID(task_name, gp.g_json_obj)
			print("->Task ID: %s" % task_name)
			if task_name == str(0):
				print("Task does not exist.")
				continue
			# check Task ID layer
			gp.g_keyword = task_name
			ret_id = SearchTaskbyID(gp.g_json_obj)
			gp.g_keyword = ""
			# delete item
			gp.g_json_obj = DeleteTask(ret_id, gp.g_json_obj)
			# write data
			UpdateDB()

		elif command=="open":
			print "[open] Task name?"
			task_name = raw_input("[open] >> ")
			task_name = GetTaskID(task_name, gp.g_json_obj)
			print("->Task ID: %s" % task_name)
			if task_name == str(0):
				print("Task does not exist.")
				continue
			print "[open] Date? (YYYY-MM-DD default:today)"
			new_date = raw_input("[open] >> ")
			new_date = new_date.replace("/","-")
			# check Task ID layer
			gp.g_keyword = task_name
			ret_id = SearchTaskbyID(gp.g_json_obj)
			gp.g_keyword = ""
			# update status
			gp.g_json_obj = ChangeStatus("open", new_date, ret_id, gp.g_json_obj)
			# write data
			UpdateDB()

		elif command=="close":
			print "[close] Task name?"
			task_name = raw_input("[close] >> ")
			task_name = GetTaskID(task_name, gp.g_json_obj)
			print("->Task ID: %s" % task_name)
			if task_name == str(0):
				print("Task does not exist.")
				continue
			print "[close] Date? (YYYY-MM-DD default:today)"
			new_date = raw_input("[close] >> ")
			new_date = new_date.replace("/","-")
			# check Task ID layer
			gp.g_keyword = task_name
			ret_id = SearchTaskbyID(gp.g_json_obj)
			# update status
			gp.g_json_obj = ChangeStatus("close", new_date, ret_id, gp.g_json_obj)
			gp.g_keyword = task_name
			ret_id = SearchTaskbyID(gp.g_json_obj)
			gp.g_keyword = ""
			gp.g_json_obj = ChangeItem("progress", "100%", ret_id, gp.g_json_obj)
			# write data
			UpdateDB()

		elif command=="pending":
			print "[pending] Task name?"
			task_name = raw_input("[pending] >> ")
			task_name = GetTaskID(task_name, gp.g_json_obj)
			print("->Task ID: %s" % task_name)
			if task_name == str(0):
				print("Task does not exist.")
				continue
			# check Task ID layer
			gp.g_keyword = task_name
			ret_id = SearchTaskbyID(gp.g_json_obj)
			gp.g_keyword = ""
			# update status
			new_date = ""
			gp.g_json_obj = ChangeStatus("pending", new_date, ret_id, gp.g_json_obj)
			# write data
			UpdateDB()

		elif command=="progress":
			print "[progress] Task name?"
			task_name = raw_input("[progress] >> ")
			task_name = GetTaskID(task_name, gp.g_json_obj)
			print("->Task ID: %s" % task_name)
			if task_name == str(0):
				print("Task does not exist.")
				continue
			print "[progress] Progress [%] ?"
			new_progress = raw_input("[progress] >> ")
			new_progress = new_progress.replace("%","")
			new_progress = new_progress + "%"
			print new_progress
			# check Task ID layer
			gp.g_keyword = task_name
			ret_id = SearchTaskbyID(gp.g_json_obj)
			gp.g_keyword = ""
			# update progress
			gp.g_json_obj = ChangeItem("progress", new_progress, ret_id, gp.g_json_obj)
			# write data
			UpdateDB()

		elif command=="title":
			print "[title] Current task name?"
			task_name = raw_input("[title] >> ")
			task_name = GetTaskID(task_name, gp.g_json_obj)
			print("->Task ID: %s" % task_name)
			if task_name == str(0):
				print("Task does not exist.")
				continue
			print "[title] New task name?"
			new_task_name = raw_input("[title] >> ")
			# check Task ID layer
			gp.g_keyword = task_name
			ret_id = SearchTaskbyID(gp.g_json_obj)
			gp.g_keyword = ""
			# update title
			gp.g_json_obj = ChangeItem("title", new_task_name, ret_id, gp.g_json_obj)
			# write data
			UpdateDB()

		elif command=="member":
			print "[member] Task name?"
			task_name = raw_input("[member] >> ")
			task_name = GetTaskID(task_name, gp.g_json_obj)
			print("->Task ID: %s" % task_name)
			if task_name == str(0):
				print("Task does not exist.")
				continue
			print "[member] Who?"
			new_member = raw_input("[member] >> ")
			# check Task ID layer
			gp.g_keyword = task_name
			ret_id = SearchTaskbyID(gp.g_json_obj)
			gp.g_keyword = ""
			# update member
			gp.g_json_obj = ChangeItem("member", new_member, ret_id, gp.g_json_obj)
			# write data
			UpdateDB()

		elif command=="due":
			print "[due] Task name?"
			task_name = raw_input("[due] >> ")
			task_name = GetTaskID(task_name, gp.g_json_obj)
			print("->Task ID: %s" % task_name)
			if task_name == str(0):
				print("Task does not exist.")
				continue
			print "[due] Date? (YYYY-MM-DD)"
			new_date = raw_input("[due] >> ")
			new_date = new_date.replace("/","-")
			if new_date == "":
				new_date = datetime.datetime.now().strftime("%Y-%m-%d") 
			# check Task ID layer
			gp.g_keyword = task_name
			ret_id = SearchTaskbyID(gp.g_json_obj)
			gp.g_keyword = ""
			# update item
			gp.g_json_obj = ChangeItem("due", new_date, ret_id, gp.g_json_obj)
			# write data
			UpdateDB()

		elif command=="note":
			print "[note] Task name?"
			task_name = raw_input("[note] >> ")
			task_name = GetTaskID(task_name, gp.g_json_obj)
			print("->Task ID: %s" % task_name)
			if task_name == str(0):
				print("Task does not exist.")
				continue
			print "[note] Description?"
			note_add = raw_input("[note] >> ")
			# check Task ID layer
			gp.g_keyword = task_name
			ret_id = SearchTaskbyID(gp.g_json_obj)
			gp.g_keyword = ""
			# update description
			gp.g_json_obj = ChangeNote(note_add, ret_id, gp.g_json_obj)
			# write data
			UpdateDB()

		elif command=="search":
			print "[search] Keytype?"
			gp.g_keytype = raw_input("[search] >> ")
			print "[search] Keyword?"
			gp.g_keyword = raw_input("[search] >> ")
			# search item
			LockDB()
			ret_id = SearchKey(gp.g_json_obj)
			UnlockDB()
			gp.g_keytype = ""
			gp.g_keyword = ""

		elif command=="mytask":
			print "[mytask] Member name?"
			member_name = raw_input("[mytask] >> ")
			LockDB()
			SearchMytask(gp.g_json_obj, member_name)
			UnlockDB()

		elif command=="delay?":
			# Check due date
			today = datetime.datetime.now().strftime("%Y-%m-%d") 
			gp.g_json_obj = CheckDelay(today, gp.g_json_obj)
			# write data
			UpdateDB()

		elif command=="chart":
			updateAnyGanttJS(gp.g_json_obj)
#TEST		gp.g_web_driver.refresh()
			webbrowser.open("schedule.html", new=1)

		elif command=="update":
			updateAnyGanttJS(gp.g_json_obj)

		elif command=="test1":
			LockJS()
		elif command=="test2":
			UnlockJS()

		sleep(0.02)
