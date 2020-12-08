from django.db import models
import json
import hashlib
import datetime

class DataBase:
	def __init__(self):
		self.users = Users()
		self.orders = Orders()
		self.orgs = Orgs()

class Org:
	def __init__(self, id, name, date, dirname, dob, orders):
		self.id = id
		self.name = name
		self.date = date
		self.dirname = dirname
		self.dob = dob
		self.orders = orders

class Orgs:
	def __init__(self):
		self.path = 'main/data/orgs.json'
		self.orgs = []
		self.load_js()
	def save(self):
		with open(self.path, 'w', encoding="utf-8") as file: json.dump(self.get_list(), file)
	def load_js(self):
		with open(self.path, 'r', encoding="utf-8") as file:
			text = json.loads(file.read())
			for each in text["orgs"]: self.orgs.append(
				Org(each["id"],each["name"],each["date"],each["dirname"],each["dob"],each["orders"]))

	def create_org(self, name, date, dirname, dob):
		ids = []
		orgs = self.get_list()["orgs"]
		for each in orgs: ids.append(each["id"])
		if len(ids) == 0:
			org_id = 0
		else:
			org_id = max(ids) + 1

		self.orgs.append(Org(org_id, name, date, dirname, dob, name))
		self.save()
		return True

	def get_list(self):
		data=[]
		for each in self.orgs:
			data.append({"id":each.id,"name":each.name,"date":each.date,"dirname":each.dirname,"dob":each.dob,"orders":each.orders})
		return {"orgs": data}

	def delete_org(self, id):
		for each in self.orgs:
			if each.id == id:
				self.orgs.remove(each)
				self.save()
				break

class Order:
	def __init__(self, id, info, author, sending, expecting, status, org):
		self.id = id
		self.info = info
		self.author = author
		self.sending = sending
		self.expecting = expecting
		self.status = status
		self.org = org

class Orders:
	def __init__(self):
		self.path = 'main/data/package.json'
		self.orders = []
		self.load_js()
	def save(self):
		with open(self.path, 'w', encoding="utf-8") as file: json.dump(self.get_list(), file)
	def load_js(self):
		with open(self.path, 'r', encoding="utf-8") as file:
			text = json.loads(file.read())
			for each in text["orders"]: self.orders.append(
				Order(each["id"], each["info"], each["author"], each["sending"], each["expecting"], each["status"], each["org"]))

	def create_order(self, info, author, expecting):
		ids = []

		orders = self.get_list()["orders"]
		for each in orders: ids.append(each["id"])
		today = datetime.datetime.today()
		sending = today.strftime("%d/%m/%Y %H:%M:%S")
		if len(ids) == 0:
			orders_id = 0
		else:
			orders_id = max(ids) + 1

			self.orders.append(Order(orders_id, info, author, sending, expecting, "свободен", -1))
			self.save()
			return True
	def get_list(self):
		data=[]
		for each in self.orders:
			data.append({"id": each.id, "info": each.info, "author": each.author, "sending": each.sending, "expecting": each.expecting,"status":each.status,"org":each.org})
		return {"orders": data}

	def get_too(self,name):
		data=[]
		for each in self.orders:
			if each.org == name:
				data.append({"id": each.id, "info": each.info, "author": each.author, "sending": each.sending, "expecting": each.expecting,"status":each.status,"org":each.org})
		return {"orders": data}

	def delete_order(self, id):
		for each in self.orders:
			if each.id == id:
				self.orders.remove(each)
				self.save()
				break

	def change_status(self,id,status,org):
		for each in self.orders:
			if each.id == id:
				each.status = status
				each.org = org
				self.save()
				return each.status




class User:
	def __init__(self, id, username, password, group, org):
		self.id = id
		self.username = username
		self.password = password
		self.group = group
		self.org = org

class Users:
	def __init__(self):
		self.path = 'main/data/users.json'
		self.users = []
		self.load_js()
	def save(self):
		with open(self.path, 'w', encoding="utf-8") as file: json.dump(self.get_list(), file)
	def load_js(self):
		with open(self.path, 'r', encoding="utf-8") as file:
			text = json.loads(file.read())
		for each in text["users"]: self.users.append(User(each["id"],each["username"],each["password"],each["group"],each["org"]))

	def auth(self, username, password):
		password = password[:int(len(password)/2)] + str("moder1") + password[int(len(password)/2):]
		byted = bytes(password, "utf-8")
		hashed = hashlib.sha1(byted)
		password = hashed.hexdigest()
		for user in self.users:
			if (user.username == username) and (user.password == password):
				return user

	def create_user(self, username, password, group):
		password = password[:int(len(password)/2)] + str("moder1") + password[int(len(password)/2):]
		byted = bytes(password, "utf-8")
		hashed = hashlib.sha1(byted)
		password = hashed.hexdigest()
		ids = []
		users = self.get_list()["users"]
		for each in users: ids.append(each["id"])
		if len(ids) == 0: user_id = 0
		else: user_id = max(ids)+1
		for each in self.users:
			if username == each.username:
				return False
		else:
			self.users.append(User(user_id, username, password, group, -1))
			self.save()
			return True
	def get_list(self):
		data=[]
		for each in self.users:
			data.append({"id": each.id, "username": each.username, "password": each.password, "group": each.group, "org": each.org})
		return {"users": data}

	def new_group(self, username, newGroup):
		for each in self.users:
			if each.username == username:
				each.group = newGroup
				self.save()
				return each.group
	def delete_user(self, username):
		for each in self.users:
			if each.username == username:
				self.users.remove(each)
				self.save()
				break
	def change_photo(self, photo, username):
		new_photo = '../media/' + str(photo)
		for each in self.users:
			if each.username == username:
				each.photo = new_photo
				self.save()
				return each.photo

class ImageDownload(models.Model):
	img = models.ImageField(upload_to='')

