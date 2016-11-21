from dcbot.constants import *


class Child(object):
    """Currently Unused
    Gonna see if I actually need this class later, might do something like a stat calculator?
    """
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
        self.element = kwargs[JSON_ATTRIBUTE_ID]
        self.role = kwargs[JSON_ROLE]
        self.stat_hp = kwargs[JSON_STAT_HP]
        self.stat_atk = kwargs[JSON_STAT_ATK]
        self.stat_def = kwargs[JSON_STAT_DEF]
        self.stat_agi = kwargs[JSON_STAT_AGI]
        self.stat_crit = kwargs[JSON_STAT_CRIT]

    def to_json(self):
        """TO-DO: Make this return a dictionary by scanning the class field instead of doing this shit"""
        return {JSON_IDX: self.idx, JSON_ID: self.id, JSON_INVEN_ID: self.inven_id, JSON_NAME: self.name,
                JSON_EN_NAME: self.en_name, JSON_RARITY: self.rarity, JSON_ATTRIBUTE_ID: self.element,
                JSON_ROLE: self.role, JSON_STAT_HP: self.stat_hp, JSON_STAT_ATK: self.stat_atk,
                JSON_STAT_DEF: self.stat_def, JSON_STAT_AGI: self.stat_agi, JSON_STAT_CRIT: self.stat_crit}
