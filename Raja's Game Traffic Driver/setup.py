from cx_Freeze import Executable, setup

# All game assets + save files needed next to the exe at runtime.
include_files = [
    "a7.mp3", "run.mp3", "cc.mp3",
    "road1.png", "road2.png", "sideBoard.png",
    "car.png", "playerCar2.png", "playerCar3.png",
    "ped1.png", "deadped1.png", "ped2.png", "deadped2.png", "ped3.png", "deadped3.png",
    "car2.png", "car3.png", "truck1.png",
    "menu.png", "garage.png",
    "playUp.png", "playDown.png",
    "garageUp.png", "garageDown.png",
    "quitUp.png", "quitDown.png",
    "backUp.png", "backDown.png",
    "selectUp.png", "selectDown.png",
    "buyUp.png", "buyDown.png",
    "Car2.txt", "Car3.txt", "cash.txt",
]

executables = [Executable("cargame.py")]

setup(
    name="Traffic Driver",
    version="1.0",
    description="Traffic car game",
    options={
        "build_exe": {
            "packages": ["pygame"],
            "include_files": include_files,
        }
    },
    executables=executables,
)
