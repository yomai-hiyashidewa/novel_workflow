import yaml
import os

class YamlAdapter:
    _data = None

    @staticmethod
    def _get_abs_path(yaml_path: str) -> str:
        # 呼び出し元に依存せず絶対パスを返す
        base_dir = os.path.dirname(os.path.dirname(__file__))  # apps/ より上のプロジェクトルート
        abs_path = os.path.join(base_dir, yaml_path)
        return os.path.abspath(abs_path)

    @classmethod
    def load(cls, yaml_path: str = "config/config.yaml") -> dict | None:
        abs_path = cls._get_abs_path(yaml_path)
        if not os.path.exists(abs_path):
            print(f"INFO: Config file '{abs_path}' does not exist.")
            return None
        with open(abs_path, "r", encoding="utf-8") as f:
            cls._data = yaml.safe_load(f)
        return cls._data

    @classmethod
    def get(cls, key: str, default=None, yaml_path: str = "config/config.yaml"):
        if cls._data is None:
            cls.load(yaml_path)
        return cls._data.get(key, default) if cls._data else default

    @classmethod
    def save(cls, data: dict, yaml_path: str = "config/config.yaml"):
        abs_path = cls._get_abs_path(yaml_path)
        with open(abs_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, allow_unicode=True)
        cls._data = data