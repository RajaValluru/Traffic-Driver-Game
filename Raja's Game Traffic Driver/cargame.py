"""Bike Game"""
import pygame
import time
import random

pygame.init()


pygame.mixer.music.load('a7.mp3')
#colors
white=(255,255,255)
black=(0,0,0)
red= (225,0,0)
green=(20,12,124)
blue=(0,200,0)
yellow=(255,255,0)
lavender=(40,183,200)
g=(0,180,0)

#declaring time
clock = pygame.time.Clock()

#display dimensions
dw=828
dh=700

#fps
lvl=40
#dimensions
cT=40
cH=80
pedH=20
pedT=10
pedL=True

#files
grassyRoad1=grassyRoad3=pygame.image.load("road1.png")
grassyRoad2=pygame.image.load("road2.png")
sideBoard=pygame.image.load('sideBoard.png')

playerCar1=pygame.image.load("car.png")
playerCar2=pygame.image.load("playerCar2.png")
playerCar3=pygame.image.load("playerCar3.png")
ped1=pygame.image.load("ped1.png")
deadped1=pygame.image.load("deadped1.png")
ped2=pygame.image.load("ped2.png")
deadped2=pygame.image.load("deadped2.png")
ped3=pygame.image.load("ped3.png")
deadped3=pygame.image.load("deadped3.png")

car2=pygame.image.load("car2.png")
car3=pygame.image.load("car3.png")
truck1=pygame.image.load("truck1.png")




randomCars=[[35,80],[41,90],[32,80]]


peds=[ped1,ped2,ped3]
deadpeds=[deadped1,deadped2,deadped3]
pedPos=[5,270,543]

#Display font and Window, Window Header
smallFont=pygame.font.SysFont("kristenitc",10)
medFont=pygame.font.SysFont("kristenitc",20)
largeFont=pygame.font.SysFont("ravie",50)
gameDisplay = pygame.display.set_mode((dw,dh))    #creating surface
pygame.display.set_caption("Traffic Driver")

#menu screen
menuScreen=pygame.image.load('menu.png')
playUp=pygame.image.load('playUp.png')
playDown=pygame.image.load('playDown.png')
garageUp=pygame.image.load('garageUp.png')
garageDown=pygame.image.load('garageDown.png')
quitUp=pygame.image.load('quitUp.png')
quitDown=pygame.image.load('quitDown.png')
backUp=pygame.image.load('backUp.png')
backDown=pygame.image.load('backDown.png')
selectUp=pygame.image.load('selectUp.png')
selectDown=pygame.image.load('selectDown.png')
buyDown=pygame.image.load('buyDown.png')
currentCar=playerCar1
Car2File=open('Car2.txt')
Car2=int(Car2File.read(10))
Car2File.close()

Car3File=open('Car3.txt')
Car3=int(Car3File.read(10))
Car3File.close()

def cursorOnButton(curXY,x1,y1,x2,y2):
    if(x1<curXY[0]<x2 and y1<curXY[1]<y2):
        return True

def spawnPed(carPosX,carPosY,pedPosY,life,ped,deadped,pedPosX):

    
    if(crash(carPosX,carPosY,pedPosX,pedPosY,cT,cH,pedH,pedT)):
        life=False
    if(life==False):
            gameDisplay.blit(deadped,[pedPosX,pedPosY])
    elif(life==True):
            gameDisplay.blit(ped,[pedPosX,pedPosY])
    pygame.display.update()
    return life


def text_objects1(text,color,size):
    if size=='small':
        textSurface=smallFont.render(text,True,color)
    elif size=='med':
        textSurface=medFont.render(text,True,color)
    elif size=='large':
        textSurface=largeFont.render(text,True,color)
    return textSurface,textSurface.get_rect()

def message1(msg,color,WC,HC,yDisplace=0,size="small"):
    textSurf,textRect=text_objects(msg,color,size)
    textRect.center = WC,HC+yDisplace
    gameDisplay.blit(textSurf,textRect)
   


def text_objects(text,color,size):
    if size=='small':
        textSurface=smallFont.render(text,True,color)
    elif size=='med':
        textSurface=medFont.render(text,True,color)
    elif size=='large':
        textSurface=largeFont.render(text,True,color)
    return textSurface,textSurface.get_rect()

#to print a message on screen
def message(msg,color,yDisplace=0,size="small"):
    textSurf,textRect=text_objects(msg,color,size)
    textRect.center = (dw/2),(dh/2)+yDisplace
    gameDisplay.blit(textSurf,textRect)


 #rotation of image about center
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image



def store(currentCar):
    G=True
    temp=0
    while G:
        Car2File=open('Car2.txt')
        Car2=int(Car2File.read(1))
        Car2File.close()
        Car3File=open('Car3.txt')
        Car3=int(Car3File.read(1))
        Car3File.close()
        cur=pygame.mouse.get_pos()
        gar=pygame.image.load('garage.png')
        gameDisplay.blit(gar,[0,0])
        cashFile=open('cash.txt')
        cash=long(cashFile.read(8))
        cashFile.close()
        message('Money:'+str(cash),g,220,'med')
        pygame.display.update()
        if(cursorOnButton(cur,36,41,124,88)):
            gameDisplay.blit(backDown,[36,41])
            temp=1
        elif(cursorOnButton(cur,34,479,198,546)):
            gameDisplay.blit(selectDown,[34,479])
            temp=2


        if(Car2==0):
            if(cursorOnButton(cur,327,479,427,536)):
                gameDisplay.blit(buyDown,[327,479])
                temp=3
        elif(Car2==1):
            gameDisplay.blit(selectUp,[302,476])
            if(cursorOnButton(cur,302,476,466,543)):
                gameDisplay.blit(selectDown,[302,476])
                temp=4            


        if(Car3==0):
            if(cursorOnButton(cur,612,479,709,535)):
                gameDisplay.blit(buyDown,[612,479])
                temp=5
        elif(Car3==1):
            gameDisplay.blit(selectUp,[608,479])
            if(cursorOnButton(cur,608,479,735,543)):
                gameDisplay.blit(selectDown,[608,479])
                temp=6

        pygame.display.update()
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit()
                quit()
            elif e.type==pygame.MOUSEBUTTONDOWN:
                if temp==1:
                    intro(currentCar)
                elif temp==2:
                    
                    currentCar=playerCar1
                elif temp==3:
                    cashFile=open('cash.txt')
                    cash=long(cashFile.read(8))
                    cashFile.close()
                    if(cash>=20000):
                        cash-=20000
                        cashFile=open('cash.txt','w')
                        cashFile.write(str(cash))
                        cashFile.close()
                        Car2File=open('Car2.txt','w')
                        Car2File.write('1')
                        Car2File.close()
                        message('You Bought This Benz Car',green,-20,'large')
                        pygame.display.update()
                        time.sleep(1)
                        
                    else:
                        message('Not Enough Cash',red,-20,'large')
                        pygame.display.update()
                        time.sleep(1)
                elif temp==4:
                    currentCar=playerCar2
                elif temp==5:
                    cashFile=open('cash.txt')
                    cash=long(cashFile.read(8))
                    cashFile.close()
                    if(cash>=100000):
                        cash-=100000
                        cashFile=open('cash.txt','w')
                        cashFile.write(str(cash))
                        cashFile.close()
                        Car3File=open('Car3.txt','w')
                        Car3File.write('1')
                        Car3File.close()
                        message('You Bought This F1 Car',green,-20,'large')
                        pygame.display.update()
                        time.sleep(1)
                    else:
                        message('Not Enough Cash',red,-20,'large')
                        pygame.display.update()
                        time.sleep(1)
                elif temp==6:
                    currentCar=playerCar3
                                   


def crash(carPosX,carPosY,polePosX,polePosY,carR,carH,pT,pH):
    if(((carPosX >= polePosX and carPosX <= polePosX+pT)or (carPosX+carR >= polePosX and carPosX+carR<= polePosX+pT)) and ((carPosY >= polePosY and carPosY <= polePosY+pH)or (carPosY+carH >= polePosY and carPosY+carH<= polePosY+pH))):
       return True

    elif(((carPosX >= polePosX and carPosX <= polePosX+pT)or (carPosX+carR >= polePosX and carPosX+carR<= polePosX+pT)) and ((carPosY >= polePosY and carPosY <= polePosY+pH)or (carPosY+carH >= polePosY and carPosY+carH<= polePosY+pH))):
       return True
def instruction():
    J=True
    while J:
        gameDisplay.fill(lavender)
        message("Avoid crashing into other cars",yellow,20,'med')
        message("More Score=more money",yellow,50,'med')
        message("Use money to buy cars",yellow,80,'med')
        message("'B' for back",green,120,'med')
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.KEYDOWN:
                if e.key==pygame.K_b:
                    J=False
        


def intro(currentCar):
    I=True

    pygame.mixer.music.play(-1)
    
    while I:
        gameDisplay.fill(yellow)
        gameDisplay.blit(menuScreen,[0,0])
        cur=pygame.mouse.get_pos()
        if(cursorOnButton(cur,320,405,473,484)):
            gameDisplay.blit(playDown,[320,405])
            
            temp=1
          
        elif(cursorOnButton(cur,333,500,462,552)):
            temp=2
            gameDisplay.blit(garageDown,[333,500])
        elif(cursorOnButton(cur,350,567,443,619)):
            temp=3
            gameDisplay.blit(quitDown,[350,567])
        else:
            temp=0
        pygame.display.update()
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit()
                quit()
            elif e.type==pygame.MOUSEBUTTONDOWN:
                if temp==1:
                    pygame.mixer.music.stop()
                    game(currentCar,grassyRoad1,grassyRoad2,grassyRoad3)
                elif temp==2:
                    store(currentCar)
                elif temp==3:
                    pygame.quit()
                    quit()

def game(p1Car,road1,road2,road3):
    pygame.mixer.music.load('run.mp3')
    pygame.mixer.music.play(-1)
    gameExit= False
    gameOver=[False,False]
    #rotation of car
    rotateRight=360
    rotateRight_changeA=0
    rotateRight_changeB=0
    rotateLeft=0
    rotateLeft_changeA=0
    rotateLeft_changeB=0
    rrUB=351
    rlUB=9
    rrLB=360
    rlLB=0
    transRight=0
    transLeft=0
    fTrans='none'
    pedL=True
    extraCash=0
    score=0
    cashFile=open('cash.txt')
    cash=int(cashFile.read(10))
    cashFile.close()

    #random cars
    carspeedList1=[0,0,0,0,0,0,0]
    carspeedList2=[0,0,0,0,0,0,0]
    carspeedList3=[0,0,0,0,0,0,0]
    randCarD1=[0,0,0,0,0,0]
    randCarD2=[0,0,0,0,0,0]
    randCarD3=[0,0,0,0,0,0]
    cars=[truck1,car2,car3]
    carpos=[44,98,156,210,270,320,384,435,493,547]
    randX1List=[0,0,0,0,0,0,0]
    randX2List=[0,0,0,0,0,0,0]
    randX3List=[0,0,0,0,0,0,0]
    randY1List=[850,850,850,850,850,850]
    randY2List=[-150,-150,-150,-150,-150,-150]
    randY3List=[1200,1200,1200,1200,1200,1200]
    randcarList1=[car2,car2,car2,car2,car2,car2]
    randcarList2=[car2,car2,car2,car2,car2,car2]
    randcarList3=[car2,car2,car2,car2,car2,car2]

    #Movement of car

    rY_speed=0.0
    rY_accel=0.0
    rY_deccel=0.0
    r2X=0
    r2Y=-700
    r3Y=-1400
    r3X=0
    r1X=0
    r1Y=0
    d=0
    u=0


    carRotated=p1Car
    pos2X=320
    pos2Y=450
    


    #ped
    randPedY=800
    

    while not gameExit:
        
#if game over,will go into loop
        if (gameOver[0] or gameOver[1]):
            pygame.mixer.music.stop()
            pygame.mixer.music.load('cc.mp3')
            pygame.mixer.music.play(1,28)
            cash+=int(extraCash)
            cashFile=open('cash.txt','w')
            cashFile.write(str(int(cash)))
            cashFile.close()
            while gameOver[0] or gameOver[1]:
                #ask if we want to play again
                message("You Crashed",red,-100,'large')
                pygame.display.update()
                time.sleep(1)
                gameDisplay.fill(green)
                message("+"+str(int(extraCash)),blue,-40,'med')
                message("Total Money: "+str(int(cash)),blue,0,'med')
                message("B to play again",yellow,40,'med')
                message("Q to quit",yellow,65,'med')
                pygame.display.update()
                
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            gameExit = True
                            gameOver[0]=gameOver[1]=False
                        elif event.key == pygame.K_b:
                            intro(p1Car)
                    elif event.type==pygame.QUIT:
                        gameExit=True
                        gameOver[0]=gameOver[1]=False



                    
        gameDisplay.fill(white)
        gameDisplay.blit(road1,[r1X,r1Y])
        gameDisplay.blit(road2,[r2X,r2Y])
        gameDisplay.blit(road3,[r3X,r3Y])
        gameDisplay.blit(sideBoard,[628,0])
        message1(str(score),yellow,728,104,0,'med')
        
        for e in pygame.event.get():
      
            if e.type==pygame.QUIT:
                pygame.quit()
                quit()
            elif (e.type == pygame.KEYDOWN):
                if e.key == pygame.K_UP:
                    if(d==0):
                        rY_accel=0.3
                        rY_deccel=0
                        u=1
                elif e.key == pygame.K_DOWN:
                    if(u==0):
                        rY_accel=0
                        rY_deccel=3
                        d=1
                elif e.key == pygame.K_RIGHT:
                        if(rY_speed>0.5 and fTrans=='none'):
                            rotateRight_changeA=-3
                            rotateRight_changeB=0
                            transRight=7
                            fTrans='right'
                elif e.key == pygame.K_LEFT:
                        if(rY_speed>0.5 and fTrans=='none'):
                            rotateLeft_changeA=3
                            rotateLeft_changeB=0
                            transLeft=-7
                            fTrans='left'
                
                    
            elif (e.type==pygame.KEYUP):
                if e.key == pygame.K_UP:
                    if(u==1):
                        rY_accel=0
                        rY_deccel=0.2
                        u=0
                    
                elif e.key == pygame.K_DOWN:
                    if(d==1):
                        d=0
                        rY_accel=0
                        rY_deccel=0.2
                elif e.key == pygame.K_RIGHT:

                        if(rY_speed>.5 and fTrans=='right'):
                            
                            rotateRight_changeB=-3
                            rotateRight_changeA=0
                            transRight=0
                            fTrans='rightback'    
                elif e.key == pygame.K_LEFT:

                        if(rY_speed>.5 and fTrans=='left'):
                            rotateLeft_changeA=0
                            rotateLeft_changeB=3
                            transLeft=0
                            fTrans='leftback'

                
        if(rY_speed>=0 and rY_speed<34):
            rY_speed+=rY_accel
        if(rY_speed>0 and rY_speed<38):
            rY_speed-=rY_deccel
        if(rY_speed<0):
            rY_speed=0
        r1Y+=rY_speed
        r2Y+=rY_speed
        r3Y+=rY_speed
        if(r1Y>1400):
            r1Y=0
            r2Y=-700
            r3Y=-1400
        if(rY_speed<5):
            rotateRight=360
            rotateLeft=0
            transRight=0
            transLeft=0
        if(rY_speed>10 and pos2X+10<250):
            score+=int(rY_speed*2)
            extraCash+=0.2
        elif(rY_speed>10):
            score+=int(rY_speed)
            extraCash+=0.1
        #pedestrian
        if(randPedY>700):
            randPedY=random.randrange(-2000,-20)
            pedL=True
            pedNo=random.randrange(0,3)
            ped=peds[pedNo]
            deadped=deadpeds[pedNo]
            pedpos=random.randrange(0,3)
            pedX=pedPos[pedpos]
        randPedY+=rY_speed
        pedL=spawnPed(pos2X,pos2Y,randPedY,pedL,ped,deadped,pedX)
        
        

        #car rotation

        if(fTrans=='right' or fTrans=='rightback'):
            if(rotateRight<=rrLB and rotateRight>rrUB):
                rotateRight+=rotateRight_changeA
            if(rotateRight<rrLB and rotateRight>=rrUB):
                rotateRight-=rotateRight_changeB
        elif(fTrans=='left' or fTrans=='leftback'):
            if(rotateLeft>=rlLB and rotateLeft<rlUB):
                rotateLeft+=rotateLeft_changeA
            if(rotateLeft>rlLB and rotateLeft<=rlUB):
                rotateLeft-=rotateLeft_changeB
        if(fTrans=='leftback' or fTrans=='rightback'):
            if(rotateRight>=rrLB or rotateLeft<=rlLB):
                fTrans='none'
                rotateLeft_changeB=0
                rotateRight_changeB=0
        
        
        if fTrans == 'right' or fTrans == 'rightback':
            carRotated=rot_center(p1Car,rotateRight)
            pos2X+=transRight
        elif fTrans == 'left' or fTrans == 'leftback':
            carRotated=rot_center(p1Car,rotateLeft)
            pos2X+=transLeft
        else:
            carRotated=p1Car
        gameDisplay.blit(carRotated,[pos2X,pos2Y])
        #random cars
        for i in range(0,2,1):
            if gameOver[0]:
                break
            if(randY1List[i]>700):
                randcarY=random.randrange(-1200,-20)
                randY1List[i]=randcarY
                
                carNo=random.randrange(0,3)
                randX1List[i]=carpos[random.randrange(0,5)]
                randcarList1[i]=pygame.transform.rotate(cars[carNo],180)
                carspeedList1[i]=random.randrange(5,12)
                randCarD1[i]=carNo
            randY1List[i]+=rY_speed+carspeedList1[i]
            gameDisplay.blit(randcarList1[i],[randX1List[i]-33,randY1List[i]]) 
            gameOver[0]=crash(pos2X+3,pos2Y,randX1List[i],randY1List[i],cT-3,cH,randomCars[randCarD1[i]][0],randomCars[randCarD1[i]][1])
            if gameOver[0]:
                break
        for i in range(0,3,1):
            if gameOver[0]:
                break
            if(randY2List[i]<-149):
                randcarY=(random.randrange(1200,1500))
                randY2List[i]=randcarY
                carNo=random.randrange(0,3)
                randX2List[i]=carpos[random.randrange(5,10)]
                randcarList2[i]=cars[carNo]
                carspeedList2[i]=random.randrange(10,20)
                randCarD2[i]=carNo
            randY2List[i]+=rY_speed-carspeedList2[i]
            gameDisplay.blit(randcarList2[i],[randX2List[i],randY2List[i]]) 
            gameOver[0]=crash(pos2X+3,pos2Y,randX2List[i],randY2List[i],cT-3,cH,randomCars[randCarD2[i]][0],randomCars[randCarD2[i]][1])
            if gameOver[0]:
                break
            if(randY3List[i]>1000):
                randcarY=(random.randrange(-2000,-100))
                randY3List[i]=randcarY
                carNo=random.randrange(0,3)
                randX3List[i]=carpos[random.randrange(5,10)]
                randcarList3[i]=cars[carNo]
                carspeedList3[i]=random.randrange(10,20)
                randCarD3[i]=carNo
            randY3List[i]+=rY_speed-carspeedList3[i]
            gameDisplay.blit(randcarList3[i],[randX3List[i],randY3List[i]]) 
            gameOver[0]=crash(pos2X+2,pos2Y,randX3List[i],randY3List[i],cT-2,cH,randomCars[randCarD3[i]][0],randomCars[randCarD3[i]][1])
            if gameOver[0]:
                break
               
        if(pos2X+cT+5>608 or pos2X<20):
            gameOver[1]=True
        
        pygame.display.update()
        
        clock.tick(lvl)

    pygame.quit()
    quit()


intro(playerCar1)

                
                
                
            










                
