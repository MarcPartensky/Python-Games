import tensorflow as tf
import numpy as np

from othello import Othello
from player import Robot,Humain
from mywindow import Window


class Trainer:
    def __init__(self,window,players,number_games=1,affichage=False):
        self.window=window
        self.games=[]
        self.players=players
        self.affichage=affichage
    def __call__(self,number_of_games):
        for i in range(number_of_games):
            print("Training game:",i)
            game=Othello(self.window,self.players,self.affichage)
            game()
            self.games.append(game)
            for id_player,player in enumerate(self.players):
                if isinstance(player,NeuralNetwork):
                    self.teach(id_player,game)
    def teach(self,id_player,game):
        player=self.players[id_player]
        print("player:",player)
        print("game.gagnant:",game.gagnant)
        print("game.historique:",game.historique)
        if player is game.gagnant:
            lesson=[]
            historique=game.historique
            for action in game.historique:
                action_grid,action_id_player,action_choice=action
                if action_id_player==id_player:
                    lesson+=[np.array(action),action_choice]
            self.players[id_player].training_data+=lesson







class NeuralNetwork:
    def __init__(self,training_data=[]):
        self.training_data=training_data
        self.model=tf.keras.models.Sequential()
        self.model.add(tf.keras.layers.Flatten())
        for i in range(4):
            self.model.add(tf.keras.layers.Dense(128,activation=tf.nn.relu))
        self.model.add(tf.keras.layers.Dense(8,activation=tf.nn.relu))
        self.model.add(tf.keras.layers.Dense(8,activation=tf.nn.softmax))
        self.model.compile(optimizer="adam",loss="sparse_categorical_crossentropy",metrics=["accuracy"])

    def train(self):
        if len(self.training_data)>0:
            x_train,y_train=self.training_data
            self.model.fit(x_train,y_train,epochs=3)
        else:
            raise Exception("Neural Network has no training data.")

    def jouer(self,plateau,fenetre,tour):
        input=np.array(plateau.grille)
        predictions=self.model.predict([input])
        #print(predictions)
        raw_choice=predictions.argmax()
        choice=[raw_choice//plateau.taille[0],raw_choice%plateau.taille[0]]
        #print(choice)
        return choice

if __name__=="__main__":
    window=Window([800,800],set=False)
    players=[Robot(),NeuralNetwork()]
    training=Trainer(window,players)
    training(10)
    window.set()
    print(players[1].training_data)
    game=Othello(window,[Humain(),training.players[1]],affichage=True)
    game()
