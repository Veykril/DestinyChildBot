import json
import traceback

from dcbot.constants import *


class ChildrenManager(object):
    def __init__(self, children_file='resources/children.json', nicknames_file='resources/nicknames.json'):
        self.children_file = children_file
        self.nicknames_file = nicknames_file

        self.children = []
        try:
            with open(self.children_file, 'r', encoding="utf8") as f:
                self.children = json.load(f)
            print("Children file successfully read!")
        except Exception:
            print("Couldnt parse or find the children json file:", children_file)
            traceback.print_exc()

        self.nicknames = {}
        try:
            with open(nicknames_file, 'r', encoding="utf8") as f:
                self.nicknames = json.load(f)
        except Exception:
            print("Couldnt load nicknames")
            traceback.print_exc()

        self.children_map = {}
        for i in range(0, len(self.children)):  # iterate over children to make index map for easier use later
            self.children_map[self.children[i][JSON_EN_NAME].lower()] = i
            self.children_map[self.children[i][JSON_NAME].lower()] = i
            self.children_map[self.children[i][JSON_ID]] = i
        for nickname in self.nicknames:  # add nicknames to the children mapping
            self.children_map[nickname.lower()] = self.children_map[self.nicknames[nickname]]
        print(self.children_map)

    def get_child_by_identifier(self, identifier):
        try:
            return self.children[self.children_map[identifier.lower() if type(identifier) == str else identifier]]
        except KeyError as ke:
            pass
        return None

    def add_nickname(self, identifier, nickname):
        try:  # check if it's the id as keyword
            identifier = int(identifier)
        except ValueError:
            identifier = identifier.lower()
        print(identifier)
        if identifier in self.children_map:
            self.children_map[nickname.lower()] = self.children_map[identifier]
            self.nicknames[nickname.lower()] = identifier
            self.save_nicknames_file()
            return True
        return False

    def save_nicknames_file(self):
        try:
            with open(self.nicknames_file, 'w', encoding="utf8") as f:
                json.dump(self.nicknames, f, ensure_ascii=False)
        except Exception:
            print("Couldnt save the nicknames json file:", self.nicknames_file)
            traceback.print_exc()

    def save_children_file(self):
        try:
            with open(self.children_file, 'w', encoding="utf8") as f:
                json.dump(self.children, f, ensure_ascii=False)
        except Exception:
            print("Couldnt save the children json file:", self.children_file)
            traceback.print_exc()
