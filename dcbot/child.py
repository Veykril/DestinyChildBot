from dcbot.constants import *
from enum import Enum


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


class Child(object):
    """ UNUSED ATM
    Should probably rename the class to something else cause child/parent relationship in programming etc
                        int,int,int,string,string,int,enum/int,enum/int,int,int,int,int,int"""
    """
    def __init__(self, idx, id, inven_id, name, en_name, rarity, element, role, stat_hp, stat_atk, stat_def, stat_agi, stat_crit):
        self.idx = idx
        self.id = id
        self.inven_id = inven_id
        self.name = name
        self.en_name = en_name
        self.rarity = rarity
        self.element = element
        self.role = role
        self.stat_hp = stat_hp
        self.stat_atk = stat_atk
        self.stat_def = stat_def
        self.stat_agi = stat_agi
        self.stat_crit = stat_crit
    """
    def __init__(self, **kwargs):
        self.idx = kwargs[JSON_IDX]
        self.id = kwargs[JSON_ID]
        self.inven_id = kwargs[JSON_INVEN_ID]
        self.name = kwargs[JSON_NAME]
        self.en_name = kwargs[JSON_EN_NAME]
        self.rarity = kwargs[JSON_RARITY]
        self.element = kwargs[JSON_ELEMENT]
        self.role = kwargs[JSON_ROLE]
        self.stat_hp = kwargs[JSON_STAT_HP]
        self.stat_atk = kwargs[JSON_STAT_ATK]
        self.stat_def = kwargs[JSON_STAT_DEF]
        self.stat_agi = kwargs[JSON_STAT_AGI]
        self.stat_crit = kwargs[JSON_STAT_CRIT]

    def toJSON(self):
        """TO-DO: Make this return a dictionary by scanning the class field instead of doing this shit"""
        return {JSON_IDX: self.idx, JSON_ID: self.id, JSON_INVEN_ID: self.inven_id, JSON_NAME: self.name,
                JSON_EN_NAME: self.en_name, JSON_RARITY: self.rarity, JSON_ELEMENT: self.element,JSON_ROLE: self.role,
                JSON_STAT_HP: self.stat_hp, JSON_STAT_ATK: self.stat_atk, JSON_STAT_DEF: self.stat_def,
                JSON_STAT_AGI: self.stat_agi, JSON_STAT_CRIT: self.stat_crit}