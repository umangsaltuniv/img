import glob
import requests
import json
import numpy as np
import time
import base64
import sys,os
import cv2
enable_pageid = True
goggle_ocr_url   = "https://byjuservernew.kritikalocr.com/internal_server/ocr/v6"
headers          = { 
                     'Content-Type':'application/json',
                     'Accept':'text/plain',
                     'API-KEY':'c960f-f558c-4457b-9a77c-4bd71'
                   }
def test_api(name):
	with open(name, "rb") as image_file:
	    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
	#json_string = json.dumps({"imgData": encoded_string,"retType":"plainstr" ,"pageId":yes"})
	data = {}
	data["imgData"] = encoded_string
	if enable_pageid:
		data['pageId'] = "yes"
	json_string = json.dumps(data)
	print("requesting api for ocr")
	res = requests.post(goggle_ocr_url, data=json_string, headers=headers)
	
	print("*********************************************************************")


	print("result obtained: ", res.content)
	return (res)

folder_path=sys.argv[1]
dest_path=os.path.join(os.getcwd(),"api_output")
if not os.path.exists(dest_path):
	os.makedirs(dest_path)

list_images=os.listdir(folder_path)
for image in list_images:
	print (image)
	t1=time.time()
	res=test_api(os.path.join(folder_path,image))
	#print (res['error_status'])
	print ("time taken = ",time.time()-t1)
	print (res)
	try:
		text=res.json()
	except Exception as e:
		print ("Json Empty for image : -", image)
		continue
	if text['error_status']==200 and ('page_id' in text.keys()):
		txt=text['text']
		if enable_pageid:
			pageId = text['page_id']
		print (txt)
		print ('page_id - ', pageId)
		print ('\n\n')
		name,_= os.path.splitext(image)
		name+=".txt"
		filename=os.path.join(dest_path,name)
		print(filename)
		with open(filename,"w+") as f:
			f.write(txt)
	else:
		print(text)
	# print (text)
	# if res.status_code is 200:
	# 	text=res.json()
	# 	# print (text['error_message'])
	# 	print (text['error_status'])
	# 	txt=text['text']
	# elif res.status_code is 500:
	# 	txt=''
	# 	print ("filename format is not supported")
	# else:
	# 	txt=''
	# 	print ("Connection error")
	
