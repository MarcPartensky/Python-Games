from myspaceshipgroup import SpaceShipGroup, GamePlayer


class AsteroidDuo(SpaceShipGroup):
    def __init__(self):
        player1 = GamePlayer.random()
        player2 = GamePlayer.random()
        entities = [player1, player2]
        super().__init__(entities)

if __name__ == "__main__":
    from mymanager import EntityManager
    game = AsteroidDuo()
    m = EntityManager(game)
    m()






