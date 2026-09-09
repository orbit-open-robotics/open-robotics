#
# SecretReader
# Read key value pairs from specified file (secrets.txt)
#
from typing import Callable, Tuple

class SecretReader:
    def __init__(self) -> None:
        self._secrets = {}

    def read(self, file_path: str = "/secrets.txt"):
         with open(file_path, "r") as credentials_file:
            for raw_line in credentials_file:
                line = raw_line.strip()
                if  line and not line.startswith("#") and '=' in line:
                    key, value = line.split("=", 1)
                    self._secrets[key.strip().lower()] = value.strip()

    def get_value(self, key: str) -> str | None:
        try:
            return self._secrets[key]
        except KeyError:
            print(f'SecretReader: no key {key} available.')
            return None

    def print_all(self) -> None:
        for key, value in self._secrets.items():
            print(f'{key}: {value}')


if __name__ == '__main__':
    reader = SecretReader()
    reader.read()
    reader.print_all()
    
