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
max_ball = 200 #画面に出せるボールの上限

#速さを表す定数
machineVelocity = 5.0

    

class Timer(Widget):
    timer = ObjectProperty(None)
    start=time.time()
    def update_time(self):
        self.now = time.time() - self.start
        self.timer = int(self.now);

#fps計測用のクラス timerを継承
class Fps():
    def __init__(self,timer):
        self.timer = timer
        self.fps_after = 0
        self.fps_before = 0
        self.queue = []
    
    def update(self):
        self.fps_before = self.fps_after
        self.fps_after = self.timer.now
        self.update_queue(1/(self.fps_after - self.fps_before))
    def update_queue(self,new):
        self.queue = [new] + self.queue
        if len(self.queue) > 60:
            self.queue.remove(self.queue[60])
    #queueの中の平均を取る
    def get_current_fps(self):
        sum = 0
        for i in self.queue:
            sum += i
        return round(sum/len(self.queue),1)
        
        
class Enemy(Image):
    def init_set(self,pos,size):
        self.pos = pos
        self.size = size
    def remove(self,game):
        game.remove_widget(self)
    #move randomly
    def move_random(self):
            self.pos = (self.pos[0]+randint(-5,5),self.pos[1]+randint(-5,5))

#敵はリストで一括管理
class EnemysList():
    enemys = []
    def __init__(self,game):
        self.game = game
    #敵を消す(弾が当たった時とかに),引数はindex gameの順番
    def remove(self,enemy_id):
        if len(self.enemys) == 0:
            return
#         self.enemys[enemy_id].remove(game)
        self.game.remove_widget(self.enemys[enemy_id])
        self.enemys.remove(self.enemys[enemy_id])
        
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
    def goTop(self):
        #最小単位を指定してそれ
        self.pos[1] = (machineVelocity + self.pos[1])
    def goDown(self):
        #最小単位を指定してそれ
        self.pos[1] = (-machineVelocity + self.pos[1])
    def goLeft(self):
        self.pos[0] = self.pos[0] - machineVelocity
    def goRight(self):
        self.pos[0] = self.pos[0] + machineVelocity
    def move(self,theta,velocity):
        #角度thetaを当てた時の移動
        self.pos[0] = self.pos[0] + velocity * math.cos(theta)
        self.pos[1] = self.pos[1] + velocity * math.sin(theta)


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
#     mouse_position = (NumericProperty(),NumericProperty())
#     mouse_position = Window.mouse_pos
    timer = Timer()
    fps = ObjectProperty(None)
    
    def add_obj(self):
        self.enemy_list = EnemysList(self)
        self.enemy_list.make_enemy(self, (300,300), (30,30))
        self.enemy_list.make_enemy(self, (320,280), (30,30))
        #ロケットを定義しないとボールの発射位置を定義できないので仮においておく
        self.rocket = Rocket()
        self.rocket.init_set(self)
        self.add_widget(self.rocket)
        #ボールリスト
        self.ball_list = BallList()
        #fps計測用インスタンス
        self.fps_ins = Fps(self.timer)

    def __init__(self, **kwargs):
        super(ShootingGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print("コラコラコラコラ～ッ！(`o´)")
        if keycode[1] == 'w':
            self.rocket.goTop()
        if keycode[1] == 's':
            self.rocket.goDown()
        if keycode[1] == 'a':
            self.rocket.goLeft()
        if keycode[1] == 'd':
            self.rocket.goRight()
        return True
    
    def on_touch_down(self, touch,after = True):
        super(ShootingGame, self).on_touch_down(touch)
        print(touch)
        return False
#         return Widget.on_touch_down(self, touch)
    def on_touch_move(self, touch):
        print("move!!!",touch)
        self.ball_list.make_balls(self, self.rocket, self.enemy_list, [touch.x,touch.y])
        return Widget.on_touch_move(self, touch)
        
    def on_touch_up(self, touch):
        print("Released!!",touch)
        return Widget.on_touch_up(self, touch)
      
    #時間経過と共に更新される
    def update(self,dt):
        self.timer.update_time()
        self.enemy_list.update_enemys(self)
        self.ball_list.update_balls(self.rocket,self.enemy_list)
        #fps計測用
        self.fps_ins.update()
        self.fps = self.fps_ins.get_current_fps()
#         if(self.mouse_position != Window.mouse_pos): #マウスクリックでボールを発射
#             self.mouse_position = Window.mouse_pos
#             self.ball_list.make_balls(self,self.rocket,self.enemy_list,Window.mouse_pos)
#         
        
class ShootingGameApp(App):
    def build(self):
        game = ShootingGame()
        game.add_obj()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game

if __name__ == '__main__':
    ShootingGameApp().run()