from kivy.clock import Clock
from kivy.animation import Animation



def ReactiveFade(widget:object):
    '''
        Make the widget react by fading out and in on a certain
        Action
        
    '''
    #*prepare animations
    fade_out = Animation(opacity=0.2, d=0.1, t='out_cubic')
    fade_in = Animation(opacity=1, d=0.1, t='in_cubic')
    #*fades out -_-
    fade_out.start(widget)

    #*fades in after an amount of time to keep the animation constant
    Clock.schedule_once(lambda dt: fade_in.start(widget), 0.1)