'''
Created on 2015/05/16

@author: admin
'''
from kivy.app import App
from kivy.uix.widget import Widget


class ShootingGame(Widget):
    pass
        
class ShootingGameApp(App):
    def build(self):
        game = ShootingGame()
        return game

if __name__ == '__main__':
    ShootingGameApp().run()