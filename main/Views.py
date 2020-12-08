from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .models import *
import json


def current_user(sess, request):
		sess['user_login']=request.session['user_login']
		sess['user_group']=request.session['user_group']

	

def home(request):
	database = DataBase()
	with open('main/data/package.json', 'r', encoding="utf-8") as file:
		text = json.loads(file.read())
	data = text["orders"]
	session = {}
	try:
		current_user(session, request)
	except:
		print("We've got a bad news, sir")
		return redirect('auth')
	if request.method == "POST":
		current_user(session, request)

	session['title'] = 'Заказы'
	session['orders'] = data
	return render(request, 'main/home.html', session)

def auth(request):
	data = DataBase()
	if request.method == "POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			user_login = request.POST['login']
			user_pass = request.POST['password']
			current_u = data.users.auth(user_login, user_pass)
			try:
				if current_u.group == "Заблокирован":
					messages.error(request, f'Вы заблокированы в системе')
				else:
					request.session['user_login'] = current_u.username
					request.session['user_group'] = current_u.group
					return redirect('home')
			except:
				messages.error(request, f'Неверный логин и/или пароль!')
		else: print("Invalid form!")
	else: 
		try: 
			if request.session['user_login']: return redirect('home')
		except: form = LoginForm()
	return render(request, "main/auth.html", {'form': form, 'title': 'Авторизация'})


def manage(request):
	try:

			session = {}
			try:
				current_user(session, request)
			except:
				print("Sounds bad")
			session['title'] = 'Управление заказами'
			data = DataBase()
			users = data.users.get_list()
			orders = data.orders.get_list()
			session["users"] = users["users"]
			session["orders"] = orders["orders"]
			if request.method == "POST":
				form = CreationForm(request.POST)

				if "save" in request.POST.keys():
					if data.orders.create_order(request.POST["info"],request.session['user_login'],request.POST["expecting"]):
						messages.success(request, f'Заказ успешно добавлен!')
					else:
						messages.error(request, f'Такое имя уже занято!')
					session = data.users.get_list()
					return redirect('manage')
				elif "delete" in request.POST.keys():
					data.orders.delete_order(int(request.POST["delete"]))
					session = data.orders.get_list()
				elif "accept" in request.POST.keys():
					data.orders.change_status(int(request.POST["accept"]),"На обработке",request.session['user_login'])
					session = data.orders.get_list()

			else:
				form = CreationForm()
			session = data.orders.get_list()
			session['title'] = 'Управление заказами'
			try:
				current_user(session, request)
			except:
				print("Sounds bad!")
			session['form'] = form

	except:
		return redirect('home')
	return render(request, "main/manage.html", session)

def manageorg(request):
	try:
		if request.session['user_group'] == "Модератор":
			session = {}
			try:
				current_user(session, request)
			except:
				print("Sounds bad")
			session['title'] = 'Управление организациями'
			data = DataBase()
			users = data.users.get_list()
			orgs = data.orgs.get_list()
			session["users"] = users["users"]
			session["orgs"] = orgs["orgs"]
			if request.method == "POST":
				form = OrgAddingForm(request.POST)

				if "save" in request.POST.keys():
					if data.orgs.create_org(request.POST["name"],request.POST["date"],request.POST["dirname"],request.POST["dob"]):
						messages.success(request, f'Организация успешно добавлена!')
					else:
						messages.error(request, f'Такое имя уже занято!')
					session = data.orgs.get_list()
					return redirect('manage')
				elif "delete" in request.POST.keys():
					data.orgs.delete_org(int(request.POST["delete"]))
					session = data.orgs.get_list()

			else:
				form = OrgAddingForm()
			session = data.orgs.get_list()
			session['title'] = 'Управление организациями'
			try:
				current_user(session, request)
			except:
				print("Sounds bad!")
			session['form'] = form
		else:
			return redirect('home')
	except:
		return redirect('home')
	return render(request, "main/manageorg.html", session)

def taskoforg(request):
	try:
		if request.session['user_group'] == "Модератор" or request.session['user_group'] == "Организация":
			session = {}
			try:
				current_user(session, request)
			except:
				print("Sounds bad")
			session['title'] = 'Задачи организации'
			data = DataBase()
			users = data.users.get_list()
			if request.GET.get('name'):
				orders = data.orders.get_too(request.GET["name"])
			if "decline" in request.POST.keys():
				data.orders.change_status(int(request.POST["decline"]),"Свободен",-1)
				session = data.orders.get_list()
			session["users"] = users["users"]
			session["orders"] = orders["orders"]
			if "ready" in request.POST.keys():
				data.orders.change_status(int(request.POST["ready"]),"Заказ выполнен",-1)
				session = data.orders.get_list()
			session["users"] = users["users"]
			session["orders"] = orders["orders"]


			session['title'] = 'Управление организациями'
			try:
				current_user(session, request)
			except:
				print("Sounds bad!")
		else:
			return redirect('home')
	except:
		return redirect('home')
	return render(request, "main/tasksoforg.html", session)

def usersadm(request):
	try:
		if request.session['user_group'] == "Модератор":
			session = {}
			try:
				current_user(session, request)
			except:
				print("Sounds bad")
			session['title'] = 'Управление пользователями'
			data = DataBase()
			users = data.users.get_list()
			session["users"] = users["users"]
			if request.method == "POST":
				form = UserAddingForm(request.POST)
				if "org" in request.POST.keys():
					user_update = request.POST.get("org")
					data.users.new_group(user_update, "Организация")
					if user_update == session['user_login']: request.session['user_group'] = "Организация"
					if request.session['user_group'] != "Модератор": return redirect('home')
				elif 'zakazchik' in request.POST.keys():
					user_update = request.POST.get("zakazchik")
					data.users.new_group(user_update, "Заказчик")
					if user_update == session['user_login']: request.session['user_group'] = "Заказчик"
					if request.session['user_group'] != "Модератор": return redirect('home')
				elif "give_moderator" in request.POST.keys():
					user_update = request.POST.get("give_moderator")
					data.users.new_group(user_update, "Модератор")
					if request.session['user_group'] != "Модератор": return redirect('home')
				elif "lock" in request.POST.keys():
					user_update = request.POST.get("lock")
					data.users.new_group(user_update, "Заблокирован")
					if request.session['user_group'] != "Модератор": return redirect('home')
				elif "unlock" in request.POST.keys():
					user_update = request.POST.get("unlock")
					data.users.new_group(user_update, "NULL")
					if request.session['user_group'] != "Модератор": return redirect('home')
				elif "save" in request.POST.keys():
					if data.users.create_user(request.POST['username'], request.POST['password'], request.POST['group']):
						messages.success(request, f'Пользователь ' + request.POST['username'] + ' успешно добавлен!')
					else: messages.error(request, f'Такое имя уже занято!')
					session = data.users.get_list()
					return redirect('manage')
				elif "delete" in request.POST.keys():
					data.users.delete_user(request.POST['delete'])
					session = data.users.get_list()

			else:
				form = UserAddingForm()
			session = data.users.get_list()
			session['title'] = 'Управление пользователями'
			try:
				current_user(session, request)
			except:
				print("Sounds bad!")
			session['form'] = form
		else:
			return redirect('home')
	except: return redirect('home')
	return render(request, "main/usersadm.html", session)

def exit(request):
	request.session.clear()
	return redirect('auth')