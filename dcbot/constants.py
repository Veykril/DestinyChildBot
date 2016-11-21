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

JSON_SKILL1 = "skill1"
JSON_SKILL2 = "skill2"
JSON_SKILL3 = "skill3"
JSON_SKILL4 = "skill4"
JSON_SKILL5 = "skill5"
JSON_SKILL_DESC1 = "skill_desc1"
JSON_SKILL_DESC2 = "skill_desc2"
JSON_SKILL_DESC3 = "skill_desc3"
JSON_SKILL_DESC4 = "skill_desc4"
JSON_SKILL_DESC5 = "skill_desc5"
JSON_SKILL_DESC1_EN = "skill_desc1_en"
JSON_SKILL_DESC2_EN = "skill_desc2_en"
JSON_SKILL_DESC3_EN = "skill_desc3_en"
JSON_SKILL_DESC4_EN = "skill_desc4_en"
JSON_SKILL_DESC5_EN = "skill_desc5_en"


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