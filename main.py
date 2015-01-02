#encoding: utf-8
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.utils import platform
import random
import zlib
import os.path
import marshal
import time
from planclasses import *
from jnius import autoclass
from plyer import email
import webbrowser

if platform=="android":
	PythonActivity=autoclass("org.renpy.android.PythonActivity")

class Main(Screen):
	
	def show_school_plan(self):
		if os.path.isfile("settings.ncp"):
			file = open("settings.ncp","rb")
			settings = marshal.loads(zlib.decompress(file.read()))
			file.close()
			App.get_running_app().school = settings["school"]
		else:
			App.get_running_app().school = "LublinBiskupiak"
		
		for i in App.get_running_app().schoollist:
			if App.get_running_app().school == i:
				self.manager.current = i
	
class ScrollableLabel(ScrollView):
	text = StringProperty("")

class CurrentPlan(Screen):
	
	def return_to_previous_plan(self):
		for i in App.get_running_app().schoollist:
			if App.get_running_app().school == i:
				self.manager.current = i
	
	def refresh_plan(self):
		name = "Plans/"+App.get_running_app().school+"/"+str(App.get_running_app().class_nr)+str(self.day_nr)+".txt"
		file = open(name,"rb")
		data = file.read()
		file.close
		data = "Plan Lekcji dla klasy "+App.get_running_app().class_nr+"\n"+self.convert_day_nr()+"\n\n"+data
		self.ids.planhere.text = data
	
	def set_day_nr(self,x):
		x = int(x)
		self.day_nr = x
		self.refresh_plan()
		
	def convert_day_nr(self):
		x = int(self.day_nr)
		if(x == 1):
			return "Poniedziałek"
		elif(x == 2):
			return "Wtorek"
		elif(x == 3):
			return "Środa"
		elif(x == 4):
			return "Czwartek"
		elif(x == 5):
			return "Piątek"
			
	def clear_plan_data(self):
		self.ids.planhere.text = "Wybierz dzień tygodnia"
	
	pass

class Bells(Screen):

	skrocone = False
		
	def toggle_skrocone(self,nr):
		nr = int(nr)
		if self.skrocone == True:
			self.skrocone = False
			self.ids.dzwonki_skrocone.text = "Pokaż skrócone lekcje"
		else:
			self.skrocone = True
			self.ids.dzwonki_skrocone.text = "Pokaż normalne lekcje"
		if nr == 0:
			self.show_bells()
		else:
			Breaks.show_breaks()
			
	def show_bells(self):
		App.get_running_app().load_settings()
		fileflag = True
		if self.skrocone==True:
			fname = "Schools/Extra/"+App.get_running_app().school+"/Bells2.txt"
			if os.path.isfile(fname):
				file = open(fname,"rb")
				data = "Lista dzwonków\nSkrócone lekcje\n\n"
				fileflag = True
			else:
				data = "Przepraszamy, brak listy dzwonków dla tej szkoły\n"
				fileflag = False
		else:
			fname = "Schools/Extra/"+App.get_running_app().school+"/Bells1.txt"
			if os.path.isfile(fname):
				file = open(fname,"rb")
				data = "Lista dzwonków\nNormalne lekcje\n\n"
				fileflag = True
			else:
				data = "Przepraszamy, brak listy dzwonków dla tej szkoły\n"
				fileflag = False
				
		if fileflag == True:
			data = data + file.read()
			file.close()
			
		self.ids.dzwonki_label.text = data
		return data
	
class Breaks(Screen):
	
	skrocone = False
	
	def toggle_skrocone(self,nr):
		nr = int(nr)
		if self.skrocone == True:
			self.skrocone = False
			self.ids.przerwy_skrocone.text = "Pokaż skrócone lekcje"
		else:
			self.skrocone = True
			self.ids.przerwy_skrocone.text = "Pokaż normalne lekcje"
			
		if nr == 0:
			Bells.show_bells()
		else:
			self.show_breaks()
	
	def show_breaks(self):
		App.get_running_app().load_settings()
		fileflag = True
		if self.skrocone==True:
			fname = "Schools/Extra/"+App.get_running_app().school+"/Breaks2.txt"
			if os.path.isfile(fname):
				file = open(fname,"rb")
				data = "Lista przerw\nSkrócone lekcje\n\n"
				fileflag = True
			else:
				data = "Przepraszamy, brak listy przerw dla tej szkoły\n"
				fileflag = False
		else:
			fname = "Schools/Extra/"+App.get_running_app().school+"/Breaks1.txt"
			if os.path.isfile(fname):
				file = open(fname,"rb")
				data = "Lista przerw\nNormalne lekcje\n\n"
				fileflag = True
			else:
				data = "Przepraszamy, brak listy przerw dla tej szkoły\n"
				fileflag = False
				
		if fileflag == True:
			data = data + file.read()
			file.close()
			
		self.ids.przerwy_label.text = data
		return data

		
class Teachers(Screen):
	
	def get_teachers_list(self):
		App.get_running_app().load_settings()
		fname = "Schools/Extra/"+App.get_running_app().school+"/Teachers.txt"
		if os.path.isfile(fname):
			file = open(fname,"rb")
			data = "Lista nauczycieli\n\n"+file.read()
			file.close()
		else:
			data = "Przepraszamy, brak listy nauczycieli dla tej szkoły\n"
		return data
	
	pass
	
class Events(Screen):
	
	def get_events_list(self):
		App.get_running_app().load_settings()
		fname = "Schools/Extra/"+App.get_running_app().school+"/Events.txt"
		if os.path.isfile(fname):
			file = open(fname,"rb")
			data = "Lista wydarzeń\n\n"+file.read()
			file.close()
		else:
			data = "Przepraszamy, brak listy wydarzeń dla tej szkoły\n"
		return data
	
	pass

class About(Screen):
	
	def send_email_to_dev(self):
		if platform=="android":
			self.email=email
			recipient="narzew@gmail.com"
			subject="Pytanie o Plan Lekcji"
			text=""
			create_chooser=False
			self.email.send(recipient,subject,text,create_chooser)
			
	def open_website(self, text):
		webbrowser.open(text)
	
	def get_about_info(self):
		file = open("Info/About.txt","rb")
		data = file.read()
		file.close()
		return data
		
	pass

class Cities(Screen):
	pass

class PlanLekcji(App):
	
	school = ""
	scrman = None
	
	def on_pause(self):
		return True
	
	def show_ads(self):
		if platform=="android":
			tick=self.random.randint(1, 6)
			if tick==1:
				self.AdBuddiz.showAd(PythonActivity.mActivity)
				return True
			else:
				return False
	
	def load_ads(self):
		if platform=="android":
			self.random=random
			self.AdBuddiz=autoclass("com.purplebrain.adbuddiz.sdk.AdBuddiz")
			self.AdBuddiz.setPublisherKey("secret")
			self.AdBuddiz.cacheAds(PythonActivity.mActivity)
	
	def load_screens(self):
		hour = int(time.strftime("%H"))
		minute = int(time.strftime("%M"))
		if (hour == 4 or hour == 16) and minute == 20:
			Builder.load_file("Layouts/Style-Cannabis.kv")
		else:
			if hour < 6 or hour > 21: # 22:00 - 5:59 <- Dark Screen ->
				Builder.load_file("Layouts/Style-Midnight.kv")
			else:
				Builder.load_file("Layouts/Style-LightBlue.kv")
		
		file = open("Screens.cfg", "rb")
		data = file.read()
		file.close()
		data = data.split("\n")
		App.get_running_app().schoollist = []
		for i in data:
			try:
				data2 = i.split("=")
				# Czy Screen jest szkołą ?
				if int(data2[0]) == 1:
					App.get_running_app().schoollist.append(data2[1])
					Builder.load_file('Schools/Layouts/'+data2[1]+'.kv')
				else:
					# Standardowy screen (nieszkolny)
					Builder.load_file('Layouts/'+data2[1]+'.kv')
			except:
				continue
				
	def load_settings(self):
		if os.path.isfile("settings.ncp"):
			file = open("settings.ncp","rb")
			settings = marshal.loads(zlib.decompress(file.read()))
			file.close()
			school = settings["school"]
			App.get_running_app().school = settings["school"]
		else:
			school = "LublinBiskupiak"
			App.get_running_app().school = "LublinBiskupiak"
			data = {}
			data["school"] = "LublinBiskupiak"
			file = open("settings.ncp","wb")
			file.write(zlib.compress(marshal.dumps(data)))
			file.close()
		return school
		
	def save_settings(self, newsettings):
		file = open("settings.ncp","wb")
		settings = newsettings
		file.write(zlib.compress(marshal.dumps(settings)))
		file.close()
		
	def select_school(self,sid):
		
		data = {}
		data["school"] = sid
		App.get_running_app().school = sid
		
		file = open("settings.ncp","wb")
		file.write(zlib.compress(marshal.dumps(data)))
		file.close()
	
	def build(self):
		
		sm = ScreenManager()
		self.load_screens()
		self.load_settings()
		self.load_ads()
		sm.add_widget(Main(name='Main'))
		sm.add_widget(Cities(name='Cities'))
		sm.add_widget(CurrentPlan(name='CurrentPlan'))
		sm.add_widget(Bells(name='Bells'))
		sm.add_widget(Breaks(name='Breaks'))
		sm.add_widget(Teachers(name='Teachers'))
		sm.add_widget(Events(name='Events'))
		sm.add_widget(About(name='About'))
		# MIASTA
		sm.add_widget(CityLublin(name='CityLublin'))
		sm.add_widget(CitySanok(name='CitySanok'))
		# SZKOŁY
		sm.add_widget(LublinBiskupiak(name='LublinBiskupiak'))
		sm.add_widget(LublinStaszic(name='LublinStaszic'))
		sm.add_widget(LublinZamoyski(name='LublinZamoyski'))
		sm.add_widget(LublinPodwale(name='LublinPodwale'))
		sm.add_widget(LublinLO4(name='LublinLO4'))
		sm.add_widget(LublinGim5(name='LublinGim5'))
		sm.add_widget(LublinGim7(name='LublinGim7'))
		sm.add_widget(SanokLO1(name='SanokLO1'))
		sm.add_widget(SanokLO2(name='SanokLO2'))
		sm.add_widget(SanokGim4(name='SanokGim4'))
		sm.current = 'Main'
		return sm
	
if __name__ == "__main__":
	PlanLekcji().run()
