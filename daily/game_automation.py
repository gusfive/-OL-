from daily.base_operations import BaseOperations
from daily.config import COORDINATES, IMAGE_PATHS


class GameAutomation:
    def __init__(self):
        self.base_ops = BaseOperations()
        
    def daily_tasks(self, character):
        """执行每日任务"""
        self._select_character(character)
        self._enter_game()
        self._init_position()
        self._alliance_tasks()
        self._tiantin_tasks()
        self._activity_tasks()
        
    def _select_character(self, character_image):
        """选择角色"""
        self.base_ops.click_at(**COORDINATES['CHARACTER_SELECT'])
        self.base_ops.find_and_click(character_image)
        
    def _enter_game(self):
        """进入游戏"""
        self.base_ops.find_and_click(IMAGE_PATHS['START_GAME'])
        self.base_ops.find_and_click(IMAGE_PATHS['NOTICE'])
        self.base_ops.find_and_click(IMAGE_PATHS['ACTIVITY']) 