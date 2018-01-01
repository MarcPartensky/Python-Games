import tensorflow as tf
import numpy as np

from othello import Othello
from player import Player,Robot,Humain
from beast import Beast
from mywindow import Window

import random


class Trainer:
    def __init__(self,window,players,affichage=False):
        self.window=window
        self.games=[]
        self.players=players
        self.affichage=affichage
    def __call__(self,number_of_games):
        for i in range(number_of_games):
            #print("Training game:",i)
            game=Othello(self.window,self.players,self.affichage)
            game()
            self.games.append(game)
            for id_player,player in enumerate(self.players):
                if isinstance(player,NeuralNetwork):
                    self.teach(id_player,game)
                    self.players[id_player].train()
    def teach(self,id_player,game):
        player=self.players[id_player]
        #print("player:",player)
        #print("game.gagnant:",game.gagnant)
        #print("game.historique:",game.historique)
        x_train,y_train=[],[]
        historique=game.historique
        contestants=game.plateau.nombre_joueurs
        #print(game.historique)
        for action in game.historique:
            action_grid,action_id_player,action_choice=action
            #print(action_grid)
            action_grid=self.exchangePieces(action_grid,id_player,game.gagnant,contestants)
            #print(action_grid)
            #print(game.gagnant,action_id_player)
            if game.gagnant==action_id_player:
                x_train.append(action_grid)
                y_train.append(action_choice)
        x_player_train,y_player_train=self.players[id_player].training_data
        x_player_train+=x_train
        y_player_train+=y_train
        #print(x_player_train,y_player_train)
        self.players[id_player].training_data=[x_player_train,y_player_train]
        #=[x_train,y_train]

    def exchangePieces(self,grid,old_id,new_id,contestants):
        exchange=new_id-old_id
        sy=len(grid)
        sx=len(grid[0])
        for y in range(sy):
            for x in range(sx):
                grid[y][x]=(grid[y][x]+exchange)%contestants
        return grid








class NeuralNetwork(Player):
    def __init__(self,training_data=[[],[]]):
        Player.__init__(self)
        self.training_data=training_data
        self.model=tf.keras.models.Sequential()
        self.model.add(tf.keras.layers.Flatten())
        for i in range(4):
            self.model.add(tf.keras.layers.Dense(128,activation=tf.nn.relu))
        self.model.add(tf.keras.layers.Dense(8,activation=tf.nn.relu))
        self.model.add(tf.keras.layers.Dense(8,activation=tf.nn.softmax))
        self.model.compile(optimizer="adam",loss="sparse_categorical_crossentropy",metrics=["accuracy"])

    def train(self,epochs=3):
        if len(self.training_data)>0:
            x_train,y_train=self.training_data
            x_train=self.convert(x_train)
            x_train=np.array(self.convert(x_train))
            y_train=np.array(self.convert(y_train))
            print(type(x_train))
            print(type(x_train[0]))
            print(type(x_train[0][0]))
            print(type(x_train[0][0][0]))
            #print(type(x_train))
            #print(y_train)
            self.model.fit(x_train,y_train,epochs=epochs)
        else:
            raise Exception("Neural Network has no training data.")

    def convert(self,tree):
        if type(tree)==list:
            tree=[]
            for element in tree:
                tree.append(self.convert(element))
            return tree
        else:
            return float(tree)



    def jouer(self,plateau,fenetre,tour):
        input=np.array(plateau.grille)
        predictions=self.model.predict([input])
        #print(predictions)
        raw_choice=predictions.argmax()
        choice=[raw_choice//plateau.taille[0],raw_choice%plateau.taille[0]]
        #print("Network choice:",choice)
        if choice in plateau.mouvements:
            pass
            #print("Valid")
        else:
            #print("Random")
            choice=random.choice(plateau.mouvements)
        #print("Final choice:  ",choice)
        #print("")
        return choice

if __name__=="__main__":
    window=Window(taille=[800,800],set=False)
    players=[Beast(2),NeuralNetwork()]
    training=Trainer(window,players,affichage=True)
    training(5)
    window.set()
    print(training.players[1].training_data)
    game=Othello(window,[NeuralNetwork(),Robot(1)])
    #game=Othello(window,[Humain(),training.players[1]],affichage=True)
    game()
