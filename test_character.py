import background
import character
import gamemode


class TestCharacter:

    def test_initial_location(self):
        initial_location = (0, 0)
        mocked_character = character.Character(initial_location, None, True, 0)
        assert initial_location == mocked_character.current_location

    def test_is_blue_team(self):
        blue_team_member = True
        mocked_character = character.Character((0, 0), None, blue_team_member, 0)
        assert blue_team_member == mocked_character.blue_team_member

    def test_is_red_team(self):
        blue_team_member = False
        mocked_character = character.Character((0, 0), None, blue_team_member, 0)
        assert blue_team_member == mocked_character.blue_team_member

    def test_brain_initialized(self):
        mocked_character = character.Character((0, 0), None, True, 0)
        assert mocked_character.brain is not None

    def test_dna_initialized(self):
        mocked_character = character.Character((0, 0), None, True, 0)
        assert mocked_character.dna != []

    def test_update_image_blue_team(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        mocked_character = character.Character((0, 0), mocked_game_mode, True, 0)
        assert mocked_character.player_image == mocked_character.blue_character_img

    def test_update_image_red_team(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        mocked_character = character.Character((0, 0), mocked_game_mode, False, 0)
        assert mocked_character.player_image == mocked_character.red_character_img

    def test_update_image_blue_team_with_knife(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        mocked_character = character.Character((0, 0), mocked_game_mode, True, 0)
        mocked_character.has_knife = True
        mocked_character.update_image()
        assert mocked_character.player_image == mocked_character.blue_character_with_knife_img

    def test_update_image_red_team_with_knife(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        mocked_character = character.Character((0, 0), mocked_game_mode, False, 0)
        mocked_character.has_knife = True
        mocked_character.update_image()
        assert mocked_character.player_image == mocked_character.red_character_with_knife_img

    def test_move_left(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        initial_location = (128, 128)
        mocked_character = character.Character(initial_location, mocked_game_mode, False, 0)
        mocked_game_mode.red_characters_locations.append(initial_location)
        mocked_character.move_left()
        assert mocked_character.current_location == (initial_location[0] - 64, initial_location[1])

    def test_move_right(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        initial_location = (128, 128)
        mocked_character = character.Character(initial_location, mocked_game_mode, False, 0)
        mocked_game_mode.red_characters_locations.append(initial_location)
        mocked_character.move_right()
        assert mocked_character.current_location == (initial_location[0] + 64, initial_location[1])

    def test_move_up(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        initial_location = (128, 128)
        mocked_character = character.Character(initial_location, mocked_game_mode, False, 0)
        mocked_game_mode.red_characters_locations.append(initial_location)
        mocked_character.move_up()
        assert mocked_character.current_location == (initial_location[0], initial_location[1] - 64)

    def test_move_down(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        initial_location = (128, 128)
        mocked_character = character.Character(initial_location, mocked_game_mode, False, 0)
        mocked_game_mode.red_characters_locations.append(initial_location)
        mocked_character.move_down()
        assert mocked_character.current_location == (initial_location[0], initial_location[1] + 64)

    def test_death(self):
        mocked_character = character.Character((0,0), None, False, 0)
        mocked_character.die()
        assert mocked_character.is_dead

    def test_dna_few_mutations(self):
        mocked_character = character.Character((0,0), None, False, 0)
        dna_before_mutation = mocked_character.dna.copy()
        mocked_character.mutate_dna(1)
        assert dna_before_mutation != mocked_character.dna

    def test_dna_many_mutations(self):
        mocked_character = character.Character((0,0), None, False, 0)
        dna_before_mutation = mocked_character.dna.copy()
        mocked_character.mutate_dna(100)
        assert dna_before_mutation != mocked_character.dna

    def test_check_should_die(self):
        mocked_character = character.Character((0,0), None, False, 0)
        mocked_character.energy = 0
        mocked_character.check_should_die()
        assert mocked_character.is_dead

    def test_action_taking_energy(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        initial_location = (128, 128)
        mocked_character = character.Character(initial_location, mocked_game_mode, False, 0)
        mocked_game_mode.red_characters_locations.append(initial_location)
        initial_energy = mocked_character.energy
        mocked_character.do_action(0)
        assert initial_energy != mocked_character.energy

    def test_knife_craft(self):
        mocked_game_mode = gamemode.GameMode()
        mocked_game_mode.current_background = background.Background()
        initial_location = (128, 128)
        mocked_character = character.Character(initial_location, mocked_game_mode, False, 0)
        mocked_game_mode.current_background.square_dict.update({initial_location: "LOG"})
        mocked_game_mode.current_background.log_locations.append(initial_location)
        mocked_character.craft_knife()
        assert mocked_character.has_knife

    def test_load_blue_character_image(self):
        mocked_character = character.Character((0,0), None, False, 0)
        mocked_character.load_blue_character_images()
        assert mocked_character.blue_character_img is not None and \
            mocked_character.blue_character_with_knife_img is not None

    def test_load_red_character_image(self):
        mocked_character = character.Character((0,0), None, False, 0)
        mocked_character.load_red_character_images()
        assert mocked_character.red_character_img is not None and \
            mocked_character.red_character_with_knife_img is not None

    def test_get_closest_enemy_index(self):
        mocked_character = character.Character((0,0), None, False, 0)
        enemies_loc = ([0, 64], [128, 128], [128, 0], [128, 64], [0, 128])
        found_index = mocked_character.get_closest_enemy_index(enemies_loc)
        assert found_index == 0


