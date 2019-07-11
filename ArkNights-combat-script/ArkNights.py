import os
import pytesseract
from PIL import Image
import time
import json

pytesseract.pytesseract.tesseract_cmd = 'C://Program Files (x86)/Tesseract-OCR/tesseract.exe'
adb_host = "127.0.0.1"
adb_port = "7555"

def get_filenum():
	filelist = os.listdir('./image')
	if filelist:
		filenum = filelist[-1].split('.')[0]
		return int(filenum)
	else:
		filenum = 0
		return filenum
	
def connect_device():
	result = os.system('adb connect {host}:{port}'.format(host = adb_host, port = adb_port))
	if(result == 0):
		print("连接成功!")
		return 1
	else:
		print("连接失败,请检查是否开启模拟器或设备ip的正确性")
		return 0

def get_data(combat_num):
	with open('./data.json', 'r') as f:
		data = json.load(f)
		f.close()
	if(combat_num in data):
		print("关卡数据存在")
		return data[combat_num]['time']
	else:
		print("关卡数据不存在")
		return 0

def write_json(combat_num, used_time):
	with open('./data.json', 'r') as f:
		data = json.load(f)
		f.close()
	new_data = {combat_num:{'time':used_time}}
	new_data = dict(data, **new_data)
	with open('./data.json', 'w') as f:
		try:
			json.dump(new_data, f)
			f.close()
			print("记录数据成功")
		except:
			print("记录数据失败")

def script(combat_num):
	combat_time = get_data(combat_num)

	os.system('adb shell input tap 1381 731')
	time.sleep(3)
	os.system('adb shell input tap 1242 453')
	start = time.time()
	if(combat_time == 0):
		pass
	else:
		print("脚本正在运行")
		time.sleep(combat_time*0.9)
	while True:
		os.system('adb shell screencap /sdcard/screenshot.png')
		os.system('adb pull /sdcard/screenshot.png ./screencap/screenshot.png')
		img = Image.open('./screencap/screenshot.png')
		img = img.crop((41,643,450,770)).convert('1')
		img.convert('L')
		text = pytesseract.image_to_string(img,lang='chi_sim')
		#print(text)
		if(text == '行 动 结 束'):
			filenum = get_filenum()
			img.save('./image/%s.jpg'%str(filenum+1))
			end = time.time()
			used_time = end-start
			if(combat_time == 0):
				write_json(combat_num, used_time)
			print("本次行动结束，用时{:.2f}秒".format(used_time))
			os.system('adb shell input tap 1242 453')
			break

if __name__ == '__main__':
	if(connect_device()):
		combat_num = input("请输入关卡：")
		epoch = input("输入作战次数：")
		epoch = int(epoch)
		for i in range(epoch):
			script(combat_num)
			print("已完成%d次战斗，剩余%d次战斗"%(i+1, epoch-i-1))
			time.sleep(3)
		print("脚本运行结束，感谢各位博士的使用")
		#print("后续功能可能会有：\n识别战斗获得物品并自动计数\n设置需要的物资数量，在理智充足时自动战斗至相应的物资数量")
