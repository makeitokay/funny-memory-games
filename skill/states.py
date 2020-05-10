from aioalice.utils.helper import Helper, HelperMode, Item


class MainMenuStates(Helper):
    mode = HelperMode.snake_case

    SELECT_GAME = Item()


class TripGameStates(Helper):
    mode = HelperMode.snake_case

    TRIP_GAME_QUIZ = Item()
    TRIP_GAME_EXCURSION = Item()
    TRIP_GAME_END = Item()


class AntonymsGameStates(Helper):
    mode = HelperMode.snake_case

    ANTONYMS_GAME = Item()
    ANTONYMS_GAME_END = Item()
