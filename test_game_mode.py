import background
import gamemode


class TestGameMode:

    def test_initial_variables(self):
        mocked_game_mode = gamemode.GameMode()
        assert mocked_game_mode.blue_characters == []
        assert mocked_game_mode.red_characters == []
        assert mocked_game_mode.current_background is None
        assert mocked_game_mode.current_turn == 0

    def test_reset_variables(self):
        mocked_game_mode = gamemode.GameMode()

        mocked_game_mode.blue_characters = [1]
        mocked_game_mode.red_characters = [2]
        mocked_game_mode.current_background = 3
        mocked_game_mode.current_turn = 4

        mocked_game_mode.reset_variables()

        assert mocked_game_mode.blue_characters == []
        assert mocked_game_mode.red_characters == []
        assert mocked_game_mode.current_background is None
        assert mocked_game_mode.current_turn == 0

    def test_create_characters(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        mocked_game_mode.create_characters()
        assert len(mocked_game_mode.blue_characters) == mocked_game_mode.number_of_character_each_team
        assert len(mocked_game_mode.red_characters) == mocked_game_mode.number_of_character_each_team

    def test_clone_best_character(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        mocked_game_mode.create_characters()
        mocked_game_mode.get_best_five_characters()
        mocked_game_mode.clone_best_characters()
        assert mocked_game_mode.blue_characters[0].dna == mocked_game_mode.best_characters_in_turn[0].dna
        assert mocked_game_mode.red_characters[0].dna == mocked_game_mode.best_characters_in_turn[0].dna

    def test_mutate_characters(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        mocked_game_mode.create_characters()
        initial_blue_dna = mocked_game_mode.blue_characters[0].dna.copy()
        initial_red_dna = mocked_game_mode.red_characters[0].dna.copy()
        mocked_game_mode.mutate_characters()
        assert initial_blue_dna != mocked_game_mode.blue_characters[0].dna
        assert initial_red_dna != mocked_game_mode.red_characters[0].dna

    def test_reset_game(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.reset_game()
        assert mocked_game_mode.current_generation == 1

    def test_on_turn_end_without_reset(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        mocked_game_mode.create_characters()
        mocked_game_mode.on_turn_end()
        assert mocked_game_mode.current_turn == 1

    def test_on_turn_end_with_reset(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        mocked_game_mode.on_turn_end()
        assert mocked_game_mode.current_generation == 1

    def test_check_if_game_over_without_characters(self):
        mocked_game_mode = gamemode.GameMode()
        assert mocked_game_mode.check_if_game_over()

    def test_check_if_game_over_with_characters_alive(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        mocked_game_mode.create_characters()
        assert not mocked_game_mode.check_if_game_over()

    def test_check_if_game_over_with_characters_dead(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        mocked_game_mode.create_characters()

        for character in mocked_game_mode.blue_characters:
            character.die()
        for character in mocked_game_mode.red_characters:
            character.die()

        assert mocked_game_mode.check_if_game_over()

    def test_has_character_at_location_success(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        mocked_game_mode.create_characters()
        valid_location = mocked_game_mode.blue_characters[0].current_location
        assert mocked_game_mode.has_character_at_location(valid_location)

    def test_has_character_at_location_fail(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        mocked_game_mode.create_characters()
        assert not mocked_game_mode.has_character_at_location((-1, -1))

    def test_has_character_at_location_ignoring_character(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        mocked_game_mode.create_characters()
        valid_location = mocked_game_mode.blue_characters[0].current_location
        character_to_ignore = mocked_game_mode.blue_characters[0]
        assert not mocked_game_mode.has_character_at_location(valid_location, character_to_ignore)
