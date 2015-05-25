# -*- coding: utf8 -*-
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
from kivy.core.window import Window
from kivy.vector import Vector
from kivy.properties import ObjectProperty,NumericProperty,ReferenceListProperty
import time
import math

ball_speed = 3 #ボールの基本速度
ball_count = 3 #ボールの跳ね返り回数
max_ball = 20 #画面に出せるボールの上限

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

#操作する機体の定義
class Rocket(Image):
    #初期位置
    def init_set(self,game):
        self.pos = Window.center #初期位置はウィンドウの中心
    #敵もしくは弾に当たると死ぬ
    def remove(self):
        pass

class Ball(Image):
    #ball.velocity を用いるためのvelocityの定義
    velocity_x = NumericProperty()
    velocity_y = NumericProperty()
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    #初期位置。機体からクリック(タッチ)した方向に
    def init_set(self,game,rocket,enemyList,position):
        self.count = ball_count
        self.game = game
        self.rocket = rocket
        self.enemys = enemyList
        self.pos = rocket.pos #発射時の機体の位置はロケットの中心
        if self.pos[0] == position[0] and self.pos[1] == position[1]: #ロケットの位置と射出位置が重なるときはずらす(タッチ検出部分でやるべき？)
            self.pos[1] += 5
        vec = math.sqrt((position[0] - self.pos[0])  * (position[0] - self.pos[0])  + (position[1] - self.pos[1]) * (position[1] - self.pos[1]))
        ball_speedx = ball_speed * (position[0] - self.pos[0]) / vec
        ball_speedy = ball_speed * (position[1] - self.pos[1]) / vec
        self.velocity = (ball_speedx, ball_speedy)

    #ボールを動かす。画面端まで行ったら跳ね返る

    def remove(self):
        self.game.remove_widget(self)

    def move(self,rocket,enemylist):
        #壁に跳ね返る
        if self.pos[0] < 0:
            self.velocity[0] *= -1
            self.count -= 1
        if self.pos[0] > Window.size[0]:
            self.velocity[0] *= -1
            self.count -= 1
        if self.pos[1] < 0:
            self.velocity[1] *= -1
            self.count -= 1
        if self.pos[1] > Window.size[1]:
            self.velocity[1] *= -1
            self.count -= 1

        self.pos = Vector(*self.velocity) + self.pos

#ボールもリストで一括管理

class BallList():
    balls = []
    #弾を消す(敵が当たった時や規定回数跳ね返った時)
    def remove(self,ball_id):
        self.balls[ball_id].remove()
        del self.balls[ball_id]

    #弾を発射，進む方向と発射位置を指定
    def make_balls(self,game,rocket,enemy_list,ball_pos):
        if len(self.balls) < max_ball: #ボールの数を制限する
            new_ball = Ball()
            new_ball.init_set(game,rocket,enemy_list,ball_pos)
            game.add_widget(new_ball)
            self.balls.append(new_ball)
        else: pass #作らない
    def update_balls(self,rocket,enemy_list):
        for i in self.balls:
            i.move(rocket,enemy_list)
            if i.count == 0 :
                self.remove(self.balls.index(i))

class ShootingGame(Widget):
    #最初にゲームに追加される
    mouse_position = (NumericProperty(),NumericProperty())
    mouse_position = Window.mouse_pos
    timer = ObjectProperty(None)
    def add_obj(self):
        self.timer = Timer()
        self.enemy_list = EnemysList()
        self.enemy_list.make_enemy(self, (300,300), (30,30))
        self.enemy_list.make_enemy(self, (320,280), (30,30))

        #ロケットを定義しないとボールの発射位置を定義できないので仮においておく
        self.rocket = Rocket()
        self.rocket.init_set(self)

        #ボールリスト
        self.ball_list = BallList()

    #時間経過と共に更新される
    def update(self,dt):
        self.timer.update_time()
        self.enemy_list.update_enemys(self)
        self.ball_list.update_balls(self.rocket,self.enemy_list)

        if(self.mouse_position != Window.mouse_pos): #マウスクリックでボールを発射
            self.mouse_position = Window.mouse_pos
            self.ball_list.make_balls(self,self.rocket,self.enemy_list,Window.mouse_pos)

class ShootingGameApp(App):
    def build(self):
        game = ShootingGame()
        game.add_obj()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

if __name__ == '__main__':
    ShootingGameApp().run()