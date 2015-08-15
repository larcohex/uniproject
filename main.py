import kivy
kivy.require('1.8.0')

# -------------------------- Imports --------------------------
import datetime
import re
from time import time
import os
import ast
import unicodedata
from os.path import dirname, join

from kivy.app import App

from kivy.core.window import Window

from kivy.clock import Clock

from kivy.graphics import *

from kivy.animation import Animation
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition, ShaderTransition, SlideTransition,  \
									SwapTransition, FadeTransition, WipeTransition, FallOutTransition, RiseInTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.listview import ListView
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox

from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty,	\
							ObjectProperty, DictProperty
import beeminderpy
import gettext
import json
import urllib, urllib2, cookielib
import requests

from kivy.properties import ListProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManagerException
from kivy.config import Config
from kivy.animation import Animation
from kivy.uix.vkeyboard import VKeyboard
# -------------------------------------------------------------



# TODO: change to full screen in the end
Config.set ("graphics", "height", "320")
Config.set ("graphics", "width", "480")
Config.set ("graphics", "resizable", "0")
Config.write()



# -------------------------------------------------------------

def getTheme():
	try:
		with open ("cookies/settings.cookie", "r") as content_file:
			settings = content_file.read()
		settings = ast.literal_eval (settings)
		return settings["theme"]
	except IOError:
		return "Dark"

def monthString (n):
	if n == 1:
		return "January"
	elif n == 2:
		return "February"
	elif n == 3:
		return "March"
	elif n == 4:
		return "April"
	elif n == 5:
		return "May"
	elif n == 6:
		return "June"
	elif n == 7:
		return "July"
	elif n == 8:
		return "August"
	elif n == 9:
		return "September"
	elif n == 10:
		return "October"
	elif n == 11:
		return "November"
	elif n == 12:
		return "December"


def getDaysInMonth (month, year):
	if month == "Jan" or month == "Mar" or month == "May" or month == "Jul" or month == "Aug" or month == "Oct" or month == "Dec":
		return 31
	elif month == "Apr" or month == "Jun" or month == "Sep" or month == "Nov":
		return 30
	else:
		if int (year) % 4 == 0:
			return 29
		else:
			return 28


def parseDelta (s):
	diff = s.split (", ")
	if len (diff) == 2:
		days = diff[0].split()[0]
		time = diff[1].split(".")
		if len (time) == 2:
			clock = time[0].split(":")
			microseconds = time[1]
			hours = clock[0]
			minutes = clock[1]
			seconds = clock[2]
			return datetime.timedelta (days = int (days), hours = int (hours), minutes = int (minutes), seconds = int (seconds), microseconds = int (microseconds))
		else:
			clock = time[0].split(":")
			hours = clock[0]
			minutes = clock[1]
			seconds = clock[2]
			return datetime.timedelta (days = int (days), hours = int (hours), minutes = int (minutes), seconds = int (seconds))
	else:
		time = diff[0].split (".")
		if len (time) == 2:
			clock = time[0].split(":")
			microseconds = time[1]
			hours = clock[0]
			minutes = clock[1]
			seconds = clock[2]
			return datetime.timedelta (hours = int (hours), minutes = int (minutes), seconds = int (seconds), microseconds = int (microseconds))
		else:
			clock = time[0].split(":")
			hours = clock[0]
			minutes = clock[1]
			seconds = clock[2]
			return datetime.timedelta (hours = int (hours), minutes = int (minutes), seconds = int (seconds))

def initGoals():
	try:
		with open ("cookies/goals.cookie", "r") as content_file:
			content = content_file.readlines()
		goals = []
		for goal in content:
			goals.append (ast.literal_eval (goal))
		return goals
	except IOError:
		return []


def sort (x):
	return sorted (x, key = lambda goal: goal["losedate"])


def nearestGoal():
	try:
		with open ("cookies/goals.cookie", "r") as content_file:
			content = content_file.readlines()
		goals = []
		for goal in content:
			goals.append (ast.literal_eval (goal))
		goals = sort (goals)
		if goals:
			return goals[0]
		else:
			return ""
	except IOError:
		return ""


def getTimeList():
	now = datetime.datetime.now()
	try:
		with open ("cookies/settings.cookie", "r") as content_file:
			settings = content_file.read()
		settings = ast.literal_eval (settings)
		diff = parseDelta (settings["diff"])
		result = now + diff
		resultList = [str (result.hour / 10), str (result.hour % 10), str (result.minute / 10), str (result.minute % 10)]
		return resultList
	except IOError:
		resultList = [str (now.hour / 10), str (now.hour % 10), str (now.minute / 10), str (now.minute % 10)]
		return resultList

def getDateList():
	now = datetime.datetime.now()
	try:
		with open ("cookies/settings.cookie", "r") as content_file:
			settings = content_file.read()
		settings = ast.literal_eval (settings)
		diff = parseDelta (settings["diff"])
		result = now + diff
		resultList = [str (result.day / 10), str (result.day % 10), str (result.month), str (result.year)[0], str (result.year)[1], str (result.year)[2], str (result.year)[3]]
		return resultList
	except IOError:
		resultList = [str (now.day / 10), str (now.day % 10), str (now.month), str (now.year)[0], str (now.year)[1], str (now.year)[2], str (now.year)[3]]
		return resultList


def getTimeDiff():
	now = datetime.datetime.now()
	try:
		with open ("cookies/settings.cookie", "r") as content_file:
			settings = content_file.read()
		settings = ast.literal_eval (settings)
		diff = parseDelta (settings["diff"])
		return diff
	except IOError:
		return datetime.timedelta()


def getTextColor():
	try:
		with open ("cookies/settings.cookie", "r") as content_file:
			settings = content_file.read()
		settings = ast.literal_eval (settings)
		if settings["theme"] == "Dark":
			return (1, 1, 1, 1)
		elif settings["theme"] == "Light":
			return (0, 0, 0, 1)
	except IOError:
		return (1, 1, 1, 1)


def getScreen():
	try:
		with open ("cookies/settings.cookie", "r") as content_file:
			settings = content_file.read()
		settings = ast.literal_eval (settings)
		return settings["screen"]
	except IOError:
		return 0
# -------------------------------------------------------------

class FloatInput (TextInput):

	pat = re.compile ('[^0-9]')
	def insert_text (self, substring, from_undo = False):
		pat = self.pat
		if '.' in self.text:
			s = re.sub (pat, '', substring)
		else:
			s = '.'.join ([re.sub(pat, '', s) for s in substring.split ('.', 1)])
		return super (FloatInput, self).insert_text (s, from_undo = from_undo)



class CustomLayout(FloatLayout):
	
	background_image = ObjectProperty(
		Image(
			source = "",
			anim_delay = .04))

class SleepScreen (Screen):

	diff = ObjectProperty (getTimeDiff())
	textColor = ListProperty ([1, 1, 1, 1])

	def build (self):
		pass

	def updateClock (self, *args):
		time = self.ids["sleepTime"]
		date = self.ids["sleepDate"]
		time.text = self.getTime()
		date.text = self.getDate()
	
	def getDate (self):
		return (datetime.datetime.now() + self.diff).strftime("%d %B %Y")

	def getTime (self):
		return (datetime.datetime.now() + self.diff).strftime("%H:%M")

	def getNearestGoal (self):
		nearest = nearestGoal()
		if nearest == "":
			return nearest
		else:
			return nearest["title"] + ": " + datetime.datetime.fromtimestamp (nearest["losedate"]).strftime ("%H:%M %d %B %Y")

	def updateNearestGoal (self):
		nearestGoal = self.ids["sleepGoal"]
		nearestGoal.text = self.getNearestGoal()

	def returnBack (self):
		try:
			self.manager.current = "taskScreen"
		except ScreenManagerException:
			self.manager.current = "loginScreen"

class TaskScreen (Screen):


	goals = ListProperty (initGoals())
	current = NumericProperty (0)
	diff = ObjectProperty (getTimeDiff())
	theme = StringProperty (getTheme())
	textColor = ListProperty (getTextColor())
	view = ModalView (size_hint = (None, None), size = (300, 300))
	check = ModalView()
	darks = ListProperty ([6, 8])
	def __init__ (self, **kwargs):
		super (TaskScreen, self).__init__ (**kwargs)
		self._keyboard = Window.request_keyboard (self._keyboard_closed, self, "text")
		if self._keyboard.widget:
			self._keyboard.widget.layout = "newLayout.json"
			self._keyboard.widget.margin_hint = [.05, .03, .05, .03]
		self._keyboard.bind (on_key_down = self._on_keyboard_down)

	def _keyboard_closed (self):
		self._keyboard.unbind (on_key_down = self._on_keyboard_down)
		self._keyboard = None

	def _on_keyboard_down (self, keyboard, keycode, text, modifiers):
		if keycode[1] == "enter":
			keyboard.release()
		return True

	def build (self):
		pass

	def updateClock (self, *args):
		time = self.ids["statusTime"]
		date = self.ids["statusDate"]
		time.text = self.getTime()
		date.text = self.getDate()

	def getDate (self):
		return (datetime.datetime.now() + self.diff).strftime("%d %B %Y")

	def getTime (self):
		return (datetime.datetime.now() + self.diff).strftime("%H:%M")

	def prevGraph (self):
		if self.goals:
			if self.current == 0:
				self.current = len (self.goals) - 1
			else:
				self.current -= 1

	def nextGraph (self):
		if self.goals:
			self.current = (self.current + 1) % len (self.goals)


	def goToSleepScreen (self):
		sleepScreen = self.manager.get_screen ("sleepScreen")
		sleepScreen.children[-1].background_image.source = "data/gif/screen" + getScreen() + ".zip"
		if int (getScreen()) in self.darks:
			sleepScreen.textColor = [0, 0, 0, 1]
		else:
			sleepScreen.textColor = [1, 1, 1, 1]
		sleepScreen.updateNearestGoal()
		self.manager.current = "sleepScreen"

	def goToSettingsScreen (self):
		settingsScreen = self.manager.get_screen ("settingsScreen")
		settingsScreen.refreshSettings()
		settingsScreen.changeSettingsContent()
		self.manager.current = "settingsScreen"

	def checkLogout (self, *args):
		self.check.clear_widgets()
		self.check.background = "data/images/"  + self.theme + ".png"
		self.check.size_hint = (.6, .6)
		message = BoxLayout (orientation = "vertical")
		text = Label (text = "Do you want to logout?", font_size = 18, color = self.textColor)
		choice = BoxLayout (orientation = "horizontal")
		yes = Factory.ImageButton()
		yes.children[0].source = "data/icons/" + self.theme + "/png/32/checkmark.png"
		yes.bind (on_press = self.logout)
		no = Factory.ImageButton()
		no.children[0].source = "data/icons/" + self.theme + "/png/32/delete.png"
		no.bind (on_press = self.check.dismiss)
		choice.add_widget (yes)
		choice.add_widget (no)
		message.add_widget (text)
		message.add_widget (choice)
		self.check.add_widget (message)
		self.check.open()

	def logout (self, *args):
		os.remove ("cookies/user.cookie")
		os.remove ("cookies/goals.cookie")
		graphs = os.listdir ("graph")
		for i in graphs:
			os.remove ("graph/" + i)
		loginScreen = LoginScreen (name = "loginScreen")
		loginScreen.theme = self.theme
		loginScreen.textColor = self.textColor
		Clock.schedule_interval (loginScreen.updateClock, 1)
		loginScreen._keyboard = Window.request_keyboard (loginScreen._keyboard_closed, self, "text")
		loginScreen._keyboard.release()
		self.check.dismiss()
		self.manager.add_widget (loginScreen)
		self.manager.current = "loginScreen"
		taskScreen = self.manager.get_screen ("taskScreen")
		self.manager.remove_widget (taskScreen)

	def showGraph (self):
		if self.goals:
			show = ModalView (size_hint = (1, 1))
			close = Factory.ImageButton (size_hint = (1, 1))
			close.children[0].source = "graph/" + os.listdir ("graph")[self.current]
			close.children[0].size_hint = (1, 1)
			close.bind (on_press = show.dismiss)
			show.add_widget (close)
			show.open()

	def showInfo (self):
		if self.goals:
			self.check.clear_widgets()
			self.check.background = "data/images/"  + self.theme + ".png"
			self.check.size_hint = (.85, .85)
			info = BoxLayout (orientation = "vertical", spacing = 10, size_hint = (1, 1))
			norm = Label (color = self.textColor, text = "Your promise: " + str (self.goals[self.current]["rate"]) + " per " + self.goals[self.current]["runits"])
			contract = Label (color = self.textColor)
			if self.goals[self.current]["contract"] and self.goals[self.current]["contract"]["amount"]:
				contract.text = "Money on the line: " + self.goals[self.current]["contract"]["amount"]
			else:
				contract.text = "No money on the line"
			pledge = Label(color = self.textColor)
			if self.goals[self.current]["pledge"]:
				pledge.text = "Money spent: " + self.goals[self.current]["pledge"]
			else:
				pledge.text = "No money spent"
			progress = Label(color = self.textColor)
			if self.goals[self.current]["lane"] * self.goals[self.current]["yaw"] > 1:
				progress.text = "Progress: you are doing more than enough, that's awesome"
			elif self.goals[self.current]["lane"] * self.goals[self.current]["yaw"] > -1:
				progress.text = "Progress: you are doing great, keep up the good work"
			elif self.goals[self.current]["lane"] * self.goals[self.current]["yaw"] == -1:
				progress.text = "Progress: you are on the road, but you can do better"
			else:
				progress.text = "Progress: you are on the verge of failing or failed"
			close = Factory.ImageButton (size_hint = (1, 1))
			close.bind (on_press = self.check.dismiss)
			info.add_widget (norm)
			info.add_widget (contract)
			info.add_widget (pledge)
			info.add_widget (progress)
			self.check.add_widget (close)
			self.check.add_widget (info)
			self.check.open()

	def addData (self):
		if self.goals:
			self.check.clear_widgets()
			self.check.background = "data/images/"  + self.theme + ".png"
			self.check.size_hint = (.85, .85)
			submit = BoxLayout (orientation = "vertical", spacing = 10, padding = [10, 10, 10, 10], size_hint = (1, 1))
			value = BoxLayout (orientation = "horizontal", spacing = 5)
			valueMessage = Label (color = self.textColor, text = "How much did you do today?")
			valueBox = FloatInput (write_tab = False, multiline = False, font_size = 24)
			value.add_widget (valueMessage)
			value.add_widget (valueBox)
			comment = BoxLayout (orientation = "horizontal", spacing = 5)
			commentMessage = Label (color = self.textColor, text = "Comment")
			commentBox = TextInput (write_tab = False)
			comment.add_widget (commentMessage)
			comment.add_widget (commentBox)
			email = BoxLayout (orientation = "horizontal")
			emailMessage = Label (color = (1, 0, 0, 1), text = "")
			email.add_widget (emailMessage)
			choice = BoxLayout (orientation = "horizontal")
			yes = Factory.ImageButton()
			yes.children[0].source = "data/icons/" + self.theme + "/png/32/checkmark.png"
			yes.bind (on_press = self.sendValues)
			no = Factory.ImageButton()
			no.children[0].source = "data/icons/" + self.theme + "/png/32/delete.png"
			no.bind (on_press = self.check.dismiss)
			choice.add_widget (yes)
			choice.add_widget (no)
			submit.add_widget (value)
			submit.add_widget (comment)
			submit.add_widget (email)
			submit.add_widget (choice)
			self.check.add_widget (submit)
			self.check.open()

	def sendValues (self, *args):
		userFile = open ("cookies/user.cookie", "r")
		username = userFile.readline()[15:-1]
		auth_token = userFile.readline()[19:-1]
		userFile.close()
		goal = self.goals[self.current]["slug"]
		api = beeminderpy.Beeminder (username, auth_token)
		values = self.check.children[-1].children[-1].children[-2].text
		comment = self.check.children[-1].children[-2].children[-2].text
		response = json.loads (api.create_datapoint (goal, values, comment))
		response = json.loads (api.refresh_graph (goal))
		if response:
			while (True):
				response = json.loads (api.get_goal (goal))
				print response
				newgoal = {}
				for key in response:
					if isinstance (key, unicode):
						if isinstance (response[key], unicode):
							newgoal[unicodedata.normalize ("NFKD", key).encode ("ascii", "ignore")] = unicodedata.normalize ("NFKD", response[key]).encode ("ascii", "ignore")
						else:
							newgoal[unicodedata.normalize ("NFKD", key).encode ("ascii", "ignore")] = response[key]
					else:
						if isinstance (response[key], unicode):
							newgoal[key] = unicodedata.normalize ("NFKD", response[key]).encode ("ascii", "ignore")
						else:
							newgoal[key] = response[key]
				if newgoal["queued"] == False:
					break
			graphfile = urllib.URLopener()
			graphfile.retrieve (newgoal["graph_url"], "graph/" + newgoal["slug"] + ".png")
			del self.goals[self.current]
			self.goals.insert (self.current, newgoal)
			goalsFile = open ("cookies/goals.cookie", "w+")
			goalsFile.write ('\n'.join (map (str, self.goals)))
			goalsFile.close()
			self.check.dismiss()
		else:
			self.check.children[-1].children[-3].children[-1].text = "Try again"

	def showEvents(self):

		main_layout = GridLayout(cols=1,rows=1) 
		
		refresh_payload={'client_id': '80436600272-vbpjaklvfvgg7ucdvtnt1i4jrdbtmkq8.apps.googleusercontent.com', 'client_secret':'FHymJpeQ2CDpGda0cJhwtwkc','refresh_token':'1/-IqWcFhBST23F4hBBd-3Twgk7cBwyRsrF28jAjMPpcU', 'grant_type':'refresh_token'}
		refresh_request=requests.post('https://www.googleapis.com/oauth2/v3/token',data=refresh_payload)
		print refresh_request.json()['access_token']
		access_token_payload={'access_token':refresh_request.json()['access_token']}
		
		calendar_list_request=requests.get('https://www.googleapis.com/calendar/v3/users/me/calendarList', params=access_token_payload)
		
		calendars=calendar_list_request.json()['items']
		
		event_request=requests.get('https://www.googleapis.com/calendar/v3/calendars/'+calendars[0]['id'] +'/events',params=access_token_payload)


		events=event_request.json()['items']
		todos=[]
		for i in range(0,len(events)):
			 todos.append(events[i]['summary'])
		list_view = ListView(item_strings=todos)

		main_layout.add_widget(list_view)

		self.view.add_widget(main_layout)

		self.view.open()
		
class LoginScreen (Screen):

	diff = ObjectProperty (getTimeDiff())
	theme = StringProperty (getTheme())
	textColor = ListProperty (getTextColor())
	darks = ListProperty ([6, 8])

	def __init__ (self, **kwargs):
		super (LoginScreen, self).__init__ (**kwargs)
		self._keyboard = Window.request_keyboard (self._keyboard_closed, self, "text")
		if self._keyboard.widget:
			self._keyboard.widget.layout = "newLayout.json"
			self._keyboard.widget.margin_hint = [.05, .03, .05, .03]
		self._keyboard.bind (on_key_down = self._on_keyboard_down)

	def _keyboard_closed (self):
		self._keyboard.unbind (on_key_down = self._on_keyboard_down)
		self._keyboard = None

	def _on_keyboard_down (self, keyboard, keycode, text, modifiers):
		if keycode[1] == "enter":
			keyboard.release()
		return True

	def build (self):
		pass

	def updateClock (self, *args):
		time = self.ids["statusTime"]
		date = self.ids["statusDate"]
		time.text = self.getTime()
		date.text = self.getDate()

	def getDate (self):
		return (datetime.datetime.now() + self.diff).strftime("%d %B %Y")

	def getTime (self):
		return (datetime.datetime.now() + self.diff).strftime("%H:%M")


	def checkLogin (self):
		self._keyboard = Window.request_keyboard (self._keyboard_closed, self, "text")
		self._keyboard.release()
		username = self.ids["username"].text
		password = self.ids["password"].text
		if not username or not password:
			error = self.ids["errorLabel"]
			error.text = "Don't leave forms blank"
			return

		try:
			cj = cookielib.CookieJar()
			opener = urllib2.build_opener (urllib2.HTTPCookieProcessor (cj))
			login_data = urllib.urlencode ({"user[login]" : username, "user[password]" : password})
			opener.open ("https://www.beeminder.com/users/sign_in", login_data)
			response = json.loads (opener.open ("https://www.beeminder.com/api/v1/auth_token.json").read())
			if not os.path.exists("cookies"):
				os.makedirs("cookies")
			userFile = open ("cookies/user.cookie", "w+")
			userFile.write ("{user[login] : " + username + "\nuser[auth_token] : " + response["auth_token"] + "}")
			userFile.close()
			goals = json.loads (beeminderpy.Beeminder (username, response["auth_token"]).get_all_goals())


			newgoals = []
			for goal in goals:
				newgoal = {}
				for key in goal:
					if isinstance (key, unicode):
						if isinstance (goal[key], unicode):
							newgoal[unicodedata.normalize ("NFKD", key).encode ("ascii", "ignore")] = unicodedata.normalize ("NFKD", goal[key]).encode ("ascii", "ignore")
						else:
							newgoal[unicodedata.normalize ("NFKD", key).encode ("ascii", "ignore")] = goal[key]
					else:
						if isinstance (goal[key], unicode):
							newgoal[key] = unicodedata.normalize ("NFKD", goal[key]).encode ("ascii", "ignore")
						else:
							newgoal[key] = goal[key]
				newgoals.append (newgoal)
			sort (newgoals)
			goalsFile = open ("cookies/goals.cookie", "w+")
			goalsFile.write ('\n'.join (map (str, newgoals)))
			goalsFile.close()
			for goal in newgoals:
				graphfile = urllib.URLopener()
				graphfile.retrieve (goal["graph_url"], "graph/" + goal["slug"] + ".png")
			taskScreen = TaskScreen (name = "taskScreen", goals = newgoals, current = 0)
			taskScreen.theme = self.theme
			taskScreen.textColor = self.textColor
			Clock.schedule_interval (taskScreen.updateClock, 1)
			self.manager.add_widget (taskScreen)
			self.manager.current = "taskScreen"
			self.manager.remove_widget (self)



		except urllib2.HTTPError:
			error = self.ids["errorLabel"]
			error.text = "Wrong username/password"


	def goToSettingsScreen (self):
		settingsScreen = self.manager.get_screen ("settingsScreen")
		settingsScreen.refreshSettings()
		settingsScreen.changeSettingsContent()
		self.manager.current = "settingsScreen"


	def goToSleepScreen (self):
		sleepScreen = self.manager.get_screen ("sleepScreen")
		sleepScreen.children[-1].background_image.source = "data/gif/screen" + getScreen() + ".zip"
		if int (getScreen()) in self.darks:
			sleepScreen.textColor = [0, 0, 0, 1]
		else:
			sleepScreen.textColor = [1, 1, 1, 1]
		sleepScreen.updateNearestGoal()
		sleepScreen.updateNearestGoal()
		self.manager.current = "sleepScreen"

class SettingsScreen (Screen):

	tabs = ListProperty (["Time", "Date", "Theme", "Screensaver", "Wi-Fi"])
	diff = ObjectProperty (getTimeDiff())
	timeList = ListProperty (getTimeList())
	dateList = ListProperty (getDateList())
	current = NumericProperty (0)
	theme = StringProperty (getTheme())
	themeList = ListProperty (["Dark", "Light"])
	textColor = ListProperty (getTextColor())
	screen = StringProperty (getScreen())

	def build (self):
		pass

	def updateClock (self, *args):
		time = self.ids["statusTime"]
		date = self.ids["statusDate"]
		time.text = self.getTime()
		date.text = self.getDate()


	def getDate (self):
		return (datetime.datetime.now() + self.diff).strftime("%d %B %Y")

	def getTime (self):
		return (datetime.datetime.now() + self.diff).strftime("%H:%M")


	def prevTab (self):
		if (self.current == 0):
			self.current = len (self.tabs) - 1
		else:
			self.current -= 1
		tab = self.ids["tabName"]
		self.changeSettingsContent()


	def nextTab (self):
		self.current = (self.current + 1) % len (self.tabs)
		tab = self.ids["tabName"]
		self.changeSettingsContent()


	def saveChanges (self):
		with open ("cookies/settings.cookie", "r") as content_file:
			settings = ast.literal_eval (content_file.read())
		newTime = datetime.datetime.strptime (self.dateList[0] + self.dateList[1] + " " + monthString (int (self.dateList[2])) + " " + self.dateList[3] + self.dateList[4] + self.dateList[5] + self.dateList[6] + " " + self.timeList[0] + self.timeList[1] + ":" + self.timeList[2] + self.timeList[3], "%d %B %Y %H:%M")
		now = datetime.datetime.now()
		diff = newTime - now
		settings["diff"] = str (diff)
		settings["theme"] = self.theme
		settings["screen"] = self.screen
		settingsFile = open ("cookies/settings.cookie", "w+")
		settingsFile.write (str (settings))
		settingsFile.close()
		self.diff = diff
		try:
			taskScreen = self.manager.get_screen ("taskScreen")
			taskScreen.diff = diff
			taskScreen.theme = self.theme
			taskScreen.textColor = self.textColor
			sleepScreen = self.manager.get_screen ("sleepScreen")
			sleepScreen.diff = diff
			sleepScreen.theme = self.theme
			sleepScreen.textColor = self.textColor
			infoScreen = self.manager.get_screen ("infoScreen")
			infoScreen.diff = diff
			infoScreen.theme = self.theme
			infoScreen.textColor = self.textColor
			taskScreen.updateClock()
			self.manager.current = "taskScreen"
		except ScreenManagerException:
			loginScreen = self.manager.get_screen ("loginScreen")
			loginScreen.diff = diff
			loginScreen.theme = self.theme
			loginScreen.textColor = self.textColor
			sleepScreen = self.manager.get_screen ("sleepScreen")
			sleepScreen.diff = diff
			sleepScreen.theme = self.theme
			sleepScreen.textColor = self.textColor
			infoScreen = self.manager.get_screen ("infoScreen")
			infoScreen.diff = diff
			infoScreen.theme = self.theme
			infoScreen.textColor = self.textColor
			loginScreen.updateClock()		
			self.manager.current = "loginScreen"


	def discardChanges (self):
		try:
			self.manager.current = "taskScreen"
		except ScreenManagerException:
			self.manager.current = "loginScreen"


	def changeSettingsContent (self):
		content = self.ids["settingsContent"]
		content.clear_widgets()
		if self.current == 0:
			content.size_hint = (.4, .8)
			up = BoxLayout (size_hint = (1, .3), orientation = "horizontal")
			up1 = Factory.NoImageButton (size_hint = (.2, 1))
			up1.bind (on_press = self.hour1Up)
			up2 = Factory.NoImageButton (size_hint = (.2, 1))
			up2.bind (on_press = self.hour2Up)
			space = Label (size_hint = (.2, 1))
			up3 = Factory.NoImageButton (size_hint = (.2, 1))
			up3.bind (on_press = self.min1Up)
			up4 = Factory.NoImageButton (size_hint = (.2, 1))
			up4.bind (on_press = self.min2Up)
			up.add_widget (up1)
			up.add_widget (up2)
			up.add_widget (space)
			up.add_widget (up3)
			up.add_widget (up4)

			time = BoxLayout (size_hint = (1, .4), orientation = "horizontal")
			h1 = Factory.CenteredText (color = self.textColor, size_hint = (.2, 1), text = self.timeList[0], font_size = 54)
			h2 = Factory.CenteredText (color = self.textColor, size_hint = (.2, 1), text = self.timeList[1], font_size = 54, opacity = .3)
			colon = Factory.CenteredText (color = self.textColor, size_hint = (.2, 1), text = ":", font_size = 54, opacity = .3)
			m1 = Factory.CenteredText (color = self.textColor, size_hint = (.2, 1), text = self.timeList[2], font_size = 54, opacity = .3)
			m2 = Factory.CenteredText (color = self.textColor, size_hint = (.2, 1), text = self.timeList[3], font_size = 54, opacity = .3)
			time.add_widget (h1)
			time.add_widget (h2)
			time.add_widget (colon)
			time.add_widget (m1)
			time.add_widget (m2)

			down = BoxLayout (size_hint = (1, .3), orientation = "horizontal")
			down1 = Factory.NoImageButton (size_hint = (.2, 1))
			down1.bind (on_press = self.hour1Down)
			down2 = Factory.NoImageButton (size_hint = (.2, 1))
			down2.bind (on_press = self.hour2Down)
			space2 = Label (size_hint = (.2, 1))
			down3 = Factory.NoImageButton (size_hint = (.2, 1))
			down3.bind (on_press = self.min1Down)
			down4 = Factory.NoImageButton (size_hint = (.2, 1))
			down4.bind (on_press = self.min2Down)
			down.add_widget (down1)
			down.add_widget (down2)
			down.add_widget (space2)
			down.add_widget (down3)
			down.add_widget (down4)

			content.add_widget (up)
			content.add_widget (time)
			content.add_widget (down)

		elif self.current == 1:
			content.size_hint = (.7, .8)
			up = BoxLayout (size_hint = (1, .3), orientation = "horizontal")
			up1 = Factory.NoImageButton (size_hint = (.31, 1))
			up1.bind (on_press = self.dayUp)
			space = Label (size_hint = (.13, 1))
			up3 = Factory.NoImageButton (size_hint = (.46, 1))
			up3.bind (on_press = self.monthUp)
			space2 = Label (size_hint = (.1, 1))
			up4 = Factory.NoImageButton (size_hint = (.6, 1))
			up4.bind (on_press = self.yearUp)
			up.add_widget (up1)
			up.add_widget (space)
			up.add_widget (up3)
			up.add_widget (space2)
			up.add_widget (up4)

			date = BoxLayout (size_hint = (1, .4), orientation = "horizontal")
			d1 = Factory.CenteredText (color = self.textColor, size_hint = (.04, 1), text = self.dateList[0], font_size = 48)
			d2 = Factory.CenteredText (color = self.textColor, size_hint = (.04, 1), text = self.dateList[1], font_size = 48)
			m = Factory.CenteredText (color = self.textColor, size_hint = (.18, 1), text = monthString (int (self.dateList[2]))[0:3], font_size = 48, opacity = .3)
			y1 = Factory.CenteredText (color = self.textColor, size_hint = (.04, 1), text = self.dateList[3], font_size = 48, opacity = .3)
			y2 = Factory.CenteredText (color = self.textColor, size_hint = (.04, 1), text = self.dateList[4], font_size = 48, opacity = .3)
			y3 = Factory.CenteredText (color = self.textColor, size_hint = (.04, 1), text = self.dateList[5], font_size = 48, opacity = .3)
			y4 = Factory.CenteredText (color = self.textColor, size_hint = (.04, 1), text = self.dateList[6], font_size = 48, opacity = .3)
			date.add_widget (d1)
			date.add_widget (d2)
			date.add_widget (m)
			date.add_widget (y1)
			date.add_widget (y2)
			date.add_widget (y3)
			date.add_widget (y4)


			down = BoxLayout (size_hint = (1, .3), orientation = "horizontal")
			down1 = Factory.NoImageButton (size_hint = (.31, 1))
			down1.bind (on_press = self.dayDown)
			space5 = Label (size_hint = (.13, 1))
			down3 = Factory.NoImageButton (size_hint = (.46, 1))
			down3.bind (on_press = self.monthDown)
			space6 = Label (size_hint = (.1, 1))
			down4 = Factory.NoImageButton (size_hint = (.6, 1))
			down4.bind (on_press = self.yearDown)
			down.add_widget (down1)
			down.add_widget (space5)
			down.add_widget (down3)
			down.add_widget (space6)
			down.add_widget (down4)

			content.add_widget (up)
			content.add_widget (date)
			content.add_widget (down)


		elif self.current == 2:
			content.size_hint = (1, .8)
			choose = BoxLayout (orientation = "horizontal", size_hint = (1, 1))
			left = Factory.LeftButton()
			left.children[0].source = "data/icons/"  + self.theme + "/png/32/br_prev.png"
			left.bind (on_press = self.prevTheme)
			theme = Label (text = self.theme, font_size = 36, color = self.textColor)
			right = Factory.RightButton()
			right.children[0].source = "data/icons/"  + self.theme + "/png/32/br_next.png"
			right.bind (on_press = self.nextTheme)
			choose.add_widget (left)
			choose.add_widget (theme)
			choose.add_widget (right)
			content.add_widget (choose)

		elif self.current == 3:
			content.size_hint = (1, .8)
			choose = BoxLayout (orientation = "horizontal", size_hint = (1, 1))
			left = Factory.LeftButton()
			left.children[0].source = "data/icons/"  + self.theme + "/png/32/br_prev.png"
			left.bind (on_press = self.prevScreen)
			space = Label (size_hint = (.05, 1))
			screen = CustomLayout (size_hint = (.4, 1))
			screen.background_image.source = "data/gif/screen" + self.screen + ".zip"
			space2 = Label (size_hint = (.05, 1))
			right = Factory.RightButton()
			right.children[0].source = "data/icons/"  + self.theme + "/png/32/br_next.png"
			right.bind (on_press = self.nextScreen)
			choose.add_widget (left)
			choose.add_widget (space)
			choose.add_widget (screen)
			choose.add_widget (space2)
			choose.add_widget (right)
			content.add_widget (choose)


	def hour1Up (self, *args):
		content = self.ids["settingsContent"]
		time = content.children[1]
		toChange = time.children[-1]
		for i in time.children:
			i.opacity = .3
		toChange.opacity = 1
		toChange.text = str ((int (toChange.text) + 1) % 3)
		self.timeList[0] = toChange.text
		if toChange.text == "2":
			if int (time.children[-2].text) > 3:
				time.children[-1].text = "2"
				time.children[-2].text = "3"
				self.timeList[1] = "3"


	def hour2Up (self, *args):
		content = self.ids["settingsContent"]
		time = content.children[1]
		toChange = time.children[-2]
		for i in time.children:
			i.opacity = .3
		toChange.opacity = 1
		if (time.children[-1].text == "2"):
			toChange.text = str ((int (toChange.text) + 1) % 4)
		else:
			toChange.text = str ((int (toChange.text) + 1) % 10)
		self.timeList[1] = toChange.text

	def min1Up (self, *args):
		content = self.ids["settingsContent"]
		time = content.children[1]
		toChange = time.children[-4]
		for i in time.children:
			i.opacity = .3
		toChange.opacity = 1
		toChange.text = str ((int (toChange.text) + 1) % 6)
		self.timeList[2] = toChange.text

	def min2Up (self, *args):
		content = self.ids["settingsContent"]
		time = content.children[1]
		toChange = time.children[-5]
		for i in time.children:
			i.opacity = .3
		toChange.opacity = 1
		toChange.text = str ((int (toChange.text) + 1) % 10)
		self.timeList[3] = toChange.text

	def hour1Down (self, *args):
		content = self.ids["settingsContent"]
		time = content.children[1]
		toChange = time.children[-1]
		for i in time.children:
			i.opacity = .3
		toChange.opacity = 1
		if (toChange.text == "0"):
			toChange.text = "2"
		else:
			toChange.text = str (int (toChange.text) - 1)
		self.timeList[0] = toChange.text
		if toChange.text == "2":
			if int (time.children[-2].text) > 3:
				time.children[-2].text = "3"
				self.timeList[1] = "3"

	def hour2Down (self, *args):
		content = self.ids["settingsContent"]
		time = content.children[1]
		toChange = time.children[-2]
		for i in time.children:
			i.opacity = .3
		toChange.opacity = 1
		if (time.children[-1].text == "2"):
			if (toChange.text == "0"):
				toChange.text = "3"
			else:
				toChange.text = str (int (toChange.text) - 1)
		else:
			if (toChange.text == "0"):
				toChange.text = "9"
			else:
				toChange.text = str (int (toChange.text) - 1)
		self.timeList[1] = toChange.text

	def min1Down (self, *args):
		content = self.ids["settingsContent"]
		time = content.children[1]
		toChange = time.children[-4]
		for i in time.children:
			i.opacity = .3
		toChange.opacity = 1
		if (toChange.text == "0"):
			toChange.text = "5"
		else:
			toChange.text = str (int (toChange.text) - 1)
		self.timeList[2] = toChange.text

	def min2Down (self, *args):
		content = self.ids["settingsContent"]
		time = content.children[1]
		toChange = time.children[-5]
		for i in time.children:
			i.opacity = .3
		toChange.opacity = 1
		if (toChange.text == "0"):
			toChange.text = "9"
		else:
			toChange.text = str (int (toChange.text) - 1)
		self.timeList[3] = toChange.text



	def dayUp (self, *args):
		content = self.ids["settingsContent"]
		date = content.children[1]
		for i in date.children:
			i.opacity = .3
		date.children[-1].opacity = 1
		date.children[-2].opacity = 1
		days = getDaysInMonth (date.children[-3].text, date.children[-4].text + date.children[-5].text + date.children[-6].text + date.children[-7].text)
		newDays = int (date.children[-1].text + date.children[-2].text)
		newDays = (newDays + 1) % (days + 1)
		newDays = str (newDays)
		if len (newDays) == 1:
			newDays = "0" + newDays
		self.dateList[0] = newDays[0]
		self.dateList[1] = newDays[1]
		date.children[-1].text = self.dateList[0]
		date.children[-2].text = self.dateList[1]


	def monthUp (self, *args):
		content = self.ids["settingsContent"]
		date = content.children[1]
		toChange = date.children[-3]
		for i in date.children:
			i.opacity = .3
		toChange.opacity = 1
		toChange.text = monthString (max ((int (self.dateList[2]) + 1) % 13, 1))[0:3]
		days = getDaysInMonth (date.children[-3].text, date.children[-4].text + date.children[-5].text + date.children[-6].text + date.children[-7].text)
		self.dateList[2] = str (max ((int (self.dateList[2]) + 1) % 13, 1))
		if int (date.children[-1].text + date.children[-2].text) > days:
			date.children[-1].text = str (days)[0]
			date.children[-2].text = str (days)[1]


	def yearUp (self, *args):
		content = self.ids["settingsContent"]
		date = content.children[1]
		for i in date.children:
			i.opacity = .3
		date.children[-4].opacity = 1
		date.children[-5].opacity = 1
		date.children[-6].opacity = 1
		date.children[-7].opacity = 1
		newYear = int (date.children[-6].text + date.children[-7].text)
		newYear = (newYear + 1) % 100
		newYear = str (newYear)
		if len (newYear) == 1:
			newYear = "0" + newYear
		self.dateList[5] = newYear[0]
		self.dateList[6] = newYear[1]
		date.children[-6].text = self.dateList[5]
		date.children[-7].text = self.dateList[6]
		if int (date.children[-4].text + date.children[-5].text + date.children[-6].text + date.children[-7].text) % 4 != 0:
			if (date.children[-3].text == "Feb"):
				if int (date.children[-1].text + date.children[-2].text) == 29:
					date.children[-2].text = "8"
					self.dateList[1] = "8"


	def dayDown (self, *args):
		content = self.ids["settingsContent"]
		date = content.children[1]
		for i in date.children:
			i.opacity = .3
		date.children[-1].opacity = 1
		date.children[-2].opacity = 1
		days = getDaysInMonth (date.children[-3].text, date.children[-4].text + date.children[-5].text + date.children[-6].text + date.children[-7].text)
		newDays = int (self.dateList[0] + self.dateList[1])
		if newDays == 1:
			newDays = days
		else:
			newDays -= 1
		newDays = str (newDays)
		if len (newDays) == 1:
			newDays = "0" + newDays
		self.dateList[0] = newDays[0]
		self.dateList[1] = newDays[1]
		date.children[-1].text = self.dateList[0]
		date.children[-2].text = self.dateList[1]

	def monthDown (self, *args):
		content = self.ids["settingsContent"]
		date = content.children[1]
		toChange = date.children[-3]
		for i in date.children:
			i.opacity = .3
		toChange.opacity = 1
		if toChange.text == "Jan":
			toChange.text = "Dec"
			self.dateList[2] = "12"
		else:
			toChange.text = monthString (int (self.dateList[2]) - 1)[0:3]
			self.dateList[2] = str (int (self.dateList[2]) - 1)
		days = getDaysInMonth (date.children[-3].text, date.children[-4].text + date.children[-5].text + date.children[-6].text + date.children[-7].text)
		if int (date.children[-1].text + date.children[-2].text) > days:
			date.children[-1].text = str (days)[0]
			date.children[-2].text = str (days)[1]

	def yearDown (self, *args):
		content = self.ids["settingsContent"]
		date = content.children[1]
		for i in date.children:
			i.opacity = .3
		date.children[-4].opacity = 1
		date.children[-5].opacity = 1
		date.children[-6].opacity = 1
		date.children[-7].opacity = 1
		newYear = int (date.children[-6].text + date.children[-7].text)
		if newYear == 0:
			newYear = 99
		else:
			newYear -= 1
		newYear = str (newYear)
		if len (newYear) == 1:
			newYear = "0" + newYear
		self.dateList[5] = newYear[0]
		self.dateList[6] = newYear[1]
		date.children[-6].text = self.dateList[5]
		date.children[-7].text = self.dateList[6]
		if int (date.children[-4].text + date.children[-5].text + date.children[-6].text + date.children[-7].text) % 4 != 0:
			if (date.children[-3].text == "Feb"):
				if int (date.children[-1].text + date.children[-2].text) == 29:
					date.children[-2].text = "8"
					self.dateList[1] = "8"


	def prevTheme (self, *args):
		for i in range (0, len (self.themeList)):
			if self.theme == self.themeList[i]:
				currentTheme = i
				break
		if (currentTheme == 0):
			currentTheme = len (self.themeList) - 1
		else:
			currentTheme -= 1
		self.theme = self.themeList[currentTheme]
		content = self.ids["settingsContent"]
		theme = content.children[0].children[1]
		theme.text = self.theme
		if self.theme == "Dark":
			self.textColor = (1, 1, 1, 1)
		elif self.theme == "Light":
			self.textColor = (0, 0, 0, 1)
		anim = Animation (textColor = self.textColor, duration = .3)
		anim.start (self)
		anim = Animation (color = self.textColor, duration = .3)
		anim.start (theme)
		tabs = content.children[0]
		tabs.children[-1].children[0].source = "data/icons/" + self.theme + "/png/32/br_prev.png"
		tabs.children[-3].children[0].source = "data/icons/" + self.theme + "/png/32/br_next.png"

	def nextTheme (self, *args):
		for i in range (0, len (self.themeList)):
			if self.theme == self.themeList[i]:
				currentTheme = i
				break
		currentTheme = (currentTheme + 1) % len (self.themeList)
		self.theme = self.themeList[currentTheme]
		content = self.ids["settingsContent"]
		theme = content.children[0].children[1]
		theme.text = self.theme
		newColor = None
		if self.theme == "Dark":
			newColor = (1, 1, 1, 1)
		elif self.theme == "Light":
			newColor = (0, 0, 0, 1)
		anim = Animation (textColor = newColor, duration = .3)
		anim.start (self)
		anim = Animation (color = newColor, duration = .3)
		anim.start (theme)
		tabs = content.children[0]
		tabs.children[-1].children[0].source = "data/icons/" + self.theme + "/png/32/br_prev.png"
		tabs.children[-3].children[0].source = "data/icons/" + self.theme + "/png/32/br_next.png"


	def prevScreen (self, *args):
		if (self.screen == "0"):
			self.screen = str (len (os.listdir ("data/gif")) - 1)
		else:
			self.screen = str (int (self.screen) - 1)
		content = self.ids["settingsContent"]
		screen = content.children[0].children[-3]
		screen.background_image.source = "data/gif/screen" + self.screen + ".zip"


	def nextScreen (self, *args):
		self.screen = str ((int (self.screen) + 1) % len (os.listdir ("data/gif")))
		content = self.ids["settingsContent"]
		screen = content.children[0].children[-3]
		screen.background_image.source = "data/gif/screen" + self.screen + ".zip"


	def refreshSettings (self):
		self.timeList = getTimeList()
		self.dateList = getDateList()
		self.theme = getTheme()
		self.textColor = getTextColor()
		self.screen = getScreen()
		self.current = 0




class InfoScreen (Screen):

	diff = ObjectProperty (getTimeDiff())
	theme = StringProperty (getTheme())
	textColor = ListProperty (getTextColor())

	def build (self):
		pass

	def updateClock (self, *args):
		time = self.ids["statusTime"]
		date = self.ids["statusDate"]
		time.text = self.getTime()
		date.text = self.getDate()


	def getDate (self):
		return (datetime.datetime.now() + self.diff).strftime("%d %B %Y")

	def getTime (self):
		return (datetime.datetime.now() + self.diff).strftime("%H:%M")

	def goBack (self):
		try:
			self.manager.current = "taskScreen"
		except ScreenManagerException:
			self.manager.current = "loginScreen"	


class ClockApp(App):

	def build(self):

		try:
			with open ("cookies/settings.cookie", "r") as content_file:
				pass
		except IOError:
			settingsFile = open ("cookies/settings.cookie", "w+")
			settingsDict = {"diff" : "00:00:00", "theme" : "Dark", "screen": "0"}
			settingsFile.write (str (settingsDict))
			settingsFile.close()
			

		sm = ScreenManager ()
		sm.transition = SwapTransition ()
		if not os.path.isfile ("cookies/user.cookie"):
			loginScreen = LoginScreen (name = "loginScreen")
			sleepScreen = SleepScreen (name = "sleepScreen")
			settingsScreen = SettingsScreen (name = "settingsScreen")
			infoScreen = InfoScreen (name = "infoScreen")
			Clock.schedule_interval (loginScreen.updateClock, 1)
			Clock.schedule_interval (sleepScreen.updateClock, 1)
			Clock.schedule_interval (settingsScreen.updateClock, 1)
			Clock.schedule_interval (infoScreen.updateClock, 1)
			sm.add_widget (loginScreen)
			sm.add_widget (sleepScreen)
			sm.add_widget (settingsScreen)
			sm.add_widget (infoScreen)
			return sm
		if not os.path.isfile ("cookies/goals.cookie"):
			userFile = open ("cookies/user.cookie", "r")
			username = userFile.readline()[15:-1]
			auth_token = userFile.readline()[19:-1]
			userFile.close()
			goals = json.loads (beeminderpy.Beeminder (username, auth_token).get_all_goals())
			newgoals = []
			for goal in goals:
				newgoal = {}
				for key in goal:
					if isinstance (key, unicode):
						if isinstance (goal[key], unicode):
							newgoal[unicodedata.normalize ("NFKD", key).encode ("ascii", "ignore")] = unicodedata.normalize ("NFKD", goal[key]).encode ("ascii", "ignore")
						else:
							newgoal[unicodedata.normalize ("NFKD", key).encode ("ascii", "ignore")] = goal[key]
					else:
						if isinstance (goal[key], unicode):
							newgoal[key] = unicodedata.normalize ("NFKD", goal[key]).encode ("ascii", "ignore")
						else:
							newgoal[key] = goal[key]
				newgoals.append (newgoal)
			sort (newgoals)
			goalsFile = open ("cookies/goals.cookie", "w+")
			goalsFile.write ('\n'.join (map (str, newgoals)))
			goalsFile.close()
			for goal in newgoals:
				graphfile = urllib.URLopener()
				graphfile.retrieve (goal["graph_url"], goal["slug"] + ".png")


		taskScreen = TaskScreen (name = "taskScreen")
		sleepScreen = SleepScreen (name = "sleepScreen")
		settingsScreen = SettingsScreen (name = "settingsScreen")
		infoScreen = InfoScreen (name = "infoScreen")
		Clock.schedule_interval (taskScreen.updateClock, 1)
		Clock.schedule_interval (sleepScreen.updateClock, 1)
		Clock.schedule_interval (settingsScreen.updateClock, 1)
		Clock.schedule_interval (infoScreen.updateClock, 1)
		sm.add_widget (taskScreen)
		sm.add_widget (sleepScreen)
		sm.add_widget (settingsScreen)
		sm.add_widget (infoScreen)

		return sm


if __name__ == '__main__':
	ClockApp().run()
