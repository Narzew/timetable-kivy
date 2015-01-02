#encoding: utf-8
# Definicje klas planów tutaj.

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

class CityLublin(Screen):
	pass
	
class CitySanok(Screen):
	pass

class LublinBiskupiak(Screen):

	def set_class_nr(self,x):
		x = str(x)
		#self.class_nr = x
		App.get_running_app().class_nr = x
		
	def get_class_nr(self):
		return self.class_nr
		
	def show_plan(self,nr):
		App.get_running_app().show_ads()
		self.set_class_nr(nr)
		self.manager.current = 'CurrentPlan'
	
	pass
	
class LublinStaszic(Screen):

	def set_class_nr(self,x):
		x = str(x)
		#self.class_nr = x
		App.get_running_app().class_nr = x
		
	def get_class_nr(self):
		return self.class_nr
		
	def show_plan(self,nr):
		App.get_running_app().show_ads()
		self.set_class_nr(nr)
		self.manager.current = 'CurrentPlan'
	
	pass
	
class LublinZamoyski(Screen):

	def set_class_nr(self,x):
		x = str(x)
		#self.class_nr = x
		App.get_running_app().class_nr = x
		
	def get_class_nr(self):
		return self.class_nr
		
	def show_plan(self,nr):
		App.get_running_app().show_ads()
		self.set_class_nr(nr)
		self.manager.current = 'CurrentPlan'
	
	pass
	
class LublinPodwale(Screen):

	def set_class_nr(self,x):
		x = str(x)
		#self.class_nr = x
		App.get_running_app().class_nr = x
		
	def get_class_nr(self):
		return self.class_nr
		
	def show_plan(self,nr):
		App.get_running_app().show_ads()
		self.set_class_nr(nr)
		self.manager.current = 'CurrentPlan'
	
	pass
	
class LublinLO4(Screen):

	def set_class_nr(self,x):
		x = str(x)
		#self.class_nr = x
		App.get_running_app().class_nr = x
		
	def get_class_nr(self):
		return self.class_nr
		
	def show_plan(self,nr):
		App.get_running_app().show_ads()
		self.set_class_nr(nr)
		self.manager.current = 'CurrentPlan'
	
	pass
	
class LublinGim5(Screen):

	def set_class_nr(self,x):
		x = str(x)
		#self.class_nr = x
		App.get_running_app().class_nr = x
		
	def get_class_nr(self):
		return self.class_nr
		
	def show_plan(self,nr):
		App.get_running_app().show_ads()
		self.set_class_nr(nr)
		self.manager.current = 'CurrentPlan'
	
	pass
	
class LublinGim7(Screen):

	def set_class_nr(self,x):
		x = str(x)
		#self.class_nr = x
		App.get_running_app().class_nr = x
		
	def get_class_nr(self):
		return self.class_nr
		
	def show_plan(self,nr):
		App.get_running_app().show_ads()
		self.set_class_nr(nr)
		self.manager.current = 'CurrentPlan'
	
	pass
	
class SanokLO1(Screen):

	def set_class_nr(self,x):
		x = str(x)
		#self.class_nr = x
		App.get_running_app().class_nr = x
		
	def get_class_nr(self):
		return self.class_nr
		
	def show_plan(self,nr):
		App.get_running_app().show_ads()
		self.set_class_nr(nr)
		self.manager.current = 'CurrentPlan'
	
	pass
	
class SanokLO2(Screen):

	def set_class_nr(self,x):
		x = str(x)
		#self.class_nr = x
		App.get_running_app().class_nr = x
		
	def get_class_nr(self):
		return self.class_nr
		
	def show_plan(self,nr):
		App.get_running_app().show_ads()
		self.set_class_nr(nr)
		self.manager.current = 'CurrentPlan'
	
	pass
	
class SanokGim4(Screen):

	def set_class_nr(self,x):
		x = str(x)
		#self.class_nr = x
		App.get_running_app().class_nr = x
		
	def get_class_nr(self):
		return self.class_nr
		
	def show_plan(self,nr):
		App.get_running_app().show_ads()
		self.set_class_nr(nr)
		self.manager.current = 'CurrentPlan'
	
	pass
