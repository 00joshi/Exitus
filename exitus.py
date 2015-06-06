#!/usr/bin/env python3
import kivy
kivy.require('1.8.0')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, ListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.graphics import *
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from time import time
## Global Vars
guylist = list()
holelist = list()
wsize = (800,600)
nguys = 15
nholes = 10
nkills = 0
starttime = time()
Config.set('graphics', 'width', wsize[0])
Config.set('graphics', 'width', wsize[0])
Config.set('graphics', 'height', wsize[1])
class ExitusGuy(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    r = NumericProperty(0)
    def __init__(self,**kwargs):
        super(ExitusGuy, self).__init__(**kwargs)
        r = 0
        self.pos = Vector(randint(0,wsize[0]),randint(1,wsize[1]))
        self.velocity = Vector(2, 0).rotate(randint(0,360))
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
        for hole in holelist:
            if hole.disabled<=0:
                self.collision(hole)
    def collision(self, hole):
        if self.collide_widget(hole):
            if self.parent:
                self.parent.remove_widget(self)
                global nkills
                nkills+=1
                if nkills == nguys-3:
                    survival = time() -starttime
                    popup = ModalView(size_hint=(0.75, 0.5))
                    victory_label = Label(text="Game Over\n" + "%0.2f"%survival + " sec", font_size=50)
                    popup.add_widget(victory_label)
                    #popup.bind(on_dismiss=self.reset)
                    popup.open()
class ExitusHole(Widget):
     pressed = ListProperty([0,0])
     disabled = NumericProperty(0)
     r = NumericProperty(0)
     def on_touch_down(self, touch):
         if self.collide_point(*touch.pos):
             self.pressed = touch.pos
             self.disabled = 100
             return True
         return super(ExitusHole, self).on_touch_down(touch)

     def on_pressed(self, instance, pos):
#         print ('pressed at {pos}'.format(pos=pos))
         pass
     def update(self):
         if self.disabled > 0:
             self.disabled-=1
#             print(self.disabled)
     def __init__(self,**kwargs):
         super(ExitusHole, self).__init__(**kwargs)
         r = 0
         self.pos = Vector(randint(0,wsize[0]),randint(0,wsize[1]))


class ExitusGame(Widget):
    def __init__(self,**kwargs):
        super(ExitusGame, self).__init__(**kwargs)
        for i in range(0,nguys):
            guylist.append(ExitusGuy())
        for i in range(0,nholes):
            holelist.append(ExitusHole())
        for thing in guylist+holelist:
            self.add_widget(thing)
    def difficultify(self,dt):
        newhole = ExitusHole()
        self.add_widget(newhole)
        holelist.append(newhole)
    def update(self,dt):
        for guy in guylist:
            guy.move()
       # bounce off top and bottom
            if (guy.y < 0): 
                guy.velocity_y *= -1
#                guy.pos[1] = 0
            if (guy.top > self.top):
                guy.velocity_y *= -1
#                guy.pos[1] = self.height -30
       # bounce off left and right
            if (guy.x < 0):
                guy.velocity_x *= -1
#                guy.pos[0]=0
            if (guy.right > self.width):
                guy.velocity_x *= -1
#                guy.pos[0]=self.width -30
        for hole in holelist:
            hole.update()
class ExitusApp(App):
    def build(self):
        game=ExitusGame()
        Clock.schedule_interval(game.update,1.0/60.0)
        Clock.schedule_interval(game.difficultify,5)
        return game

if __name__ == '__main__':
    ExitusApp().run()
