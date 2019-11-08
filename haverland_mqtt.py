import json
import requests
import paho.mqtt.client as mqtt
import time

# Default Smartbox ID and first heater address
dev_id = "{your_device_id}"
addr = "2"

# Global variables for heater control

units = "C"			# units
away = 'false'		# away_status
away_enabled = 'true'		# away_status

ss_2 = "ok"			# sync_status
m_2 = "off"			# mode
st_2 = "5.0"		# stemp 
l_2 = 'false'		# locked
rp_2 = "high"		# priority
ao_2 = "0.5"		# away_offset
wm_2 = 'false'		# window_mode_enabled
tr_2 = 'false'		# true_radiant_enabled

ss_3 = "ok"			# sync_status
m_3 = "off"			# mode
st_3 = "5.0"		# stemp 
l_3 = 'false'		# locked
rp_3 = "high"		# priority
ao_3 = "0.5"		# away_offset
wm_3 = 'false'		# window_mode_enabled
tr_3 = 'false'		# true_radiant_enabled

data = ""

# Default Smartbox ID and first heater address
dev_id = ""
addr = "2"

# Default API urls
token_url = "https://api-haverland.helki.com/client/token"
api_url = "https://api-haverland.helki.com/api/v2/devs"

# Default MQTT topics
haverland_token_topic = 'HAVERLAND/tokens/access_token'
haverland_expires_topic = 'HAVERLAND/tokens/expires_in'
haverland_refresh_topic = 'HAVERLAND/tokens/refresh_token'

haverland_devs_topic = 'HAVERLAND/devs'
haverland_away_topic = 'HAVERLAND/away'
haverland_plimit_topic = 'HAVERLAND/plimit'
haverland_nodes_topic = 'HAVERLAND/devs/nodes'
haverland_heater_topic = 'HAVERLAND/devs/htr'
haverland_mode_command_topic = '/mode_command'
haverland_mode_state_topic = '/mode_state'
haverland_power_command_topic = '/power_command'
haverland_temperature_command_topic = '/temperature_command'

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
	global t, expires_in, units
	global ss_2, m_2, st_2, l_2
	global ss_3, m_3, st_3, l_3
	global rp_2, ao_2, wm_2, tr_2
	global rp_3, ao_3, wm_3, tr_3
	exp_time = round(time.time(),0) - t
	rem_time = expires_in - exp_time
	if (expires_in - exp_time) > 0:
		print("minutes remaining to token: " + str(round(rem_time * 0.01666666666666666666666666666667,0)))
	else:
		print("time is up!")
		get_token()
	x = msg.payload.decode("utf-8")
	if msg.topic == "HAVERLAND/devs/htr/2/mode_command":
		topic = "HAVERLAND/devs/htr/2/mode_state"
		url = "https://api-haverland.helki.com/api/v2/devs/{your_device_id}/htr/2/status"
		infot = mqttc.publish(topic, x, qos=0, retain=True)
		if x == "heat":
			m_2 = "manual"
			data = {'mode':'manual','stemp':st_2,'units':units,'locked':l_2}
			topic = "HAVERLAND/devs/htr/2/power_command"
			infot = mqttc.publish(topic, True, qos=0, retain=True)
		elif x == "auto":
			m_2 = "modified_auto"
			data = {'mode':'modified_auto','stemp':st_2,'units':units,'locked':l_2}
			topic = "HAVERLAND/devs/htr/2/power_command"
			infot = mqttc.publish(topic, True, qos=0, retain=True)
		else:
			m_2 = "off"
			data = {'mode':'off','stemp':st_2,'units':units,'locked':l_2}
			topic = "HAVERLAND/devs/htr/2/power_command"
			infot = mqttc.publish(topic, False, qos=0, retain=True)
		try:
			topic = "HAVERLAND/devs/htr/2/mode_state"
			infot = mqttc.publish(topic, m_2, qos=0, retain=True)
			data = json.dumps(data)
			response = requests.post(url, data=data, headers=headers)
			r = response.json()
			if response.status_code == 201:
				print(str(response.status_code) + " (mode_command_2) POST SUCCESSFUL")
				get_status('2')
			elif response.status_code == 401:
				print(str(response.status_code) + " (mode_command_2) POST FAILED " + r['error']['desc'])
			else:
				print(str(response.status_code) + " POST unknown")
		except KeyError:
			print('Caught KeyError mode_command_2')
			print(r['error'])
	elif msg.topic == "HAVERLAND/devs/htr/3/mode_command":
		topic = "HAVERLAND/devs/htr/3/mode_state"
		url = "https://api-haverland.helki.com/api/v2/devs/{your_device_id}/htr/3/status"
		infot = mqttc.publish(topic, x, qos=0, retain=True)
		if x == "heat":
			m_3 = "manual"
			data = {'mode':'manual','stemp':st_3,'units':units,'locked':l_3}
			topic = "HAVERLAND/devs/htr/3/power_command"
			infot = mqttc.publish(topic, True, qos=0, retain=True)
		elif x == "auto":
			m_3 = "modified_auto"
			data = {'mode':'modified_auto','stemp':st_3,'units':units,'locked':l_3}
			topic = "HAVERLAND/devs/htr/3/power_command"
			infot = mqttc.publish(topic, True, qos=0, retain=True)
		else:
			m_3 = "off"
			data = {'mode':'off','stemp':st_3,'units':units,'locked':l_3}
			topic = "HAVERLAND/devs/htr/3/power_command"
			infot = mqttc.publish(topic, False, qos=0, retain=True)
		try:
			topic = "HAVERLAND/devs/htr/3/mode_state"
			infot = mqttc.publish(topic, m_3, qos=0, retain=True)
			data = json.dumps(data)
			response = requests.post(url, data=data, headers=headers)
			r = response.json()
			if response.status_code == 201:
				print(str(response.status_code) + " (mode_command_3) POST SUCCESSFUL")
				get_status('3')
			elif response.status_code == 401:
				print(str(response.status_code) + " (mode_command_3) POST FAILED " + r['error']['desc'])
			else:
				print(str(response.status_code) + " POST unknown")
		except KeyError:
			print('Caught KeyError mode_command_3')
			print(r['error'])
	elif msg.topic == "HAVERLAND/devs/htr/2/temperature_command":
		url = "https://api-haverland.helki.com/api/v2/devs/{your_device_id}/htr/2/status"
		st_2 = x
		try:
			data = {'mode':m_2,'stemp':st_2,'units':units,'locked':l_2}
			data = json.dumps(data)
			response = requests.post(url, data=data, headers=headers)
			r = response.json()
			if response.status_code == 201:
				print(str(response.status_code) + " (temperature_command_2) POST SUCCESSFUL")
				get_status('2')
			elif response.status_code == 401:
				print(str(response.status_code) + " (temperature_command_2) POST FAILED " + r['error']['desc'])
			else:
				print(str(response.status_code) + " POST unknown")
		except KeyError:
			print('Caught KeyError temperature_command_2')
			print(r['error'])
	elif msg.topic == "HAVERLAND/devs/htr/3/temperature_command":
		url = "https://api-haverland.helki.com/api/v2/devs/{your_device_id}/htr/3/status"
		st_3 = x
		try:
			data = {'mode':m_3,'stemp':st_3,'units':units,'locked':l_3}
			data = json.dumps(data)
			response = requests.post(url, data=data, headers=headers)
			r = response.json()
			if response.status_code == 201:
				print(str(response.status_code) + " (temperature_command_3) POST SUCCESSFUL")
				get_status('3')
			elif response.status_code == 401:
				print(str(response.status_code) + " (temperature_command_3) POST FAILED " + r['error']['desc'])
			else:
				print(str(response.status_code) + " POST unknown")
		except KeyError:
			print('Caught KeyError temperature_command_3')
			print(r['error'])
	elif msg.topic == "HAVERLAND/devs/htr/2/lock_command":
		url = "https://api-haverland.helki.com/api/v2/devs/{your_device_id}/htr/2/status"
		if x == "True":
			l_2 = 'true'
		else:
			l_2 = 'false'
		try:
			data = "{\"locked\":" + l_2 +"}"
			response = requests.post(url, data=data, headers=headers)
			r = response.json()
			if response.status_code == 201:
				print(str(response.status_code) + " (lock_command_2) POST SUCCESSFUL")
				get_status('2')
			elif response.status_code == 401:
				print(str(response.status_code) + " (lock_command_2) POST FAILED " + r['error']['desc'])
			else:
				print(str(response.status_code) + " POST unknown")
		except KeyError:
			print('Caught KeyError lock_command_2')
			print(r['error'])
	elif msg.topic == "HAVERLAND/devs/htr/3/lock_command":
		url = "https://api-haverland.helki.com/api/v2/devs/{your_device_id}/htr/3/status"
		if x == "True":
			l_3 = 'true'
		else:
			l_3 = 'false'
		try:
			data = "{\"locked\":" + l_3 +"}"
			response = requests.post(url, data=data, headers=headers)
			r = response.json()
			if response.status_code == 201:
				print(str(response.status_code) + " (lock_command_3) POST SUCCESSFUL")
				get_status('3')
			elif response.status_code == 401:
				print(str(response.status_code) + " (lock_command_3) POST FAILED " + r['error']['desc'])
			else:
				print(str(response.status_code) + " POST unknown")
		except KeyError:
			print('Caught KeyError lock_command_3')
			print(r['error'])
	elif msg.topic == "HAVERLAND/devs/htr/2/true_radiant_command":
		url = "https://api-haverland.helki.com/api/v2/devs/{your_device_id}/htr/2/setup"
		if x == "True":
			tr_2 = 'true'
		else:
			tr_2 = 'false'
		try:
			data = "{\"control_mode\":6,\"units\":\"" + units + "\",\"power\":\"1200.0\",\"offset\":\"0.0\",\"priority\":\"" + rp_2 + "\",\"away_mode\":0,\"away_offset\":\"" + ao_2 + "\",\"modified_auto_span\":0,\"window_mode_enabled\":" + wm_2 + ",\"true_radiant_enabled\":" + tr_2 + "}"
			response = requests.post(url, data=data, headers=headers)
			r = response.json()
			if response.status_code == 201:
				print(str(response.status_code) + " (true_radiant_command_2) POST SUCCESSFUL")
				get_setup('2')
			elif response.status_code == 401:
				print(str(response.status_code) + " (true_radiant_command_2) POST FAILED " + r['error']['desc'])
			else:
				print(str(response.status_code) + " POST unknown")
		except KeyError:
			print('Caught KeyError true_radiant_command_2')
			print(r['error'])
	elif msg.topic == "HAVERLAND/devs/htr/3/true_radiant_command":
		url = "https://api-haverland.helki.com/api/v2/devs/{your_device_id}/htr/3/setup"
		if x == "True":
			tr_3 = 'true'
		else:
			tr_3 = 'false'
		try:
			data = "{\"control_mode\":6,\"units\":\"" + units + "\",\"power\":\"900.0\",\"offset\":\"0.0\",\"priority\":\"" + rp_3 + "\",\"away_mode\":0,\"away_offset\":\"" + ao_3 + "\",\"modified_auto_span\":0,\"window_mode_enabled\":" + wm_3 + ",\"true_radiant_enabled\":" + tr_3 + "}"
			response = requests.post(url, data=data, headers=headers)
			r = response.json()
			if response.status_code == 201:
				print(str(response.status_code) + " (true_radiant_command_3) POST SUCCESSFUL")
				get_setup('3')
			elif response.status_code == 401:
				print(str(response.status_code) + " (true_radiant_command_3) POST FAILED " + r['error']['desc'])
			else:
				print(str(response.status_code) + " POST unknown")
		except KeyError:
			print('Caught KeyError true_radiant_command_3')
			print(r['error'])
	elif msg.topic == "HAVERLAND/devs/htr/2/window_mode_command":
		url = "https://api-haverland.helki.com/api/v2/devs/{your_device_id}/htr/2/setup"
		if x == "True":
			wm_2 = 'true'
		else:
			wm_2 = 'false'
		try:
			data = "{\"control_mode\":6,\"units\":\"" + units + "\",\"power\":\"1200.0\",\"offset\":\"0.0\",\"priority\":\"" + rp_2 + "\",\"away_mode\":0,\"away_offset\":\"" + ao_2 + "\",\"modified_auto_span\":0,\"window_mode_enabled\":" + wm_2 + ",\"true_radiant_enabled\":" + tr_2 + "}"
			response = requests.post(url, data=data, headers=headers)
			r = response.json()
			if response.status_code == 201:
				print(str(response.status_code) + " (window_mode_command_2) POST SUCCESSFUL")
				get_setup('2')
			elif response.status_code == 401:
				print(str(response.status_code) + " (window_mode_command_2) POST FAILED " + r['error']['desc'])
			else:
				print(str(response.status_code) + " POST unknown")
		except KeyError:
			print('Caught KeyError window_mode_command_2')
			print(r['error'])
	elif msg.topic == "HAVERLAND/devs/htr/3/window_mode_command":
		url = "https://api-haverland.helki.com/api/v2/devs/{your_device_id}/htr/3/setup"
		if x == "True":
			wm_3 = 'true'
		else:
			wm_3 = 'false'
		try:
			data = "{\"control_mode\":6,\"units\":\"" + units + "\",\"power\":\"900.0\",\"offset\":\"0.0\",\"priority\":\"" + rp_3 + "\",\"away_mode\":0,\"away_offset\":\"" + ao_3 + "\",\"modified_auto_span\":0,\"window_mode_enabled\":" + wm_3 + ",\"true_radiant_enabled\":" + tr_3 + "}"
			response = requests.post(url, data=data, headers=headers)
			r = response.json()
			if response.status_code == 201:
				print(str(response.status_code) + " (window_mode_command_3) POST SUCCESSFUL")
				get_setup('3')
			elif response.status_code == 401:
				print(str(response.status_code) + " (window_mode_command_3) POST FAILED " + r['error']['desc'])
			else:
				print(str(response.status_code) + " POST unknown")
		except KeyError:
			print('Caught KeyError window_mode_command_3')
			print(r['error'])
	elif msg.topic == "HAVERLAND/devs/htr/2/away_offset_command":
		url = "https://api-haverland.helki.com/api/v2/devs/{your_device_id}/htr/2/setup"
		ao_2 = str(x)
		try:
			data = "{\"control_mode\":6,\"units\":\"" + units + "\",\"power\":\"1200.0\",\"offset\":\"0.0\",\"priority\":\"" + rp_2 + "\",\"away_mode\":0,\"away_offset\":\"" + ao_2 + "\",\"modified_auto_span\":0,\"window_mode_enabled\":" + wm_2 + ",\"true_radiant_enabled\":" + tr_2 + "}"
			response = requests.post(url, data=data, headers=headers)
			response = requests.post(url, data=data, headers=headers)
			r = response.json()
			if response.status_code == 201:
				print(str(response.status_code) + " (away_offset_command_2) POST SUCCESSFUL")
				get_setup('2')
			elif response.status_code == 401:
				print(str(response.status_code) + " (away_offset_command_2) POST FAILED " + r['error']['desc'])
			else:
				print(str(response.status_code) + " POST unknown")
		except KeyError:
			print('Caught KeyError away_offset_command_2')
			print(r['error'])
	elif msg.topic == "HAVERLAND/devs/htr/3/away_offset_command":
		url = "https://api-haverland.helki.com/api/v2/devs/{your_device_id}/htr/3/setup"
		ao_3 = str(x)
		try:
			data = "{\"control_mode\":6,\"units\":\"" + units + "\",\"power\":\"900.0\",\"offset\":\"0.0\",\"priority\":\"" + rp_3 + "\",\"away_mode\":0,\"away_offset\":\"" + ao_3 + "\",\"modified_auto_span\":0,\"window_mode_enabled\":" + wm_3 + ",\"true_radiant_enabled\":" + tr_3 + "}"
			response = requests.post(url, data=data, headers=headers)
			r = response.json()
			if response.status_code == 201:
				print(str(response.status_code) + " (away_offset_command_3) POST SUCCESSFUL")
				get_setup('3')
			elif response.status_code == 401:
				print(str(response.status_code) + " (away_offset_command_3) POST FAILED " + r['error']['desc'])
			else:
				print(str(response.status_code) + " POST unknown")
		except KeyError:
			print('Caught KeyError away_offset_command_3')
			print(r['error'])
	elif msg.topic == "HAVERLAND/devs/htr/2/radiator_priority_command":
		url = "https://api-haverland.helki.com/api/v2/devs/{your_device_id}/htr/2/setup"
		rp_2 = x
		try:
			data = "{\"control_mode\":6,\"units\":\"" + units + "\",\"power\":\"1200.0\",\"offset\":\"0.0\",\"priority\":\"" + rp_2 + "\",\"away_mode\":0,\"away_offset\":\"" + ao_2 + "\",\"modified_auto_span\":0,\"window_mode_enabled\":" + wm_2 + ",\"true_radiant_enabled\":" + tr_2 + "}"
			response = requests.post(url, data=data, headers=headers)
			r = response.json()
			if response.status_code == 201:
				print(str(response.status_code) + " (radiator_priority_command_2) POST SUCCESSFUL")
				get_setup('2')
			elif response.status_code == 401:
				print(str(response.status_code) + " (radiator_priority_command_2) POST FAILED " + r['error']['desc'])
			else:
				print(str(response.status_code) + " POST unknown")
		except KeyError:
			print('Caught KeyError radiator_priority_command_2')
			print(r['error'])
	elif msg.topic == "HAVERLAND/devs/htr/3/radiator_priority_command":
		url = "https://api-haverland.helki.com/api/v2/devs/{your_device_id}/htr/3/setup"
		rp_3 = x
		try:
			data = "{\"control_mode\":6,\"units\":\"" + units + "\",\"power\":\"900.0\",\"offset\":\"0.0\",\"priority\":\"" + rp_3 + "\",\"away_mode\":0,\"away_offset\":\"" + ao_3 + "\",\"modified_auto_span\":0,\"window_mode_enabled\":" + wm_3 + ",\"true_radiant_enabled\":" + tr_3 + "}"
			response = requests.post(url, data=data, headers=headers)
			r = response.json()
			if response.status_code == 201:
				print(str(response.status_code) + " (radiator_priority_command_3) POST SUCCESSFUL")
				get_setup('3')
			elif response.status_code == 401:
				print(str(response.status_code) + " (radiator_priority_command_3) POST FAILED " + r['error']['desc'])
			else:
				print(str(response.status_code) + " POST unknown")
		except KeyError:
			print('Caught KeyError radiator_priority_command_3')
			print(r['error'])
	elif msg.topic == "HAVERLAND/away_command":
		url = "https://api-haverland.helki.com/api/v2/devs/{your_device_id}/mgr/away_status"
		if x == "True":
			away = 'true'
		else:
			away = 'false'
		try:
			data = "{\"away\":" + away + ",\"enabled\":" + away_enabled + "}"
			response = requests.post(url, data=data, headers=headers)
			r = response.json()
			if response.status_code == 201:
				print(str(response.status_code) + " (away_status) POST SUCCESSFUL")
				get_away()
			elif response.status_code == 401:
				print(str(response.status_code) + " (away_status) POST FAILED " + r['error']['desc'])
			else:
				print(str(response.status_code) + " POST unknown")
		except KeyError:
			print('Caught KeyError away_status')
			print(r['error'])

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

def get_devs():
	global dev_id
	url = api_url
	response = requests.get(url, data=data, headers=headers)
	r = response.json()
	try:
		p = r['devs'][0]
		dev_id = r['devs'][0]['dev_id']
		d = json.dumps(p)
		infot = mqttc.publish(haverland_devs_topic, d, qos=0, retain=True)
	except KeyError:
		print ('Caught KeyError')
		print(r['error'])
	return 1

def get_away():
	url = away_url
	response = requests.get(url, data=data, headers=headers)
	r = response.json()
	try:
		d = json.dumps(r)
		infot = mqttc.publish(haverland_away_topic, d, qos=0, retain=True)
	except KeyError:
		print ('Caught KeyError get_away')
		print(r['error'])
	return 1

def get_plimit():
	url = plimit_url
	response = requests.get(url, data=data, headers=headers)
	r = response.json()
	try:
		d = json.dumps(r)
		infot = mqttc.publish(haverland_plimit_topic, d, qos=0, retain=True)
	except KeyError:
		print ('Caught KeyError get_plimit')
		print(r['error'])
	return 1

def get_nodes():
	url = node_url
	response = requests.get(url, data=data, headers=headers)
	r = response.json()
	try:
		p = r['nodes'][0]
		q = r['nodes'][1]
		d1 = json.dumps(p)
		d2 = json.dumps(q)
		topic = haverland_nodes_topic + "/2"
		infot = mqttc.publish(topic, d1, qos=0, retain=True)
		topic = haverland_nodes_topic + "/3"
		infot = mqttc.publish(topic, d2, qos=0, retain=True)
	except KeyError:
		print ('Caught KeyError get_nodes')
		print(r['error'])
	return 1

def get_status(addr):
	url = dev_url + "/htr/" + addr + "/status"
	topic = haverland_heater_topic + "/" + addr + "/status"
	response = requests.get(url, data=data, headers=headers)
	r = response.json()
	print("Refresh status " + addr + "...")
	try:
		d = json.dumps(r)
		infot = mqttc.publish(topic, d, qos=0, retain=True)
	except KeyError:
		print ('Caught KeyError get_status')
		print(r['error'])
	return 1

def get_setup(addr):
	url = dev_url + "/htr/" + addr + "/setup"
	topic = haverland_heater_topic + "/" + addr + "/setup"
	response = requests.get(url, data=data, headers=headers)
	r = response.json()
	print("Setting up " + addr + "...")
	try:
		d = json.dumps(r)
		infot = mqttc.publish(topic, d, qos=0, retain=True)
	except KeyError:
		print ('Caught KeyError get_setup')
		print(r['error'])
	return 1

def get_token():
	global 	token_url, token_data, token_headers, access_token, refresh_token, expires_in, t, headers
	response = requests.post(token_url, data=token_data, headers=token_headers)
	r = json.loads(response.text)
	t = round(time.time(),0) - 600
	access_token = r["access_token"]
	refresh_token = r["refresh_token"]
	expires_in = r["expires_in"]
	headers = {"Authorization": "Bearer "+access_token, "Accept": "application/json, text/plain, */*", 
	"content-type": "application/json"}
	return 1

# GET tokens
username = "{your_username}"
password = "{your_password}"
token_data = 'grant_type=password&username=' + username + '&password=' + password
token_headers = {'authorization':'Basic NTU2ZDc0MWI3OGUzYmU5YjU2NjA3NTQ4OnZkaXZkaQ==','Content-Type':'application/x-www-form-urlencoded','Accept':'application/json, text/plain, */*'}
r = ""
t = 0
access_token = ""
refresh_token = ""
expires_in = 0
headers = {""}

get_token()

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.connect("localhost", 1883, 60)

# GET Haverland data
get_devs()

dev_url = api_url + "/" + dev_id
node_url = dev_url + "/mgr/nodes"
away_url = dev_url + "/mgr/away_status"
plimit_url = dev_url + "/htr_system/power_limit"

get_away()
get_plimit()
get_nodes()

# GET Heater data
get_status('2')
get_setup('2')

get_status('3')
get_setup('3')

mqttc.subscribe([("HAVERLAND/devs/htr/2/mode_command",0),
("HAVERLAND/devs/htr/3/mode_command",0),
("HAVERLAND/devs/htr/2/temperature_command",0),
("HAVERLAND/devs/htr/3/temperature_command",0),
("HAVERLAND/devs/htr/2/lock_command",0),
("HAVERLAND/devs/htr/3/lock_command",0),
("HAVERLAND/devs/htr/2/true_radiant_command",0),
("HAVERLAND/devs/htr/3/true_radiant_command",0),
("HAVERLAND/devs/htr/2/window_mode_command",0),
("HAVERLAND/devs/htr/3/window_mode_command",0),
("HAVERLAND/devs/htr/2/away_offset_command",0),
("HAVERLAND/devs/htr/3/away_offset_command",0),
("HAVERLAND/devs/htr/2/radiator_priority_command",0),
("HAVERLAND/devs/htr/3/radiator_priority_command",0),
("HAVERLAND/away_command",0)
])


mqttc.loop_forever()
#mqttc.loop_start()


mqttc.disconnect()
