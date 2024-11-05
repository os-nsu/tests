import os

class Proxy:
    def __init__(self, config_path=None):
        self.config_path = config_path
        self.config_content = self._read_config() if config_path else ""
        self.last_modified_time = self._get_last_modified_time()

    def _read_config(self):
        if self.config_path and os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return f.read()
        return ""

    def _get_last_modified_time(self):
        return os.path.getmtime(self.config_path) if self.config_path else None

    def has_config_changed(self):
        current_time = self._get_last_modified_time()
        if current_time != self.last_modified_time:
            self.last_modified_time = current_time
            return True
        return False

    def update_config(self, new_content):
        if self.config_path:
            with open(self.config_path, "w") as f:
                f.write(new_content)
            self.config_content = new_content
            self.last_modified_time = self._get_last_modified_time()

    def get_config_content(self):
        return self.config_content

