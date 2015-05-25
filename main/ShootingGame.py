'''
Created on 2015/05/16

@author: admin
'''
from kivy.config import Config
Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '700')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from random import randint
from kivy.properties import ObjectProperty,NumericProperty
import time

class Timer(Widget):
    timer = ObjectProperty(None)
    start=time.time() 
    def update_time(self):
        self.timer = int(time.time() - self.start);
        
class Enemy(Image):    
    def init_set(self,pos,size):
        self.pos = pos
        self.size = size
    def remove(self):
            pass
    #move randomly
    def move_random(self):
            self.pos = (self.pos[0]+randint(-5,5),self.pos[1]+randint(-5,5))
            
#敵はリストで一括管理
class EnemysList():
    enemys = []
    #敵を消す(弾が当たった時とかに)
    def remove(self,enemy_id):
        pass
    #敵をつくる，ポジションと大きさを指定
    def make_enemy(self,game,enemy_pos,enemy_size):
        new_enemy = Enemy()
        new_enemy.init_set(enemy_pos, enemy_size)
        game.add_widget(new_enemy)
        self.enemys.append(new_enemy)
    #敵の動きを更新する，update中で呼ばれる(？)
    def update_enemys(self,game):
        for i in self.enemys:
            i.move_random()
            
class ShootingGame(Widget):
    #最初にゲームに追加される
    timer = ObjectProperty(None)
    def add_obj(self): 
#      self.timer = Timer()
        self.enemy_list = EnemysList()
        self.enemy_list.make_enemy(self, (300,300), (30,30))
        self.enemy_list.make_enemy(self, (320,280), (30,30))
 
    #時間経過と共に更新される    
    def update(self,dt):
        self.timer.update_time()
        self.enemy_list.update_enemys(self)
        
        
class ShootingGameApp(App):
    def build(self):
        game = ShootingGame()
        game.add_obj()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

if __name__ == '__main__':
    ShootingGameApp().run()