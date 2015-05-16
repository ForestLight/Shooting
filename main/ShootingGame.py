'''
Created on 2015/05/16

@author: admin
'''
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from random import Random, randint

class Enemy(Widget):
    r = Random()
    def init_set(self,pos,size):
        self.pos = pos
        self.size = size
    def remove(self):
            pass
    #move randomly
    def move_random(self):
            self.pos = (self.pos[0]+randint(-5,5),self.pos[1]+randint(-5,5))
            print(self.pos)
            
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
            i.pos = (i.pos[0]+randint(-5,5),i.pos[1]+randint(-5,5))
 
class ShootingGame(Widget):
    enemy_list = EnemysList()
    #最初にゲームに追加される
    def add_obj(self):        
        pass
    #時間経過と共に更新される    
    def update(self,dt):
        pass
#      self.enemy_list.update_enemys(self)
        
        
class ShootingGameApp(App):
    def build(self):
        game = ShootingGame()
        game.add_obj()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

if __name__ == '__main__':
    ShootingGameApp().run()