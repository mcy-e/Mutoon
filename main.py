from kivy.config import Config

Config.set('graphics','width','360')

Config.set('graphics','height','640')
from kivy.core.window import Window
from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivy.metrics import dp 
from kivy.core.text import LabelBase
from kivy.properties import StringProperty,BooleanProperty,ObjectProperty,DictProperty,ListProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.uix.screenmanager import FadeTransition 
from kivymd.uix.carousel import MDCarousel
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDIconButton,MDRectangleFlatButton
from kivy.uix.modalview import ModalView
#* external libs (modules perhaps i say "with a british accent")
import arabic_reshaper
from bidi.algorithm import get_display
from functools import partial
import random
from pathlib import Path
import json
import logging

logging.basicConfig(level=logging.debug)
#*register the font for easy access
LabelBase.register(name="arb_fnt", fn_regular="fonts/NotoKufiArabic-Black.ttf")

#! Global Functions
#* function to formalize the arabic text so you can display
def Arabic_txt_to_desplay(raw_text :str) -> str:
    reshaped = arabic_reshaper.reshape(raw_text)
    bidi_text = get_display(reshaped)
    return bidi_text



   
#? popups
class Info_popup(ModalView):
    close_txt_raw = StringProperty("غلق")
    info_txt_raw = StringProperty(
        "تم صنع هذا البرنامج\n"
        "لتسهيل الحصول على المتون\n"
        "وتصفحها، خاصة متون التجويد\n"
        "هذه نسخة تجريبية\n"
        "مازالت قيد التطوير"
    )

    close_txt = StringProperty()
    info_txt = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.close_txt = Arabic_txt_to_desplay(self.close_txt_raw)
        self.info_txt = Arabic_txt_to_desplay(self.info_txt_raw)

class Socials_popup(ModalView):
    close_txt_raw = StringProperty("غلق")
    main_txt_raw = StringProperty("وسائل التواصل الخاصة بصاحب التطبيق:")

    close_txt = StringProperty()
    main_txt = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.close_txt = Arabic_txt_to_desplay(self.close_txt_raw)
        self.main_txt = Arabic_txt_to_desplay(self.main_txt_raw)

    import sys

    if sys.platform == "android":
        from jnius import autoclass

        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')

        def routes(self,url):
            intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
            currentActivity = PythonActivity.mActivity
            currentActivity.startActivity(intent)
    else:
        

        def routes(self,url):
            import webbrowser
            webbrowser.open(url)

class Gift_popup(ModalView):
    close_txt_raw = StringProperty("غلق")
    main_txt_raw = StringProperty("فضلا منكم نسأل الدعاء لنا\n و للأمة الإسلامية")
    
    ad3iya = ListProperty( [
    "اللهم آتنا في الدنيا حسنة وفي\nالآخرة حسنة وقنا عذاب النار",
    "اللهم اغفر لي ولوالدي وللمؤمنين\nوالمؤمنات يوم يقوم الحساب",
    "اللهم إني أسألك الهدى والتقى\nوالعفاف والغنى",
    "اللهم يا مصرف القلوب صرف قلوبنا\nعلى طاعتك",
    "رب اغفر لي وتب علي إنك أنت\nالتواب الرحيم",
    "اللهم ثبت قلبي على دينك\nوطاعتك",
    "اللهم إني أسألك الجنة وأعوذ\nبك من النار",
    "اللهم إني أسألك من الخير كله\nعاجله وآجله",
    "اللهم إني أعوذ بك من جهد البلاء\nودرك الشقاء وسوء القضاء",
    "اللهم إني أعوذ بك من الهم\nوالحزن والعجز والكسل",
    "أستغفر الله العظيم الذي لا إله\nإلا هو الحي القيوم وأتوب إليه",
    "سبحان الله وبحمده سبحان\nالله العظيم",
    "لا إله إلا الله وحده لا شريك\nله له الملك وله الحمد",
    "الحمد لله الذي بنعمته تتم\nالصالحات",
    "لا حول ولا قوة إلا بالله\nالعلي العظيم",
    "سبحان الله والحمد لله ولا إله إلا\nالله والله أكبر"
])
    
    close_txt = StringProperty()
    main_txt = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.close_txt = Arabic_txt_to_desplay(self.close_txt_raw)
        self.main_txt = Arabic_txt_to_desplay(self.main_txt_raw)
    def create(self):
        popup=Gift_popup()
        popup.Load_Dawa()
        popup.open()
    def Load_Dawa(self):
        picked_raw = random.choice(self.ad3iya)
        picked = Arabic_txt_to_desplay(picked_raw)
        self.main_txt = picked

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
            logging.error(f"Error {e}")

class Options(MDIconButton):

    is_pressed=BooleanProperty(False)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon='dots-horizontal'
        
        #* remove that boring ripple effect
        self.ripple_alpha=0
        
        
    def _start_animation(self, animation, widget, dt):
        animation.start(widget)
        widget.disabled= not widget.disabled

    def hide(self):
        options=App.get_running_app().root.ids.main_s.ids.nav_bar.ids.options_grid
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
        options=App.get_running_app().root.ids.main_s.ids.nav_bar.ids.options_grid

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
   
    mtn_active=BooleanProperty(True)
    current_tab = StringProperty("mutoon")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def set_color_delayed(self,tabed_item):
       Clock.schedule_once(lambda dt: self.set_color(tabed_item), 0)

    def set_current_tab(self, tab_name):
        if self.current_tab != tab_name:
            self.current_tab = tab_name





class Muton_Full_Widget(MDFloatLayout):
    mtn_text_raw=StringProperty("المتون")
    mtn_text=StringProperty("")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
    try:
        def on_kv_post(self, base_widget):
            self.mtn_text=Arabic_txt_to_desplay(self.mtn_text_raw)
    except Exception as e:
        logging.error(f"Error : {e}")


class Muton_btns(MDGridLayout):
    #* Arabic strings (can't be handled in the kv file)
    tohfa=StringProperty("تحفة الأطفال")
    Djazzeria=StringProperty("الجزرية")
    ibn_b=StringProperty("إبن بري")
    al_shatibiya=StringProperty("الشاطبية")
    mojmel=StringProperty("مجمل إعتقاد السلف")

    def show_loading_screen(self):
        App.get_running_app().root.ids.loading.manager.transition=FadeTransition(duration=1/10)
        App.get_running_app().root.current="loading"
    def go_to_screen(self,screen_name:str):
        try:
            if not screen_name:
                logging.error("No screen name is detected")
                raise Exception(f"No screen name found or type {type(screen_name)} missmatch")
            self.show_loading_screen()

            Clock.schedule_once(lambda dt : delayed_go_to(screen_name),0.5)        
            def delayed_go_to(name):
                App.get_running_app().root.current=name  
        except Exception as e:
            logging.error(f"Error : {e}")
    


class Explanation_of_Muton_Full_Widget(MDFloatLayout):
    mtn_text_explan_raw=StringProperty("شرح المتون")
    mtn_text_explan=StringProperty("")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
    
    try:
        def on_kv_post(self, base_widget):

            self.mtn_text_explan=Arabic_txt_to_desplay(self.mtn_text_explan_raw)
    except Exception as e:
        logging.error(f"Error : {e}")

class Explanation_of_Muton_btns(MDGridLayout):
    #* Arabic strings (can't be handled in the kv file) E stands for Explanation
    tohfa_E=StringProperty(" شرح تحفة الأطفال ")
    Djazzeria_E=StringProperty(" شرح الجزرية")
    ibn_b_E=StringProperty(" شرح إبن بري")
    al_shatibiya_E=StringProperty("شرح الشاطبية")
    mojmel_E=StringProperty("شرح المجمل ")

    def show_loading_screen(self):
        App.get_running_app().root.ids.loading.manager.transition=FadeTransition(duration=1/10)
        App.get_running_app().root.current="loading"
    def go_to_screen(self,screen_name:str):
        try:
            if not screen_name:
                logging.error("No screen name is detected")
                raise Exception(f"No screen name found or type {type(screen_name)} missmatch")
            self.show_loading_screen()

            Clock.schedule_once(lambda dt : delayed_go_to(screen_name),0.5)        
            def delayed_go_to(name):
                App.get_running_app().root.current=name  
        except Exception as e:
            logging.error(f"Error : {e}")



#*Screens init for py
class TohfaScreen(MDScreen):
    title_raw=StringProperty("تحفة الأطفال")
    sections_raw=ListProperty(['المقدمة', 'النون الساكنة والتنوين', 'الميم والنون المشددتين', 'الميم الساكنة', 'لِام آل ولِام الفعل', 'المثلين والمتقاربين والمتجانسين', 'أقسام المد', 'أحَكام المد', 'أقسام المد اللازم', 'الخاتمة'])
    copyright_raw=StringProperty("تحقيق حسن بن مصطفى بن أحمد الوراقي المصري")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fade_in=Animation(opacity=1,duration=1/5,t='in_quad')
        self.fade_out=Animation(opacity=0,duration=1/5,t='out_quad')
        self.title=Arabic_txt_to_desplay(self.title_raw)
        self.copyright=Arabic_txt_to_desplay(self.copyright_raw)
        self.sections=[]
        for sec in self.sections_raw:
            temp=Arabic_txt_to_desplay(sec)
            self.sections.append(temp)
        
        

    def fade_effect(self):
        self.back=self.ids.back_btn
        self.menu=self.ids.menu_btn
        self.title=self.ids.title
       
        self.fade_in.start(self.back)
        self.fade_in.start(self.menu)
        self.fade_in.start(self.title)
        


       
        
    def on_enter(self, *args):

        #* MAKES THE PAGE ONLY WHEN THE USER ENTERS IT
        if "page" in self.ids:  
            self.fade_effect() 
            self.ids.page.start()
            
    def on_leave(self, *args):
        #* the screen is inactive no need for the widget
        if "page" in self.ids:
            
            
            self.ids.page.checking.cancel()
            
class Tohfa_pages(MDCarousel):
    checking=ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction='left' 
        self.built=False
        self.img_path ="PDF_Images/To7fa"
       

    def start(self):
        if not self.built:

            self.page_index = 1
            self.batch_size = 4
            self.total_pages = 4 
            Clock.schedule_once(lambda dt: self.load_next_pages(), 0)
            
            self.checking=Clock.schedule_interval(self.check_if_at_end, 0.5)
            self.built=True
    
    def check_if_at_end(self, dt):
        if self.index >= len(self.slides) - 1:
            self.load_next_pages()

    def load_next_pages(self):
        try:
            if self.page_index > self.total_pages:
                return  

            self.end_page = min(self.page_index + self.batch_size - 1, self.total_pages)

            for i in range(self.page_index, self.end_page + 1): 
                path = Path(f'{self.img_path}/page_{i:03d}.png')
                if path.exists():
                    slide = MDFloatLayout(size_hint=(1, 1))
                    img = Image(
                        source=str(path),
                        allow_stretch=True,
                        keep_ratio=False,
                        size_hint=(1, 1),
                        pos_hint={"center_x": 0.5, "center_y": 0.5}
                    )
                    slide.add_widget(img)
                    self.add_widget(slide)
                    logging.debug(f"Added slide {i}")
                else:
                    logging.error(f"Page not found: {path}")

            logging.debug("Successfully loaded pages")
            self.page_index = self.end_page + 1 

        except Exception as e:
            logging.error(f"Error: {e}")
    def load_section(self, page_number):
        index = page_number - 1

        while index >= len(self.slides) and self.page_index <= self.total_pages:
            self.load_next_pages()  

        if 0 <= index < len(self.slides):
            self.index = index
        else:
            logging.error(f"Page {page_number} cannot be loaded.")


class MojmelScreen(MDScreen):
    title_raw=StringProperty("مجمل إعتقاد السلف")
    sections_raw=ListProperty(["مقدمة","العقائد"])
    copyright_raw=StringProperty("نظم الشيخ محمد سالم بن محمد علي ابن عبد الودود الهاشمي الشنقبطي")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fade_in=Animation(opacity=1,duration=1/5,t='in_quad')
        self.fade_out=Animation(opacity=0,duration=1/5,t='out_quad')
        self.title=Arabic_txt_to_desplay(self.title_raw)
        self.copyright=Arabic_txt_to_desplay(self.copyright_raw)
        self.sections=[]
        for sec in self.sections_raw:
            temp=Arabic_txt_to_desplay(sec)
            self.sections.append(temp)
        
        

    def fade_effect(self):
        self.back=self.ids.back_btn
        self.menu=self.ids.menu_btn
        self.title=self.ids.title
       
        self.fade_in.start(self.back)
        self.fade_in.start(self.menu)
        self.fade_in.start(self.title)
        


       
        
    def on_enter(self, *args):

        #* MAKES THE PAGE ONLY WHEN THE USER ENTERS IT
        if "page" in self.ids:  
            self.fade_effect() 
            self.ids.page.start()
            
    def on_leave(self, *args):
        #* the screen is inactive no need for the widget
        if "page" in self.ids:
            
            
            self.ids.page.checking.cancel()
            
class Mojmel_pages(MDCarousel):
    checking=ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction='left' 
        self.built=False
        self.img_path ="PDF_Images/mojmel"
    
       

    def start(self):
        if not self.built:

            self.page_index = 1
            self.batch_size = 5
            self.total_pages = 23
            Clock.schedule_once(lambda dt: self.load_next_pages(), 0)
            self.checking=Clock.schedule_interval(self.check_if_at_end, 0.5)
            self.built=True
    
    def check_if_at_end(self, dt):
        if self.index >= len(self.slides) - 1:
            self.load_next_pages()

    def load_next_pages(self):
        try:
            if self.page_index > self.total_pages:
                return  

            self.end_page = min(self.page_index + self.batch_size - 1, self.total_pages)

            for i in range(self.page_index, self.end_page + 1): 
                path = Path(f'{self.img_path}/page_{i:03d}.png')
                if path.exists():
                    slide = MDFloatLayout(size_hint=(1, 1))
                    img = Image(
                        source=str(path),
                        allow_stretch=True,
                        keep_ratio=False,
                        size_hint=(1, 1),
                        pos_hint={"center_x": 0.5, "center_y": 0.5}
                    )
                    slide.add_widget(img)
                    self.add_widget(slide)
                    logging.debug(f"Added slide {i}")
                else:
                    logging.error(f"Page not found: {path}")

            logging.debug("Successfully loaded pages")
            self.page_index = self.end_page + 1 

        except Exception as e:
            logging.error(f"Error: {e}")
    def load_section(self, page_number):
        index = page_number - 1

        while index >= len(self.slides) and self.page_index <= self.total_pages:
            self.load_next_pages()  

        if 0 <= index < len(self.slides):
            self.index = index
        else:
            logging.error(f"Page {page_number} cannot be loaded.")

class DjScreen(MDScreen):
    title_raw=StringProperty("المقدمة الجزرية")
    sections_raw=ListProperty( [
        "المقدمة",
        "مخارج الحروف",
        "صفات الحروف",
        "التجويد",
        "تنبيهات",
        "الراءات",
        "اللامات وأحكام",
        "الضاد والظاء",
        "النون والميم المشددتان",
        "النون الساكنة والتنوين",
        "المد",
        "الوقف والابتداء",
        "المقطوع والموصول",
        "التاءات",
        "همز الوصل",
        "الوقف على أواخر الكلم"
    ])
    copyright_raw=StringProperty("تحقيق أيمن رشدي سويد")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fade_in=Animation(opacity=1,duration=1/5,t='in_quad')
        self.fade_out=Animation(opacity=0,duration=1/5,t='out_quad')
        self.title=Arabic_txt_to_desplay(self.title_raw)
        self.copyright=Arabic_txt_to_desplay(self.copyright_raw)
        self.sections=[]
        for sec in self.sections_raw:
            temp=Arabic_txt_to_desplay(sec)
            self.sections.append(temp)
        
        

    def fade_effect(self):
        self.back=self.ids.back_btn
        self.menu=self.ids.menu_btn
        self.title=self.ids.title
       
        self.fade_in.start(self.back)
        self.fade_in.start(self.menu)
        self.fade_in.start(self.title)
        


       
        
    def on_enter(self, *args):

        #* MAKES THE PAGE ONLY WHEN THE USER ENTERS IT
        if "page" in self.ids:  
            self.fade_effect() 
            self.ids.page.start()
            
    def on_leave(self, *args):
        #* the screen is inactive no need for the widget
        if "page" in self.ids:
            
            
            self.ids.page.checking.cancel()
            
class Dj_pages(MDCarousel):
    checking=ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction='left' 
        self.built=False
        self.img_path ="PDF_Images/Dj"
      
       

    def start(self):
        if not self.built:

            self.page_index = 1
            self.batch_size = 5
            self.total_pages = 11
            Clock.schedule_once(lambda dt: self.load_next_pages(), 0)
            self.checking=Clock.schedule_interval(self.check_if_at_end, 0.5)
            self.built=True
   
    def check_if_at_end(self, dt):
        if self.index >= len(self.slides) - 1:
            self.load_next_pages()

    def load_next_pages(self):
        try:
            if self.page_index > self.total_pages:
                return  

            self.end_page = min(self.page_index + self.batch_size - 1, self.total_pages)

            for i in range(self.page_index, self.end_page + 1): 
                path = Path(f'{self.img_path}/page_{i:03d}.png')
                if path.exists():
                    slide = MDFloatLayout(size_hint=(1, 1))
                    img = Image(
                        source=str(path),
                        allow_stretch=True,
                        keep_ratio=False,
                        size_hint=(1, 1),
                        pos_hint={"center_x": 0.5, "center_y": 0.5}
                    )
                    slide.add_widget(img)
                    self.add_widget(slide)
                    logging.debug(f"Added slide {i}")
                else:
                    logging.error(f"Page not found: {path}")

            logging.debug("Successfully loaded pages")
            self.page_index = self.end_page + 1 

        except Exception as e:
            logging.error(f"Error: {e}")
    def load_section(self, page_number):
        index = page_number - 1

        while index >= len(self.slides) and self.page_index <= self.total_pages:
            self.load_next_pages()  

        if 0 <= index < len(self.slides):
            self.index = index
        else:
            logging.error(f"Page {page_number} cannot be loaded.")


class IBN_BScreen(MDScreen):
    title_raw=StringProperty("الدرر اللوامع")
    sections_raw=ListProperty([
        "المقدمة",
        "الإستعاذة",
        "البسملة",
        "ميم الجمع",
        "هاء الضمير",
        "الممدود و المقصور",
        "التحقيق و التسهيل",
        "الإبدال",
        "أحكام نقل الحركة",
        "الإظهار و الإدغام",
        "إدغام النون و التنوين",
        "المفتوح و الممال",
        "الراءات",
        "أحكام اللام",
        "الإشمام و الروم",
        "ياءات الإضافة",
        "زوائد الياءات",
        "فرش الحروف",
        "مخارج الحروف",
        "صفات الحروف",
        "خاتمة"
    ])
    copyright_raw=StringProperty("تحقيق سليم بن محمد بن يوسف ربيع الجزائري")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fade_in=Animation(opacity=1,duration=1/5,t='in_quad')
        self.fade_out=Animation(opacity=0,duration=1/5,t='out_quad')
        self.title=Arabic_txt_to_desplay(self.title_raw)
        self.copyright=Arabic_txt_to_desplay(self.copyright_raw)
        self.sections=[]
        for sec in self.sections_raw:
            temp=Arabic_txt_to_desplay(sec)
            self.sections.append(temp)
        
        

    def fade_effect(self):
        self.back=self.ids.back_btn
        self.menu=self.ids.menu_btn
        self.title=self.ids.title
       
        self.fade_in.start(self.back)
        self.fade_in.start(self.menu)
        self.fade_in.start(self.title)

      
        


       
        
    def on_enter(self, *args):
            
        #* MAKES THE PAGE ONLY WHEN THE USER ENTERS IT
        if "page" in self.ids: 
            self.fade_effect() 
            self.ids.page.start()

            
    def on_leave(self, *args):
        #* the screen is inactive no need for the widget
        if "page" in self.ids:
            
            
            if self.ids.page.checking:
                self.ids.page.checking.cancel()
            
class IBN_B_pages(MDCarousel):
    checking=ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction='left' 
        self.built=False
        self.img_path ="PDF_Images/ibn_b"
        self.page_index = 1
        self.total_pages = 47
       

    def start(self):
        if not self.built:
            self.page_index = 1
            self.total_pages = 47
            self.batch_size =47
            self.load_next_pages()
            self.built = True
    def check_if_at_end(self, dt):
        if self.index >= len(self.slides) - 1:
            self.load_next_pages()

    def load_next_pages(self):
        try:
            if self.page_index > self.total_pages:
                return  

            self.end_page = min(self.page_index + self.batch_size - 1, self.total_pages)

            for i in range(self.page_index, self.end_page + 1): 
                path = Path(f'{self.img_path}/page_{i:03d}.png')
                if path.exists():
                    slide = MDFloatLayout(size_hint=(1, 1))
                    img = Image(
                        source=str(path),
                        allow_stretch=True,
                        keep_ratio=False,
                        size_hint=(1, 1),
                        pos_hint={"center_x": 0.5, "center_y": 0.5}
                    )
                    slide.add_widget(img)
                    self.add_widget(slide)
                    logging.debug(f"Added slide {i}")
                else:
                    logging.error(f"Page not found: {path}")

            logging.debug("Successfully loaded pages")
            self.page_index = self.end_page + 1 

        except Exception as e:
            logging.error(f"Error: {e}")
    def load_section(self, page_number):
        index = page_number - 1

        while index >= len(self.slides) and self.page_index <= self.total_pages:
            self.load_next_pages()  

        if 0 <= index < len(self.slides):
            self.index = index
        else:
            logging.error(f"Page {page_number} cannot be loaded.")



class AL_SHATScreen(MDScreen):
    title_raw=StringProperty("الشاطبية")
    sections_raw=ListProperty([
        "المقدمة",
        "الاستعاذة",
        "البسملة",
        "أم القرآن",
        "الإدغام الكبير",
        "إدغام المتقاربين",
        "هاء الكناية",
        "المد والقصر",
        "الهمزتان بكلمة",
        "الهمزتان بكلمتين",
        "الهمز المفرد",
        "نقل حركة الهمز",
        "وقف حمزة وهشام",
        "الإظهار والإدغام",
        "إدغام إذ وقد",
        "الحروف المتقاربة",
        "النون الساكنة والتنوين",#16
        "الفتح والإمالة",#17
        "إمالة هاء التأنيث",
        "الراءات",#19
        "اللامات",#20
        "الوقف على أواخر الكلم",
        "الوقف على الرسم",
        "ياء الإضافة",
        "ياءات الزوائد",
        "فرش الحروف",
        "التكبير",
        "المخارج والصفات",
        "خاتمة"
    ])
    copyright_raw=StringProperty("محمد تميم الزعبي")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fade_in=Animation(opacity=1,duration=1/5,t='in_quad')
        self.fade_out=Animation(opacity=0,duration=1/5,t='out_quad')
        self.title=Arabic_txt_to_desplay(self.title_raw)
        self.copyright=Arabic_txt_to_desplay(self.copyright_raw)
        self.sections=[]
        for sec in self.sections_raw:
            temp=Arabic_txt_to_desplay(sec)
            self.sections.append(temp)
        
        

    def fade_effect(self):
        self.back=self.ids.back_btn
        self.menu=self.ids.menu_btn
        self.title=self.ids.title
       
        self.fade_in.start(self.back)
        self.fade_in.start(self.menu)
        self.fade_in.start(self.title)

      
        


       
        
    def on_enter(self, *args):
            
        #* MAKES THE PAGE ONLY WHEN THE USER ENTERS IT
        if "page" in self.ids: 
            self.fade_effect() 
            self.ids.page.start()

            
    def on_leave(self, *args):
        #* the screen is inactive no need for the widget
        if "page" in self.ids:
            
            
            self.ids.page.checking.cancel()
            
class AL_SHAT_pages(MDCarousel):
    checking=ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction='left' 
        self.built=False
        self.img_path ="PDF_Images/al_shat"
        self.page_index = 1
        self.total_pages = 95
        
       

    def start(self):
        if not self.built:
            self.page_index = 1
            self.total_pages = 95
            self.batch_size =90
            self.load_next_pages()
            self.checking = Clock.schedule_interval(self.check_if_at_end, 0.5)
            self.built = True
            
    def check_if_at_end(self, dt):
        if self.index >= len(self.slides) - 1:
            self.load_next_pages()

    def load_next_pages(self):
        try:
            if self.page_index > self.total_pages:
                return  

            self.end_page = min(self.page_index + self.batch_size - 1, self.total_pages)

            for i in range(self.page_index, self.end_page + 1): 
                path = Path(f'{self.img_path}/page_{i:03d}.png')
                if path.exists():
                    slide = MDFloatLayout(size_hint=(1, 1))
                    img = Image(
                        source=str(path),
                        allow_stretch=True,
                        keep_ratio=False,
                        size_hint=(1, 1),
                        pos_hint={"center_x": 0.5, "center_y": 0.5}
                    )
                    slide.add_widget(img)
                    self.add_widget(slide)
                    logging.debug(f"Added slide {i}")
                else:
                    logging.error(f"Page not found: {path}")

            logging.debug("Successfully loaded pages")
            self.page_index = self.end_page + 1 

        except Exception as e:
            logging.error(f"Error: {e}")
    def load_section(self, page_number :int):
        index = page_number - 1

        while index >= len(self.slides) and self.page_index <= self.total_pages:
            self.load_next_pages()  

        if 0 <= index < len(self.slides):
            self.index = index
        else:
            logging.error(f"Page {page_number} cannot be loaded.")



#* for Explanations

class Tohfa_E_Screen(MDScreen):
    title_raw=StringProperty("شرح تحفة الاطفال")
    sections_raw=ListProperty([
        "المقدمة",
        "الفصل الأول",
        "الفصل الثاني",
        "الفصل الثالث",
        "الفصل الرابع"
    ])
    copyright_raw=StringProperty("أبي حفص عمر بن أحمد الأزهري")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fade_in=Animation(opacity=1,duration=1/5,t='in_quad')
        self.fade_out=Animation(opacity=0,duration=1/5,t='out_quad')
        self.title=Arabic_txt_to_desplay(self.title_raw)
        self.copyright=Arabic_txt_to_desplay(self.copyright_raw)
        self.sections=[]
        for sec in self.sections_raw:
            temp=Arabic_txt_to_desplay(sec)
            self.sections.append(temp)
        
        

    def fade_effect(self):
        self.back=self.ids.back_btn
        self.menu=self.ids.menu_btn
        self.title=self.ids.title
       
        self.fade_in.start(self.back)
        self.fade_in.start(self.menu)
        self.fade_in.start(self.title)

      
        


       
        
    def on_enter(self, *args):
            
        #* MAKES THE PAGE ONLY WHEN THE USER ENTERS IT
        if "page" in self.ids: 
            self.fade_effect() 
            self.ids.page.start()

            
    def on_leave(self, *args):
        #* the screen is inactive no need for the widget
        if "page" in self.ids:
            
            
            self.ids.page.checking.cancel()
            
class Tohfa_E_pages(MDCarousel):
    checking=ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction='left' 
        self.built=False
        self.img_path ="PDF_Images/To7fa_E"
        self.page_index = 1
        self.total_pages = 58
        
       

    def start(self):

        if not self.built:
            self.page_index = 1
            self.total_pages = 58
            self.batch_size =58
            self.load_next_pages()
            self.checking = Clock.schedule_interval(self.check_if_at_end, 0.5)
            self.built = True
            
    def check_if_at_end(self, dt):
        if self.index >= len(self.slides) - 1:
            self.load_next_pages()

    def load_next_pages(self):
        try:
            if self.page_index > self.total_pages:
                return  

            self.end_page = min(self.page_index + self.batch_size - 1, self.total_pages)

            for i in range(self.page_index, self.end_page + 1): 
                path = Path(f'{self.img_path}/page_{i:03d}.png')
                if path.exists():
                    slide = MDFloatLayout(size_hint=(1, 1))
                    img = Image(
                        source=str(path),
                        allow_stretch=True,
                        keep_ratio=False,
                        size_hint=(1, 1),
                        pos_hint={"center_x": 0.5, "center_y": 0.5}
                    )
                    slide.add_widget(img)
                    self.add_widget(slide)
                    logging.debug(f"Added slide {i}")
                else:
                    logging.error(f"Page not found: {path}")

            logging.debug("Successfully loaded pages")
            self.page_index = self.end_page + 1 

        except Exception as e:
            logging.error(f"Error: {e}")
    def load_section(self, page_number):
        index = page_number - 1

        while index >= len(self.slides) and self.page_index <= self.total_pages:
            self.load_next_pages()  

        if 0 <= index < len(self.slides):
            self.index = index
        else:
            logging.error(f"Page {page_number} cannot be loaded.")
class Dj_E_Screen(MDScreen):
    title_raw=StringProperty("شرح الجزرية")
    sections_raw=ListProperty( [
        "مقدمة",
        "تمهيد",
        "نص المقدمة",
        "مقدمة المصنف",
        "مخارج الحروف",
        "صفات الحروف",
        "معرفة التجويد",
        "الترقيق",
        "الراءات",
        "التفخيم",
        "الإدغام",
        "الضاد و الظاء",
        "النون و الميم",
        "المد",
        "الوقف و الابتداء",
        "المقطوع و الموصول",
        "هاءات التانيث",
        "الابتداء بهمزة الوصل",
        "الوقف على أواخر الكلم",
        "خاتمة المقدمة",
        "قائمة المصادر"
    ])
    copyright_raw=StringProperty("غانم قدوري الحمد")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fade_in=Animation(opacity=1,duration=1/5,t='in_quad')
        self.fade_out=Animation(opacity=0,duration=1/5,t='out_quad')
        self.title=Arabic_txt_to_desplay(self.title_raw)
        self.copyright=Arabic_txt_to_desplay(self.copyright_raw)
        self.sections=[]
        for sec in self.sections_raw:
            temp=Arabic_txt_to_desplay(sec)
            self.sections.append(temp)
        
        

    def fade_effect(self):
        self.back=self.ids.back_btn
        self.menu=self.ids.menu_btn
        self.title=self.ids.title
       
        self.fade_in.start(self.back)
        self.fade_in.start(self.menu)
        self.fade_in.start(self.title)

      
        


       
        
    def on_enter(self, *args):
            
        #* MAKES THE PAGE ONLY WHEN THE USER ENTERS IT
        if "page" in self.ids: 
            self.fade_effect() 
            self.ids.page.start()

            
    def on_leave(self, *args):
        #* the screen is inactive no need for the widget
        if "page" in self.ids:
            
            
            if self.ids.page.checking:
                
                self.ids.page.checking.cancel()

            
class Dj_E_pages(MDCarousel):
    checking=ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction='left' 
        self.built=False
        self.img_path ="PDF_Images/Dj_E"
        self.page_index = 1
        self.total_pages = 159
        
       

    def start(self):
        if self.img_path=="":
            return
        if not self.built:
            self.page_index = 1
            self.total_pages = 159
            self.batch_size =159
            self.load_next_pages()
            self.checking = Clock.schedule_interval(self.check_if_at_end, 0.5)
            self.built = True
            
    def check_if_at_end(self, dt):
        if self.index >= len(self.slides) - 1:
            self.load_next_pages()

    def load_next_pages(self):
        try:
            if self.page_index > self.total_pages:
                return  

            self.end_page = min(self.page_index + self.batch_size - 1, self.total_pages)

            for i in range(self.page_index, self.end_page + 1): 
                path = Path(f'{self.img_path}/page_{i:03d}.png')
                if path.exists():
                    slide = MDFloatLayout(size_hint=(1, 1))
                    img = Image(
                        source=str(path),
                        allow_stretch=True,
                        keep_ratio=False,
                        size_hint=(1, 1),
                        pos_hint={"center_x": 0.5, "center_y": 0.5}
                    )
                    slide.add_widget(img)
                    self.add_widget(slide)
                    logging.debug(f"Added slide {i}")
                else:
                    logging.error(f"Page not found: {path}")

            logging.debug("Successfully loaded pages")
            self.page_index = self.end_page + 1 

        except Exception as e:
            logging.error(f"Error: {e}")
    def load_section(self, page_number):
        index = page_number - 1

        while index >= len(self.slides) and self.page_index <= self.total_pages:
            self.load_next_pages()  

        if 0 <= index < len(self.slides):
            self.index = index
        else:
            logging.error(f"Page {page_number} cannot be loaded.")


#* not added
class IBN_B_E_Screen(MDScreen):
    title_raw=StringProperty("شرح الدرر اللوامع")
    sections_raw=ListProperty()
    copyright_raw=StringProperty("")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fade_in=Animation(opacity=1,duration=1/5,t='in_quad')
        self.fade_out=Animation(opacity=0,duration=1/5,t='out_quad')
        self.title=Arabic_txt_to_desplay(self.title_raw)
        self.copyright=Arabic_txt_to_desplay(self.copyright_raw)
        self.sections=[]
        for sec in self.sections_raw:
            temp=Arabic_txt_to_desplay(sec)
            self.sections.append(temp)
        
        

    def fade_effect(self):
        self.back=self.ids.back_btn
        self.menu=self.ids.menu_btn
        self.title=self.ids.title
       
        self.fade_in.start(self.back)
        self.fade_in.start(self.menu)
        self.fade_in.start(self.title)

      
        


       
        
    def on_enter(self, *args):
            
        #* MAKES THE PAGE ONLY WHEN THE USER ENTERS IT
        if "page" in self.ids: 
            self.fade_effect() 
            self.ids.page.start()

            
    def on_leave(self, *args):
        #* the screen is inactive no need for the widget
        if "page" in self.ids:
            
            
            if self.ids.page.checking:
                
                self.ids.page.checking.cancel()
            
            
class IBN_B_E_pages(MDCarousel):
    checking=ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction='left' 
        self.built=False
        self.img_path =""
        self.pag_index = 1
        self.total_pages = 58
        
       

    def start(self):
        if not self.img_path:   
            return
        if not self.built:
            self.page_index = 1
            self.total_pages = 58
            self.batch_size =58
            self.load_next_pages()
            self.checking = Clock.schedule_interval(self.check_if_at_end, 0.5)
            self.built = True
            
    def check_if_at_end(self, dt):
        if self.index >= len(self.slides) - 1:
            self.load_next_pages()

    def load_next_pages(self):
        try:
            if self.page_index > self.total_pages:
                return  

            self.end_page = min(self.page_index + self.batch_size - 1, self.total_pages)

            for i in range(self.page_index, self.end_page + 1): 
                path = Path(f'{self.img_path}/page_{i:03d}.png')
                if path.exists():
                    slide = MDFloatLayout(size_hint=(1, 1))
                    img = Image(
                        source=str(path),
                        allow_stretch=True,
                        keep_ratio=False,
                        size_hint=(1, 1),
                        pos_hint={"center_x": 0.5, "center_y": 0.5}
                    )
                    slide.add_widget(img)
                    self.add_widget(slide)
                    logging.debug(f"Added slide {i}")
                else:
                    logging.error(f"Page not found: {path}")

            logging.debug("Successfully loaded pages")
            self.page_index = self.end_page + 1 

        except Exception as e:
            logging.error(f"Error: {e}")
    def load_section(self, page_number):
        index = page_number - 1

        while index >= len(self.slides) and self.page_index <= self.total_pages:
            self.load_next_pages()  

        if 0 <= index < len(self.slides):
            self.index = index
        else:
            logging.error(f"Page {page_number} cannot be loaded.")

#* not added 
class AL_SHAT_E_Screen(MDScreen):
    title_raw=StringProperty("شرح الشاطبية")
    sections_raw=ListProperty()
    copyright_raw=StringProperty("")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fade_in=Animation(opacity=1,duration=1/5,t='in_quad')
        self.fade_out=Animation(opacity=0,duration=1/5,t='out_quad')
        self.title=Arabic_txt_to_desplay(self.title_raw)
        self.copyright=Arabic_txt_to_desplay(self.copyright_raw)
        self.sections=[]
        for sec in self.sections_raw:
            temp=Arabic_txt_to_desplay(sec)
            self.sections.append(temp)
        
        

    def fade_effect(self):
        self.back=self.ids.back_btn
        self.menu=self.ids.menu_btn
        self.title=self.ids.title
       
        self.fade_in.start(self.back)
        self.fade_in.start(self.menu)
        self.fade_in.start(self.title)

      
        


       
        
    def on_enter(self, *args):
            
        #* MAKES THE PAGE ONLY WHEN THE USER ENTERS IT
        if "page" in self.ids: 
            self.fade_effect() 
            
            self.ids.page.start()

            
    def on_leave(self, *args):
        #* the screen is inactive no need for the widget
        if "page" in self.ids:
            
            
            if self.ids.page.checking:
                
                self.ids.page.checking.cancel()
            
class AL_SHAT_E_pages(MDCarousel):
    checking=ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction='left' 
        self.built=False
        self.img_path =""
        self.pag_index = 1
        self.total_pages = 58
        
       

    def start(self):
        if self.img_path=="":
          return
        if not self.built:
            self.page_index = 1
            self.total_pages = 58
            self.batch_size =58
            self.load_next_pages()
            self.checking = Clock.schedule_interval(self.check_if_at_end, 0.5)
            self.built = True
            
    def check_if_at_end(self, dt):
        if self.index >= len(self.slides) - 1:
            self.load_next_pages()

    def load_next_pages(self):
        try:
            if self.page_index > self.total_pages:
                return  

            self.end_page = min(self.page_index + self.batch_size - 1, self.total_pages)

            for i in range(self.page_index, self.end_page + 1): 
                path = Path(f'{self.img_path}/page_{i:03d}.png')
                if path.exists():
                    slide = MDFloatLayout(size_hint=(1, 1))
                    img = Image(
                        source=str(path),
                        allow_stretch=True,
                        keep_ratio=False,
                        size_hint=(1, 1),
                        pos_hint={"center_x": 0.5, "center_y": 0.5}
                    )
                    slide.add_widget(img)
                    self.add_widget(slide)
                    logging.debug(f"Added slide {i}")
                else:
                    logging.error(f"Page not found: {path}")

            logging.debug("Successfully loaded pages")
            self.page_index = self.end_page + 1 

        except Exception as e:
            logging.error(f"Error: {e}")
    def load_section(self, page_number):
        index = page_number - 1

        while index >= len(self.slides) and self.page_index <= self.total_pages:
            self.load_next_pages()  

        if 0 <= index < len(self.slides):
            self.index = index
        else:
            logging.error(f"Page {page_number} cannot be loaded.")


class Mojmel_E_Screen(MDScreen):
    title_raw=StringProperty("شرح المجمل")
    sections_raw=ListProperty([
    "المقدّمة",
    "ترجمة الناظم",
    "ترجمة الشارح",
    "عملي في الكتاب",
    "مجمل اعتقاد السلف",
    "الشرح والبسملة",
    "أصل الناظم",
    "أسماء النبي",
    "آل النبي",
    "إطلاقات العبودية",
    "اشتقاق اسم الله",
    "القدر ومراتبه",
    "أقسام القدر",
    "الإرادة: تكوينية وتشريعية",
    "الخلاف في خلق الأفعال",
    "مذهب الكسب",
    "القول الراجح في الأفعال",
    "التخيير والتسيير",
    "الإرادتين وأفعال العباد",
    "حكمة الله",
    "خلق الله بـ(كن)",
    "قاعدة التسليم",
    "بطلان وجوب سبق الشك",
    "خلق الأفعال",
    "أسباب القدر",
    "أحدية الله وصمديته",
    "إلحاد الاتحاد",
    "نفي المماثلة لا نفي الصفات",
    "صفات أهل السنة",
    "إمرار نصوص الصفات",
    "منهج السلف",
    "التعبير بالنفس",
    "لفظ الذات",
    "القول في الصفات كالذات",
    "نفي الكيف",
    "القول في بعض الصفات",
    "باب الصفات الإلهية",
    "المنهج الصحيح",
    "صفات فعلية",
    "صفة الإتيان",
    "صفة الواسع",
    "إثبات اليد ومباينتها",
    "رؤية الله: الدنيا والآخرة",
    "السمع والبصر",
    "صفة المحبة",
    "صفات العجب والضحك",
    "صفات الرضى والاستجابة",
    "الغضب",
    "البغض",
    "الطمس",
    "الطبع والختم على القلوب",
    "القبض والبسط",
    "الإعطاء والمنع",
    "الخافض الرافع",
    "المعز والمذل",
    "يكره ويمقت",
    "يهدي ويضل",
    "إقبال الله وإعراضه",
    "أقسام التوبة",
    "الرحمة",
    "الأخذ",
    "إطعام الخلق",
    "الغيرة",
    "الاستحياء",
    "صفة الأذن",
    "أفعال الله بمشيئته",
    "مشيئة العباد",
    "تنزيه عن الضلال",
    "تنزيه عن الظلم",
    "نفي المعين والظهير",
    "نفي العجز",
    "كلام الله غير مخلوق",
    "النسخ",
    "إثبات الكلام",
    "الكلام التكويني والتشريعي",
    "إثبات السكوت",
    "إحاطة الله",
    "إثبات الوجه",
    "الاستواء",
    "نفي التشبيه",
    "إثبات النزول",
    "إثبات العلو",
    "تفصيل الكلام في الجهة",
    "إثبات الاصطفاء",
    "الكتب المنزلة",
    "القرآن كلام الله",
    "الصوت والحرف",
    "تنزيه كلام الله",
    "بطلان قياس المماثلة",
    "تكليم موسى",
    "إبراهيم خليلا",
    "تأويل ما يوهم النقص",
    "أسماء الله الحسنى",
    "توقيفية الأسماء",
    "التسعة والتسعين",
    "اسم الله الأعظم",
    "منهج السلف في الصفات",
    "تعريف الشرك",
    "تحقيق التوحيد",
    "اتباع الأحوط",
    "التوسل بالنبي",
    "التعبيد في الأسماء",
    "النذر لغير الله",
    "التمسح بالقبور",
    "العبادة بشرعه",
    "توحيد الربوبية",
    "دعاء غير الله",
    "تعريف الإيمان",
    "الأعمال والإيمان",
    "زيادة الإيمان",
    "نقصان الإيمان",
    "الإيمان بالوحي",
    "الإيمان بالكتب",
    "الإيمان بالملائكة",
    "الإيمان بالرسل",
    "عدد الرسل",
    "خاتم النبيين",
    "تأييد المعجزات",
    "معجزة القرآن",
    "الشفاعة الكبرى",
    "شهادة محمد رسول الله",
    "السنة والقرآن",
    "الإيمان باليوم الآخر",
    "القبر أول المنازل",
    "الساعة وأشراطها",
    "البعث وأدلته",
    "مشاهد اليوم الآخر",
    "الصراط والجنة والنار",
    "الكتابة من مراتب القدر",
    "قائمة المصادر",
    "فهرس الموضوعات"
])
    copyright_raw=StringProperty("محمد حسن ولد الددو الشنقيطي")
    page_numbers = ListProperty([
    9, 11, 13, 15, 17, 25, 26, 27, 28, 28, 33, 36, 37, 38, 39, 40, 40, 41, 42, 42,
    43, 44, 45, 46, 46, 46, 47, 49, 50, 50, 51, 53, 54, 58, 59, 59, 61, 61, 64, 67,
    68, 69, 70, 62, 62, 63, 66, 71, 72, 73, 73, 74, 74, 75, 76, 77, 78, 79, 80, 80,
    81, 82, 83, 84, 86, 87, 89, 90, 91, 96, 97, 99, 100, 102, 103, 104, 109, 109, 110, 112,
    113, 117, 118, 119, 120, 121, 121, 122, 123, 124, 125, 126, 127, 128, 130, 114, 115, 116, 135, 136,
    137, 139, 140, 142, 144, 145, 148, 149, 150, 152, 153, 155, 132, 133, 134, 156, 157, 158, 161,
    162, 164, 166, 167, 169, 170, 171, 173, 175,177,181, 191
])
    t_color = ListProperty([0.1, 0.1, 0.1, 1])
    l_color = ListProperty([0.1, 0.1, 0.1, 1])
    app=ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fade_in=Animation(opacity=1,duration=1/5,t='in_quad')
        self.fade_out=Animation(opacity=0,duration=1/5,t='out_quad')
        self.title=Arabic_txt_to_desplay(self.title_raw)
        self.copyright=Arabic_txt_to_desplay(self.copyright_raw)
        self.sections=[]
        for sec in self.sections_raw:
            temp=Arabic_txt_to_desplay(sec)
            self.sections.append(temp)
        Clock.schedule_once(lambda dt:self.add_ferhas("dark"),0.1)


    def wrapper(self,n):
        self.ids.page.load_section(n),
        self.ids.nav_drawer.set_state("close")


    def on_kv_post(self, base_widget):

        self.app = App.get_running_app()
        self.update_colors()
        self.app.bind(dark_mode=lambda instance, value: self.update_colors())

    def update_colors(self):
        if not self.app:
            return
        if self.app.dark_mode:
            self.t_color = [0.9, 0.9, 0.9, 1]
            self.l_color = [0.9, 0.9, 0.9, 1]
        else:
            self.t_color = [0.1, 0.1, 0.1, 1]
            self.l_color = [0.1, 0.1, 0.1, 1]

        for b in self.ids.fehras.children:
            b.text_color = self.t_color
            b.line_color = self.l_color

    def add_ferhas(self, caller):
        fehras = self.ids.fehras
        if fehras.children:
            fehras.clear_widgets()

        for section, number in zip(self.sections, self.page_numbers):
            b = MDRectangleFlatButton(
                font_name="arb_fnt",
                text_color=self.t_color,
                line_color=self.l_color,
                ripple_color=(0.2, 0.2, 0.2, 0.1),
                size_hint=(1, 0.2),
                theme_text_color="Custom",
                on_release=lambda btn, n=number: self.wrapper(n)
            )
            b.text = section
            fehras.add_widget(b)
            
        

    def fade_effect(self):
        self.back=self.ids.back_btn
        self.menu=self.ids.menu_btn
        self.title=self.ids.title
       
        self.fade_in.start(self.back)
        self.fade_in.start(self.menu)
        self.fade_in.start(self.title)

      
        


       
        
    def on_enter(self, *args):
            
        #* MAKES THE PAGE ONLY WHEN THE USER ENTERS IT
        if "page" in self.ids: 
            self.fade_effect() 
            self.ids.page.start()

            
    def on_leave(self, *args):
        #* the screen is inactive no need for the widget
        if "page" in self.ids:
            
            
            if self.ids.page.checking:
                
                self.ids.page.checking.cancel()

            
class Mojmel_E_pages(MDCarousel):
    checking=ObjectProperty(None)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.direction='left' 
        self.built=False
        self.img_path ="PDF_Images/mojmel_E"

        self.page_index = 1
        self.total_pages = 198
        self.batch_size =85
        
       

    def start(self):
        if not self.img_path:
           return
        if not self.built:
            self.page_index = 1
            self.total_pages = 198
            self.batch_size =99
            self.load_next_pages()
            self.checking = Clock.schedule_interval(self.check_if_at_end, 0.5)
            self.built = True
            
    def check_if_at_end(self, dt):
        if self.index >= len(self.slides) - 1:
            self.load_next_pages()

    def load_next_pages(self):
        try:
            if self.page_index > self.total_pages:
                return  

            self.end_page = min(self.page_index + self.batch_size - 1, self.total_pages)

            for i in range(self.page_index, self.end_page + 1): 
                path = Path(f'{self.img_path}/page_{i:03d}.png')
                if path.exists():
                    slide = MDFloatLayout(size_hint=(1, 1))
                    img = Image(
                        source=str(path),
                        allow_stretch=True,
                        keep_ratio=False,
                        size_hint=(1, 1),
                        pos_hint={"center_x": 0.5, "center_y": 0.5}
                    )
                    slide.add_widget(img)
                    self.add_widget(slide)
                    logging.debug(f"Added slide {i}")
                else:
                    logging.error(f"Page not found: {path}")

            logging.debug("Successfully loaded pages")
            self.page_index = self.end_page + 1 

        except Exception as e:
            logging.error(f"Error: {e}")
    def load_section(self, page_number):
        index = page_number - 1

        while index >= len(self.slides) and self.page_index <= self.total_pages:
            self.load_next_pages()  

        if 0 <= index < len(self.slides):
            self.index = index
        else:
            logging.error(f"Page {page_number} cannot be loaded.")



class app(MDApp):
    dark_mode=BooleanProperty(True)
    checking=ObjectProperty(None)
    waiting_text_raw=StringProperty("إنتظر قليلا ...")
    not_available_raw=StringProperty("غير متاح في الوقت الراهن")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.settings_path=Path("settings.json")
        self.theme_cls.primary_palette = "Amber"
        self.theme_cls.accent_palette = "Gray"
        self.waiting_text=Arabic_txt_to_desplay(self.waiting_text_raw)
        self.not_available=Arabic_txt_to_desplay(self.not_available_raw)
        

    def load_theme(self):
        data = self.load_data()
        
        if data and "theme" in data :
            self.theme_cls.theme_style=data["theme"]
            self.dark_mode=True if data['theme']=='Dark' else False
        else:
            self.theme_cls.theme_style='Dark'
            self.dark_mode=True
        

    def on_start(self):
        self.load_theme()

    
    def load_data(self):
        if self.settings_path.exists() and self.settings_path.stat().st_size >0:
            with open(self.settings_path, "r") as f:
                return json.load(f)
        self.settings_path.touch(exist_ok=True)
        return {}  

    def save_property(self,key, value):
        data = self.load_data()
        data[key] = value  
        logging.debug("Saved Settings: " +": "+ str(data))
        with open(self.settings_path, "w") as f:
            json.dump(data, f, indent=4)

    def on_pause(self):
        if self.settings_path.exists():
            self.save_property("theme",self.theme_cls.theme_style)
        return True
        
    #*for desktop
    def on_stop(self):
        if self.settings_path.exists():
            self.save_property("theme",self.theme_cls.theme_style)


    #* Other functions

    def Switch_Theme(self):
        self.dark_mode = not self.dark_mode 
        if self.dark_mode:  
            App.get_running_app().theme_cls.theme_style='Dark'

        else:
            App.get_running_app().theme_cls.theme_style='Light'


       

if __name__=='__main__':
    app().run()
