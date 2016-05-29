#!/usr/bin/env python3
#
# Sounds from: (CC-by-SA)
# http://www.freesound.org/people/Robinhood76/sounds/64425/
# http://www.freesound.org/people/mikaelfernstrom/sounds/68695/
# http://www.freesound.org/people/marionagm90/sounds/220660/

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
from kivy.core.audio import SoundLoader
## Global Vars
wsize = (800,600)
nguys = 10
nholes = 5
sndscream = SoundLoader.load('scream.wav')
sndhammer = SoundLoader.load('hammer.wav')
sndfanfare = SoundLoader.load('fanfare.wav')
Config.set('graphics', 'width', wsize[0])
Config.set('graphics', 'height', wsize[1])
class ExitusGuy(Widget):
    scream = sndscream
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
       # bounce off top and bottom
        if (self.y < 0): 
            self.velocity_y *= -1
        if (self.top > game.top):
            self.velocity_y *= -1
       # bounce off left and right
        if (self.x < 0):
            self.velocity_x *= -1
        if (self.right > game.width):
            self.velocity_x *= -1
        for hole in ExitusGame.holelist:
            if hole.disabled<=0:
                self.collision(hole)
    def collision(self, hole):
        if self.collide_widget(hole):
            if self.parent:
                self.scream.play()
                self.parent.remove_widget(self)
                game.scoreupdate()
class ExitusHole(Widget):
     pressed = ListProperty([0,0])
     disabled = NumericProperty(0)
     r = NumericProperty(0)
     hammer=sndhammer
     def on_touch_down(self, touch):
         if self.collide_point(*touch.pos):
             self.pressed = touch.pos
             self.disabled = 100
             self.hammer.play()
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
    fanfare = sndfanfare
    starttime = NumericProperty(0)
    guylist = list()
    holelist = list()
    nkills = NumericProperty(0)
    def GameOverNote(self,survivaltime):
        popup = ModalView(size_hint=(0.75, 0.5))
        victory_label = Label(text="Game Over\n" + "%0.2f"%survivaltime + " sec", font_size=50)
        popup.add_widget(victory_label)
        popup.bind(on_dismiss=game.reset)
        popup.bind(on_press=popup.dismiss)
        popup.open()
    def __init__(self,**kwargs):
        super(ExitusGame, self).__init__(**kwargs)
        self.starttime = time()
        self.nkills = 0
        Clock.schedule_interval(self.update,1.0/60.0)
        Clock.schedule_interval(self.difficultify,5)
        for i in range(0,nguys):
            self.guylist.append(ExitusGuy())
        for i in range(0,nholes):
            self.holelist.append(ExitusHole())
        for thing in self.guylist+self.holelist:
            self.add_widget(thing)
    def reset(self,origin):
        print("resetting")
        self.guylist.clear()
        self.holelist.clear()
        self.__init__()
    def scoreupdate(self):
        self.nkills+=1
        if self.nkills == nguys-3:
            self.gameover()
    def gameover(self):
            survival = time() - self.starttime
            self.clear_widgets()
            Clock.unschedule(self.update)
            Clock.unschedule(self.difficultify)
            self.GameOverNote(survival)
            self.fanfare.play()
    def difficultify(self,dt):
        newhole = ExitusHole()
        self.add_widget(newhole)
        self.holelist.append(newhole)
    def update(self,dt):
        for guy in self.guylist:
            guy.move()
        for hole in self.holelist:
            hole.update()

class ExitusApp(App):
    def build(self):
        game=ExitusGame()
        global game
        return game
if __name__ == '__main__':
    ExitusApp().run()
