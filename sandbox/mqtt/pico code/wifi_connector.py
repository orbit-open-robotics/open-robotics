#
# WebClient
# Requires micropython.umqtt.simple library
#
from network import WLAN, STA_IF
from time import sleep
from typing import Callable, Tuple
from orbit.secret_reader import SecretReader


class WifiConnector:
    def __init__(self,
                 network_name: str | None = None,
                 password: str | None = None,
                 secrets_file_path: str | None = None,
                 delay: float = 0.5
                 ) -> None:
        if network_name is not None and password is not None:
            self._network_name: str = network_name
            self._password: str = password
        elif secrets_file_path is not None:
            self._network_name, self._password = self._read_credentials(secrets_file_path)
        else:
            print('Error: no credentials provided!')

        self._delay: float = delay

    def _read_credentials(self, file_path: str = "/wifi_credentials.txt") -> Tuple[str, str]:
        """Read SSID and password from a secrets text file.

        Supported format:
            network_name = MySSID
            password = MyPassword
        """
        secret_reader = SecretReader()
        secret_reader.read(file_path)

        network_name: str | None = secret_reader.get_value('network_name')
        password: str | None = secret_reader.get_value('password')

        if network_name is not None and password is not None:
            return network_name, password

        raise ValueError(f'Could not read WiFi credentials from file {file_path}. ')
                
    def connect(self) -> None:
        wlan: WLAN = WLAN(STA_IF)
        wlan.active(True)
        wlan.connect(self._network_name, self._password)
        print("Connecting to WiFi", end="")
        while not wlan.isconnected():
            print(".", end="")
            sleep(self._delay)
        print("\nConnected! IP:", wlan.ifconfig()[0])

    
    
if __name__ == "__main__":
    # Network
    wifi_connector = WifiConnector("/wifi_credentials.txt")
    wifi_connector.connect()