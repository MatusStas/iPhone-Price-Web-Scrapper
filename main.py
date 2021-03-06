from datetime import datetime
import pickle
import time
import os
from glob import glob
from colorama import init, Fore,Style
from matplotlib import pyplot as plt


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


def return_price(elem):
    return elem[3]


def newLine():
	print()

def get_data(page_number,arr_phones):
	html = open("html","r").read().replace("PAGE_NUMBER",str(page_number))

	command = "curl {} > website".format(html)
	os.system(command)
	raw_data = open("website","r").read().split("f_back")[0]
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
	f = open(f'datums/{filename}','wb')
	pickle.dump(len(arr_phones),f)
	for i,item in enumerate(arr_phones):
		pickle.dump(item,f)
	f.close()


def load(filename,show):
	if filename == 0:
		os.system('cd datums/; ls -t | head -1 > ../last_datum')
		filename = open('last_datum','r').read()[:-1]

	f = open(f'datums/{filename}','rb')
	n = pickle.load(f)
	a = []
	for i in range(n):
		a.append(pickle.load(f))
		item = a[-1]
		if show != 0:
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
		load(0,1)
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


def graph():
	n = 0
	arr = load(0,0)
	temp = []
	number = []
	models = []
	os.system("ls datums/ > all_datums")
	filename = open('all_datums','r').readlines()
	for i in filename:
		i = i[:-1]
		a = load(i,0)
		for j in a:
			if (j.model,j.memory,j.color) not in models:
				models.append((j.model,j.memory,j.color))
				number.append(n)
				temp.append(j.price)
				n+=1

			else:
				index = models.index((j.model,j.memory,j.color))
				if j.price < temp[index]:
					temp[index] = j.price


	today = ["" for i in range(len(models))]
	newLine()
	for item in arr:
		if (item.model,item.memory,item.color) in models:
			index = models.index((item.model,item.memory,item.color))
			today[index] = "available"
	i = 0
	for index in range(len(temp)):
		models[index] += (temp[index],"")

	models = sorted(models, key = return_price)
	for model,memory,color,price,nothing in models:
		print('{:>2} {:<25s}{:>3s}GB {:>8} {:<15s} {:<2}'.format(number[i],model,str(memory),price,color,today[i]))
		i += 1


	newLine()
	n = int(input("ENTER NUMBER: "))
	model,memory,color,price, nothing = models[n]


	filename = open('all_datums','r').readlines()
	bucket = []
	for i in filename:
		i = i[:-1]
		a = load(i,0)
		for j in a:
			if (model,memory,color) == (j.model,j.memory,j.color):
				bucket.append([j,i])

	datums = []
	price = []
	for item,datum in bucket:
		new_datum = ".".join(datum.split("-")[0:3])
		datums.append(new_datum)
		price.append(item.price)

	plt.plot(datums,price)
	plt.xticks(rotation=90)
	plt.show()			


def main():
	init(autoreset=True)
	os.system("clear")

	while True:
		print("TODAY DATA [0]	LAST DATA [1]	SPECIFIC DATUM [2]   GRAPH [3]   EXIT [4]")
		number = int(input("ENTER NUMBER: "))


		if number == 0:
			arr_phones = []
			for page in range(1,10):
				get_data(page,arr_phones)
			write(arr_phones)
			compare()
			newLine()

		elif number == 1:
			os.system("clear")
			load(0,1)
			newLine()

		elif number == 2:
			os.system("clear")
			os.system("cd datums/; ls -t")
			datum = input("ENTER DATUM: ")
			os.system("clear")
			load(datum,1)
			
			newLine()
		elif number == 3:
			graph()
			newLine()
			
		else:
			exit()

if __name__ == "__main__":
	main()