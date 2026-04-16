#
# RobotAccessory
#
class RobotAccessory:
    def __init__(self) -> None:
        pass

    def initialize(self) -> None:
        pass

    def connected(self) -> None:
        pass

    def disconnected(self) -> None:
        pass

    def interpret(self, message) -> None:
        pass
    
    async def run_loop(self) -> None:
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass


if __name__ == "__main__":
    robot_accessory = RobotAccessory()