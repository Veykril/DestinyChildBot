from enum import Enum


VERSION = '0.1'

INVEN_IMAGE_URL = "http://static.inven.co.kr/image_2011/site_image/game/minidata/99/"

#  JSON RELATED
JSON_IDX = "idx"
JSON_ID = "id"
JSON_NAME = "name"
JSON_INVEN_ID = "inven_id"
JSON_EN_NAME = "en_name"
JSON_RARITY = "rarity"
JSON_ELEMENT = "element"
JSON_ROLE = "role"
JSON_STAT_HP = "stat_hp"
JSON_STAT_ATK = "stat_atk"
JSON_STAT_DEF = "stat_def"
JSON_STAT_AGI = "stat_agi"
JSON_STAT_CRIT = "stat_crit"


class Element(Enum):
    water = 1
    fire = 2
    forest = 3
    light = 4
    dark = 5
    unknown1 = 6
    unknown2 = 7
    unknown3 = 8


class Role(Enum):
    attack = 1
    defense = 2
    heal = 3
    restrain = 4
    support =5
    exp = 6
    evolution = 7
    unknown1 = 8