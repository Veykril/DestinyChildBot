import json
import traceback

from dcbot.constants import *


class ChildrenManager(object):
    def __init__(self, children_json_file='resources/children.json'):
        self.children_file = children_json_file

        self.children = []
        try:
            with open(self.children_file, 'r', encoding="utf8") as f:
                self.children = json.load(f)
            print("Children file successfully read!")
        except Exception:
            print("Couldnt parse or find the children json file:", children_json_file)
            traceback.print_exc()

        self.children_map = {}
        for i in range(0, len(self.children)):  # iterate over children to make index map for easier use later
            self.children_map[self.children[i][JSON_EN_NAME].lower()] = i
            self.children_map[self.children[i][JSON_NAME].lower()] = i
            self.children_map[self.children[i][JSON_ID]] = i
        print(self.children_map)

    def get_child_by_identifier(self, identifier):
        try:
            return self.children[self.children_map[identifier.lower() if type(identifier) == str else identifier]]
        except KeyError as ke:
            pass
        return None

    def add_entry(self, child_info):  # temporary
        self.children.append(child_info)
        self.save_children_file()

    def save_children_file(self):
        try:
            with open(self.children_file, 'w', encoding="utf8") as f:
                json.dump(self.children, f, ensure_ascii=False)
        except Exception:
            print("Couldnt save the children json file:", self.children_file)
            traceback.print_exc()
