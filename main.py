from datetime import datetime
import pickle
import time
import os
from glob import glob
from colorama import init, Fore,Style

class Item:
	def __init__(self,model,memory,price,color,link):
		self.model = model
		self.memory = memory
		self.price = price
		self.color = color
		self.link = link


def convert_time_to_name():
	now = datetime.now()
	return f'YEAR{now.year}MONTH{now.month}DAY{now.day}HOUR{now.hour}MIN{now.minute}SEC{now.second}'

	
def parse_model(i,string):
	model = ''
	i+=6
	while(string[i] != ','):
		model+=string[i]
		i+=1
	return model


def parse_memory(i,string):
	memory = ''
	i -= 1
	while(string[i] != ' '):
		memory += string[i]
		i -= 1
	return int(memory[::-1])


def parse_price(i,string):
	price = ''
	i+=6
	while(string[i] != '"'):
		price += string[i]
		i += 1
	price = float(price.replace(",",""))
	return price


def parse_color(i,string):
	color = ''
	flag = 0
	while(string[i] != '-'):
		if string[i] == '|':
			flag = 1
		if flag == 1:
			color += string[i]
		i += 1
	color = color[2:-1]
	return color


def parse_link(i,string):
	link = 'https://www.mp3.sk/'
	i += 5
	while(string[i] != '"'):
		link += string[i]
		i += 1
	return link


def get_data(page_number,arr_phones):
	html = open("html","r").read().replace("PAGE_NUMBER",str(page_number))

	command = "curl {} > website".format(html)
	# print("XXX")
	os.system(command)
	raw_data = open("website","r").read().split("f_back")[0]
	# print(raw_data)
	arr = raw_data.split("kkk")

	for index,value in enumerate(arr):
		if "novy" in value and "Watch" not in value:
			model = parse_model(value.index("Apple"),value)
			memory = parse_memory(value.index("GB"),value)
			price = parse_price(value.index("fPr\":\""),value)
			color = parse_color(value.index("|"),value)
			link = parse_link(value.index("\"u\":\""),value)
			arr_phones.append(Item(model,memory,price,color,link))


def write(arr_phones):
	arr_phones = sorted(arr_phones, key = lambda item: (item.price,item.color))
	date = datetime.now()
	filename = '{}-{:02d}-{:02d}-{:02d}-{:02d}-{:02d}'.format(date.year,date.month,date.day,date.hour,date.minute,date.second)
	# print(filename)
	f = open(f'datums/{filename}','wb')
	pickle.dump(len(arr_phones),f)
	for i,item in enumerate(arr_phones):
		# print('x')
		# print('{:<25s}{:>3s}GB {:>7s}€ {:>15s} {}'.format(item.model,str(item.memory),str(item.price),item.color,item.link))
		# print('{:<18s}{:>3s}GB {:>7s}€ {:>14s}'.format(item.model,str(item.memory),str(item.price),item.color))
		# os.system(f"google-chrome {item.link}")
		# f.write('{:<25s}{:>3s}GB {:>7s}€ {:>15s} {}\n'.format(item.model,str(item.memory),str(item.price),item.color,item.link))
		pickle.dump(item,f)
	f.close()

def load(filename):
	if filename == 0:
		os.system('cd datums/; ls -t | head -1 > ../last_datum')
		filename = open('last_datum','r').read()[:-1]

	f = open(f'datums/{filename}','rb')
	n = pickle.load(f)
	a = []
	for i in range(n):
		a.append(pickle.load(f))
		item = a[-1]
		print('{:<25s}{:>3s}GB {:>7s}€ {:>15s} {}'.format(item.model,str(item.memory),str(item.price),item.color,item.link))
	return a

def compare():
	missing = []
	os.system('clear')
	filename = sorted(glob("datums/*"))
	if len(filename) > 1:
		file_new = filename[-1]
		file_pre = filename[-2]
	else:
		load(0)
		return

	a_pre = []
	f = open(file_pre,'rb')
	n = pickle.load(f)
	for i in range(n):
		a_pre.append(pickle.load(f))
	
	a_new = []
	f = open(file_new,'rb')
	n = pickle.load(f)
	for i in range(n):
		a_new.append(pickle.load(f))

	for indexi,i in enumerate(a_new):
		count = 0
		for indexj,j in enumerate(a_pre):
			a = f'{i.model},{i.memory},{i.price},{i.color}'
			b = f'{j.model},{j.memory},{j.price},{j.color}'
			if a == b:
				break
			else:
				count += 1
		if count == len(a_pre):
			missing.append(indexi)

	for i,item in enumerate(a_new):
		if i in missing:
			print(Style.BRIGHT + Fore.GREEN + '{:<25s}{:>3s}GB {:>7s}€ {:>15s} {}'.format(item.model,str(item.memory),str(item.price),item.color,item.link))
		else:
			print('{:<25s}{:>3s}GB {:>7s}€ {:>15s} {}'.format(item.model,str(item.memory),str(item.price),item.color,item.link))			

def beta(model,memory,color):
	filename = open('all_datums','r').readlines()
	bucket = []
	for i in filename:
		i = i[:-1]
		a = load(i)
		for j in a:
			if (model,memory,color) == (j.model,j.memory,j.color):
				bucket.append([j,i])

	os.system("clear")
	for item,datum in bucket:
		print('{:<25s}{:>3s}GB {:>7s}€ {:>15s} {}'.format(item.model,str(item.memory),str(item.price),item.color,item.link))
		print(datum)			



def main():
	init(autoreset=True)

	print("TODAY DATA [0]	LAST DATA [1]	SPECIFIC DATUM [2]   BETA [3]")
	number = int(input("ENTER NUMBER: "))

	if number == 0:
		arr_phones = []
		for page in range(1,10):
			get_data(page,arr_phones)
		write(arr_phones)
		compare()
	if number == 1:
		os.system("clear")
		load(0)
	if number == 2:
		os.system("clear")
		os.system("cd datums/; ls -t")
		datum = input("ENTER DATUM: ")
		os.system("clear")
		load(datum)
	if number == 3:
		beta('iPhone 11 Pro',64,'Space Gray')

main()