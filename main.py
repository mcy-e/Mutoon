from kivy.config import Config

Config.set('graphics','width','360')

Config.set('graphics','height','640')

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.text import LabelBase
from kivy.properties import StringProperty,BooleanProperty,ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.clock import Clock
#* external libs (modules perhaps i say "with a british accent")
import arabic_reshaper
from bidi.algorithm import get_display


#*register the font for easy access
LabelBase.register(name="arb_fnt", fn_regular="fonts/NotoKufiArabic-Black.ttf")

#! Global Functions
#* function to formalize the arabic text so you can display
def Arabic_txt_to_desplay(raw_text):
    reshaped = arabic_reshaper.reshape(raw_text)
    bidi_text = get_display(reshaped)
    return bidi_text

#? Custom Widgets
class CustomImageButton(ButtonBehavior, BoxLayout):
    #*  special properties
    label_text = StringProperty("")
    source= StringProperty("")
    click=ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
 
    
    
    def on_kv_post(self, base_widget):
        if self.label_text:
            self.label_text=Arabic_txt_to_desplay(self.label_text)

    def on_press(self):
       
        Animation.cancel_all(self)
        Animation(opacity=0.5,d=0.1).start(self)

    def on_release(self):
        try:
            def restore_opacity(dt):
                Animation.cancel_all(self)
                Animation(opacity=1.0,d=0.1).start(self)
            if self.click:
                self.click()
                Clock.schedule_once(restore_opacity,0.1)
        except Exception as e:
            print(f"Error {e}")


class MainScreen(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
class BottomNavBar(MDBoxLayout):
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

class Muton_Full_Widget(MDFloatLayout):
    mtn_text_raw=StringProperty("المتون")
    mtn_text=StringProperty("")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    try:
        def on_kv_post(self, base_widget):
            self.mtn_text=Arabic_txt_to_desplay(self.mtn_text_raw)
    except Exception as e:
        print(f"Error : {e}")

class Muton_btns(MDGridLayout):
    #* Arabic strings (can't be handled in the kv file)
    tohfa=StringProperty("تحفة الأطفال")
    Djazzeria=StringProperty("الجزرية")


class Explanation_of_Muton_Full_Widget(MDFloatLayout):
    mtn_text_explan_raw=StringProperty("شرح المتون")
    mtn_text_explan=StringProperty("")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    try:
        def on_kv_post(self, base_widget):

            self.mtn_text_explan=Arabic_txt_to_desplay(self.mtn_text_explan_raw)
    except Exception as e:
        print(f"Error : {e}")

class Explanation_of_Muton_btns(MDGridLayout):
    pass

class app(MDApp):
    def on_start(self):
        self.theme_cls.theme_style="Dark"
       
        



if __name__=='__main__':
    app().run()
