import json
import traceback
import urllib.request
import urllib.error

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
        except OSError:
            print("Couldnt parse or find the children json file:", children_file)
            traceback.print_exc()

        self.nicknames = {}
        try:
            with open(nicknames_file, 'r', encoding="utf8") as f:
                self.nicknames = json.load(f)
        except OSError:
            print("Couldnt load nicknames")
            traceback.print_exc()

        self.children_map = {}
        self._build_index_map()

    def _build_index_map(self):
        for i in range(0, len(self.children)):  # iterate over children to make index map for easier use later
            self.children_map[self.children[i][JSON_EN_NAME].lower()] = i
            self.children_map[self.children[i][JSON_NAME].lower()] = i
            self.children_map[self.children[i][JSON_ID]] = i
        for nickname in self.nicknames:  # add nicknames to the children mapping
            self.children_map[nickname.lower()] = self.children_map[self.nicknames[nickname]]

    def get_child_by_identifier(self, identifier):
        try:
            return self.children[self.children_map[identifier.lower() if type(identifier) == str else identifier]]
        except KeyError as ke:
            pass
        return None

    def add_nickname(self, child, nickname):
        if nickname.lower() not in self.nicknames:
            self.children_map[nickname.lower()] = self.children_map[child[JSON_ID]]
            self.nicknames[nickname.lower()] = child[JSON_ID]
            self.save_nicknames_file()

    def remove_nickname(self, nickname):
        try:
            del self.children_map[nickname.lower()]
            del self.nicknames[nickname.lower()]
            self.save_nicknames_file()
        except Exception:
            pass

    def get_nicknames(self, child):
        nicks = []
        for k, v in self.nicknames.items():
            if v == child[JSON_ID]:
                nicks.append(k)
        return nicks

    def update_children_by_url(self, url):
        try:
            with urllib.request.urlopen(url) as response:
                html = response.read()
                self.children = json.loads(html.decode("utf-8"))
                self.save_children_file()
                self._build_index_map()
                return True
        except urllib.error.URLError:
            return False

    def save_nicknames_file(self):
        try:
            with open(self.nicknames_file, 'w', encoding="utf8") as f:
                json.dump(self.nicknames, f, ensure_ascii=False)
        except OSError:
            print("Couldnt save the nicknames json file:", self.nicknames_file)
            traceback.print_exc()

    def save_children_file(self):
        try:
            with open(self.children_file, 'w', encoding="utf8") as f:
                json.dump(self.children, f, ensure_ascii=False)
        except OSError:
            print("Couldnt save the children json file:", self.children_file)
            traceback.print_exc()
