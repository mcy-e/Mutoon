from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

class temp(MDBoxLayout):
    pass


class app(MDApp):
    def on_start(self):
        self.theme_cls="dark"



if __name__=='__main__':
    app().run()
