import cx_Freeze

executables=[cx_Freeze.Executable("cargame.py")]

cx_Freeze.setup(
        name="Traffic Driver",
        options ={"build.exe":{"packages":["pygame"],"include_files":["a7.mp3","backDown.png","backUp.png","buyDown.png","buyUp.png",'car.png','car2.png','Car2.txt','car3.png','Car3.txt','cash.txt','cc.mp3','deadped1.png','deadped2.png','deadped3.png','garage.png','garageDown.png','garageUp.png','menu.png','ped1.png','ped2.png','ped3.png','playDown.png','playerCar2.png','playerCar3.png','playUp.png','pole.jpg','quitDown.jpg','quitUp.png','road1.png','road2.png','run.mp3','selectDown.png','selectUp.png','sideBoard.png','truck1.png']}},
        description='Traffic car game',
        executables=executables
        )
        
                                                                      
