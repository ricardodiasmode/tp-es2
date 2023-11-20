import background


class TestBackground:
    mocked_background = background.Background()

    def test_screen_width(self):
        assert self.mocked_background.screen.get_width() == \
               self.mocked_background.display_width + self.mocked_background.debug_width

    def test_screen_height(self):
        assert self.mocked_background.screen.get_height() == self.mocked_background.display_height

    def test_variables_reset(self):
        self.mocked_background.reset_variables()
        assert self.mocked_background.log_locations == []
        assert self.mocked_background.square_image_dict == {}
        assert self.mocked_background.square_dict == {}

    def test_has_logs_on_init(self):
        self.mocked_background.init_background()
        assert len(self.mocked_background.log_locations) > 0

    def test_logs_square_dict_and_logs_location_are_equal_in_size(self):
        self.mocked_background.init_background()

        log_locations = []
        for key, value in self.mocked_background.square_dict.items():
            if value == "LOG":
                log_locations.append(key)

        assert len(self.mocked_background.log_locations) == len(log_locations)

    def test_update_square_to_grass(self):
        self.mocked_background.reset_variables()
        self.mocked_background.update_square((0, 0), "GRASS")
        assert self.mocked_background.square_image_dict[0, 0] == self.mocked_background.grass0_img

    def test_update_square_to_log(self):
        self.mocked_background.reset_variables()
        self.mocked_background.update_square((0, 0), "LOG")
        assert self.mocked_background.square_image_dict[0, 0] == self.mocked_background.log_img

    def test_load_grass(self):
        self.mocked_background.load_grass_images()
        assert self.mocked_background.grass0_img is not None and \
            self.mocked_background.grass1_img is not None and \
            self.mocked_background.grass2_img is not None and \
            self.mocked_background.grass3_img is not None

    def test_load_log(self):
        self.mocked_background.load_log_image()
        assert self.mocked_background.log_img is not None
