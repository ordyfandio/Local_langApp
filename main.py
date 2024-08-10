from kivymd import hooks_path
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from database import person, Database
from kivymd.toast.kivytoast import toast
from kivymd.uix.list import OneLineListItem,MDList,ThreeLineListItem
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
import json
Window.size = (360, 580)



class Content(BoxLayout):
    manager= ObjectProperty()
    nav_drawer= ObjectProperty()


class HeroScreen(Screen):
    pass

class FrontPageScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class SignUpScreen(Screen):
    pass

class ProfileScreen(Screen):
    pass

class DashboardScreen(Screen):
    pass
class DetailScreen(Screen):
    def __init__(self, **kwargs):
        super(DetailScreen, self).__init__(**kwargs)
        self.sound = None
        
    def set_detail_info(self, eng_text, lan_text, fr_text, audio):
        self.stop_all_audio()
        self.sound = audio
        self.ids.detail_label.text = eng_text
        self.ids.secondary_label.text = lan_text
        self.ids.tertiary_label.text = fr_text
        self.ids.audio_list.clear_widgets()
        for audio in audio:
            button = Button(text=audio['name'], on_press=lambda x: self.play_audio(audio['file']))
            self.ids.audio_list.add_widget(button)
            
    def stop_all_audio(self):
        if self.sound:
            self.sound.stop()
            self.sound = None
            
    def load_audio(self, audio):
        self.sound = SoundLoader.load(audio)
        self.ids.audio_list.bind(on_press=self.play_audio)

    def play_audio(self, audio):
        if self.sound:
            self.sound.stop()
        self.sound = SoundLoader.load(audio)
        if self.sound:
            self.sound.volume = 0.5
            self.sound.play()

#code for Ewondo 
class DatasetScreen(Screen):            
    def load_data(self):
        with open('ewondo.json', 'r',encoding='utf-8') as f:
            self.word = json.load(f)
            for item in self.word:
                list_item = ThreeLineListItem(
                    text=item['eng'],
                    secondary_text=item['lan'],
                    tertiary_text=item['fr'],
                    theme_text_color="Custom"
                )
                list_item.bind(on_press=self.show_detail_screen)
                self.ids.grid.add_widget(list_item)
        
    def on_enter(self):        
        self.load_data()
    def show_detail_screen(self, instance):
        eng_text = instance.text
        lan_text = instance.secondary_text
        fr_text = instance.tertiary_text
        
        for item in self.word:
            if item['eng'] == eng_text and item['lan'] == lan_text and item['fr'] == fr_text:
                detail_screen = DetailScreen(name=f"detail_screen_{self.word.index(item)}")
                audio = item.get('audio', '')
                detail_screen.set_detail_info(item['eng'], item['lan'], item['fr'], audio)
                self.manager.add_widget(detail_screen)
                self.manager.current = detail_screen.name


# code for medumba
class DataScreen(Screen):
    def load_data(self):
        with open('data.json', 'r') as f:
            reader = json.load(f)
            for item in reader:
                list_item = ThreeLineListItem(
                    text=item['lang'],
                    secondary_text=item['mlan'],
                    tertiary_text=item['nature'],
                    theme_text_color="Custom"
                )
                self.ids.grid.add_widget(list_item)
    def on_enter(self):        
        self.load_data()

sm = ScreenManager()
sm.add_widget(HeroScreen(name="hero"))
sm.add_widget(FrontPageScreen(name="FrontPage"))
sm.add_widget(ProfileScreen(name="profile"))
sm.add_widget(LoginScreen(name="login"))
sm.add_widget(SignUpScreen(name="signup"))
sm.add_widget(DashboardScreen(name="dashboard"))
sm.add_widget(DataScreen(name="medumba"))
sm.add_widget(DatasetScreen(name="ewondo"))
sm.add_widget(DetailScreen(name="detail_screen"))

    

class MyApp(MDApp):
    def on_start(self):
        self.p_obj = person()
        self.data = Database()
        self.current_screen = "signup"

    def build(self):
        Screen = Builder.load_file('main.kv')
        self.icon="img/logo.jpeg"
        return Screen

    def signup(self):
        email= self.root.get_screen('signup').ids.email_signup.text
        password= self.root.get_screen('signup').ids.password_signup.text
        print(email)
        print(password)
        if not email and not password:
            return toast('email and password are not provided.')
        elif not email:
            return toast('email is not valid')
        elif not password:
            return toast('password is not valid')
        val = self.data.select_by_email(email=email)
        if val is None:
            self.p_obj.add_email(email)
            self.p_obj.add_password(password)
            self.data.add_entry(self.p_obj)
            self.current_screen = "dashboard"
            self.root.current = self.current_screen
        else:
            return toast('already exists !!')
        return toast('registered successfully !!')
        

    def validate(self):
        email= self.root.get_screen('signup').ids.email_signup.text
        password= self.root.get_screen('signup').ids.password_signup.text
        print(email)
        print(password)
        if not email and not password:
            return toast('email and password are not provided.')
        elif not email:
            return toast('email is not valid')
        elif not password:
            return toast('password is not valid')
        val = self.data.select_by_email(email=email)
        real_email, real_pass = [val, ('', '')][val is None]
        if real_email != email:
            toast('You are not registered !!')
        elif real_pass != password:
            toast('Incorrect Password !!')
        else:
            toast('login successfull !!')
            self.current_screen = "dashboard"
            self.root.current = self.current_screen
            
            
    

MyApp().run()