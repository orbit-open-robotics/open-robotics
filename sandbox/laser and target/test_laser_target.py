#
# test_laser_target
#
from orbit import LaserTarget

def hit_function():
    print("Hit detected!")

def max_hit_function():
    print("Max hits reached!")
``


if __name__ == "__main__":
    laserTarget = LaserTarget(hit_function)
    laserTarget.initialize()
    laserTarget.start()

