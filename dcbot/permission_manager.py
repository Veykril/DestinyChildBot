import json
import traceback


class PermissionManager(object):
    def __init__(self, permissions_file='resources/permissions.json'):
        self.permissions_file = permissions_file
        try:
            with open(self.permissions_file, 'r') as f:
                self.permissions = json.load(f)
        except Exception:
            print("Couldnt parse or find the permissions json file:", self.permissions_file)
            traceback.print_exc()

    def is_superuser(self, user_id):
        return user_id in self.permissions

    def add_superuser(self, user_id):
        self.permissions.append(str(user_id))
        self.save_children_file()

    def save_children_file(self):
        try:
            with open(self.permissions_file, 'w') as f:
                json.dump(self.permissions, f)
        except Exception:
            print("Couldnt save the permissions json file:", self.permissions_file)
            traceback.print_exc()
