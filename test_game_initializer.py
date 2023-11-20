import gameInitializer


class TestGameLoop:

    def test_first_turn(self):
        mocked_game_initializer = gameInitializer.GameInitializer()
        mocked_game_initializer.run_turn()


