from enum import Enum


VERSION = '0.1'

INVEN_IMAGE_URL = "http://static.inven.co.kr/image_2011/site_image/game/minidata/99/"
DROPBOX_IMAGE_URL = "https://dl.dropboxusercontent.com/u/123314639/db-use/"
WEB_CHILDREN_URL = "http://destinychild.inven.co.kr/dataninfo/child/detail.php?d=99&c="

#  JSON RELATED
JSON_ATTRIBUTE = "attribute"
JSON_ATTRIBUTE_ID = "attribute_id"
JSON_AWAKEN_GROUP = "awaken_group"
JSON_EN_NAME = "en_name"
JSON_ENABLE_AWAKEN = "enable_awaken"
JSON_ID = "id"
JSON_IDX = "idx"
JSON_INVEN_ID = "inven_id"
JSON_NAME = "name"
JSON_RARITY = "rarity"
JSON_ROLE = "role"
JSON_ROLE_ID = "role_id"
JSON_SKILL1 = "skill1"
JSON_SKILL2 = "skill2"
JSON_SKILL3 = "skill3"
JSON_SKILL4 = "skill4"
JSON_SKILL5 = "skill5"
JSON_SKILL1_NAME = "skill1_name"
JSON_SKILL2_NAME = "skill2_name"
JSON_SKILL3_NAME = "skill3_name"
JSON_SKILL4_NAME = "skill4_name"
JSON_SKILL5_NAME = "skill5_name"
JSON_SKILL1_DESC = "skill1_desc"
JSON_SKILL2_DESC = "skill2_desc"
JSON_SKILL3_DESC = "skill3_desc"
JSON_SKILL4_DESC = "skill4_desc"
JSON_SKILL5_DESC = "skill5_desc"
JSON_SKILL1_DESC_EN = "skill1_desc_en"
JSON_SKILL2_DESC_EN = "skill2_desc_en"
JSON_SKILL3_DESC_EN = "skill3_desc_en"
JSON_SKILL4_DESC_EN = "skill4_desc_en"
JSON_SKILL5_DESC_EN = "skill5_desc_en"
JSON_START_GRADE = "start_grade"
JSON_STAT_AGI = "stat_agi"
JSON_STAT_ATK = "stat_atk"
JSON_STAT_CRIT = "stat_crit"
JSON_STAT_DEF = "stat_def"
JSON_STAT_HP = "stat_hp"


class Attribute(Enum):
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
    support = 5
    exp = 6
    evolution = 7
    unknown1 = 8
