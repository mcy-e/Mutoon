from kivy.config import Config

Config.set('graphics','width','360')

Config.set('graphics','height','640')
from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.core.text import LabelBase
from kivy.properties import StringProperty,BooleanProperty,ObjectProperty,DictProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.button import MDFloatingActionButtonSpeedDial,MDIconButton
#* external libs (modules perhaps i say "with a british accent")
import arabic_reshaper
from bidi.algorithm import get_display
from functools import partial

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

class Options(MDIconButton):

    is_pressed=BooleanProperty(False)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon='dots-horizontal'
        # self.options=App.get_running_app().root.ids.nav_bar.ids.options_grid
        #* remove that boring ripple effect
        self.ripple_alpha=0
        
        
    def _start_animation(self, animation, widget, dt):
        animation.start(widget)
        widget.disabled= not widget.disabled

    def hide(self):
        options=App.get_running_app().root.ids.nav_bar.ids.options_grid
        delay=1

        for child in options.children:
            if self!= child:
               
               fade= Animation(opacity=0,duration=1/5,t='out_circ')
               pos=Animation(pos_hint={'center_x':0.5},d=0.3)
               final=fade+pos

               Clock.schedule_once(partial(self._start_animation, final, child), delay * 0.05)
               delay+=1

    def show(self):
        delay=1
        options=App.get_running_app().root.ids.nav_bar.ids.options_grid

        for child in reversed(options.children):
            if self!= child:

               fade= Animation(opacity=1,duration=1/5,t='in_circ')
               pos=Animation(pos_hint={'x':0.5*delay},d=0.3)
               final=fade+pos
               Clock.schedule_once(partial(self._start_animation, final, child), delay * 0.05)
               delay+=1

    def Show_Options(self):

        if self.is_pressed: 
            #* animate the options tab
            anim=Animation(opacity=0,duration=1/10,t='in_circ') 
            anim.bind(on_complete=lambda *args: self._set_icon('dots-vertical'))
            anim.start(self)
            self.show()
        else:
            anim=Animation(opacity=0,duration=1/10,t='in_circ') 
            anim.bind(on_complete=lambda *args: self._set_icon('dots-horizontal'))
            anim.start(self)
            self.hide()

    def _set_icon(self, new_icon):
        self.icon = new_icon
        Animation(opacity=1, duration=1/10,t='out_circ').start(self)




class MainScreen(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
class BottomNavBar(MDBoxLayout):
    dark_mode=BooleanProperty(True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
     
    try:    
        def Switch_mode(self):
            theme_modes=self.ids.D_L_mode

            if self.dark_mode:
                App.get_running_app().theme_cls.theme_style='Dark'
                theme_modes.icon='moon-waning-crescent'
            else:
                App.get_running_app().theme_cls.theme_style='Light'
                theme_modes.icon='weather-sunny'
    except (AttributeError) as e :
        print(f"Error {e}")        
       


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
    dark_app=BooleanProperty()
    checking=ObjectProperty(None)
    def on_start(self):
        self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palate="Teal"
        self.checking=Clock.schedule_once(self.link_mode,1/60)
    
    def on_dark_mode_change(self,instance, value):
        self.dark_app=value

    def link_mode(self,dt):
        try:
            nav=App.get_running_app().root.ids.nav_bar
            nav.bind(dark_mode=self.on_dark_mode_change)

        except AttributeError as e:
            print(f"Error :{e}")
        



if __name__=='__main__':
    app().run()
