import numpy as np
import random

from config import Config
from src.Car import Car
from optimizer.RewardFunction import calculateReward

class Map:
    def __init__(self, agent, server) -> None:
        self.mapWidth = Config.mapWidth
        self.mapHeight = Config.mapHeight
        self.carList = []
        self.coverMap = np.zeros([self.mapHeight, self.mapWidth])
        self.carPosMap = np.zeros([self.mapHeight, self.mapWidth])
        self.unCoverPeriod = Config.unCoverPeriod
        self.rewardMap = np.zeros([self.mapHeight, self.mapWidth])
        self.server = server
        self.agent = agent
        self.time = 0
        self.reward = 0
        
    def run(self, epsilon, writer, memory, step):
        self.resetRewardMap()
        if len(self.carList) > 0:
            for car in self.carList:
                car.setObservation(self.coverMap, self.carPosMap)
                
            for car in self.carList:
                car.action(self.server, epsilon)
                    
            previousCoverMap = np.copy(self.coverMap)
            self.updateCoverMap()
            
            totalReward = self.calcReward()
            self.reward += totalReward
            
            for car in self.carList:
                car.setNextObservation(self.coverMap, self.carPosMap)
                memory.add([car.observation, car.state, car.reward, car.nextObservation])
            
            # for car in self.carList:
            #     writer.add_image(f'Car {car.x}-{car.y} observation at {step}', car.observation[0], 0, dataformats='HW')
            #     writer.add_image(f'Car {car.x}-{car.y} next observation at {step}', car.nextObservation[0], 0, dataformats='HW')
            
            if step % 100 == 0 and step > 0:
                sampleList = random.sample(self.carList, 5)
                for car in sampleList:
                    writer.add_image(f'Cover map of car{car.x}-{car.y} at step:{step}', car.observation[0], 0, dataformats='HW')
                    writer.add_image(f'Car position map of car{car.x}-{car.y} at step:{step}', car.observation[1], 0, dataformats='HW')
                    writer.add_image(f'Next observation map of car{car.x}-{car.y} at step:{step}', car.nextObservation[0], 0, dataformats='HW')
            
            writer.add_scalar('Cover rate', self.calcCoverRate(), step)
            writer.add_scalar('Overlap rate', self.calcOverlapRate(previousCoverMap), step)
            writer.add_scalar('Car overlap rate', self.calcCarOverlap(), step)
            writer.add_scalar('Number of car', len(self.carList), step)
            writer.add_scalar('Sending rate', self.countOnCar() / len(self.carList), step)
            writer.add_scalar('Reward', totalReward, step)
            
            for car in self.carList:
                car.run()
        # else:
            # print('Map has not cars')
        
        if self.time % self.unCoverPeriod == 0 and self.time != 0:
            self.coverMap -= 1
            self.coverMap = np.where(self.coverMap > 0, self.coverMap, 0)

        self.generateCar()
        self.removeInvalidCar()
        self.updateCarPosition()
        # writer.add_image(f'Car position map-{step}', self.carPosMap, 0, dataformats='HW')
        self.time += 1
        
    def generateCar(self):
        addedCarAmount = random.randint(0, Config.generationAmount)
        
        for _ in range(addedCarAmount):
            addedCar = Car(random.randint(0, Config.maxVelocity), random.randint(0, self.mapWidth - 1), self.agent)
            addedCar.setObservation(self.coverMap, self.carPosMap)
            self.carList.append(addedCar)
        
    def removeInvalidCar(self):
        removeCarList = []
        for car in self.carList:
            if car.x >= self.mapHeight:
                removeCarList.append(car)
        
        for removedCar in removeCarList:
            for car in self.carList:
                if removedCar == car:
                    self.carList.remove(car)
            
    def updateCarPosition(self):
        self.carPosMap = np.zeros([Config.mapHeight, Config.mapWidth])
        for car in self.carList:
            self.carPosMap[car.x, car.y] = 1
        
    def updateCoverMap(self):
        for car in self.carList:
            if car.state == Config.action["ON"]:
                self.setCover(car.x, car.y)
        self.coverMap = np.where(self.rewardMap >= 1, 1, self.coverMap)
        
    def setCover(self, x, y):
        for i in range(max(0, x - Car.coverRange), min(self.mapHeight, x + Car.coverRange + 1)):
            for j in range(max(0, y - Car.coverRange), min(self.mapWidth, y + Car.coverRange + 1)):
                self.rewardMap[i, j] += 1
                
    def addCar(self, car):
        self.carList.append(car)
        
    def calcReward(self):
        totalReward = 0
        for car in self.carList:
            reward = calculateReward(car, self.rewardMap)
            car.setReward(reward)
            totalReward += reward

        totalReward /= len(self.carList)
        return totalReward

    def resetRewardMap(self):
        self.rewardMap = np.zeros([self.mapHeight, self.mapWidth])
    
    def calcCoverRate(self):
        coverRate = self.coverMap.sum() / (self.mapHeight * self.mapWidth)
        return coverRate
    
    def countOnCar(self):
        count = 0
        for car in self.carList:
            if car.state == Config.action["ON"]:
                count += 1
        return count
    
    def calcOverlapRate(self, previousCoverMap):
        overlap = np.where(previousCoverMap * self.rewardMap > 0 , 1, 0).sum()
        overlap /= (Config.mapHeight * Config.mapWidth)
        return overlap

    def calcCarOverlap(self):
        overlapMap = self.rewardMap - 1
        overlap = np.where(overlapMap > 0, overlapMap, 0).sum()
        overlap /= (self.countOnCar() * (Config.coverRange * 2 + 1))        
        return overlap
        
    def showCarMap(self, time):
        # simg = np.stack((self.carPosMap, self.carPosMap, self.carPosMap), axis=0)
        # print(simg.shape)
        # img = Image.fromarray(simg, 'L')
        # img.save(f'CarPosition{time}.png')
        # coverimg = Image.fromarray(self.coverMap, 'L')
        # coverimg.save(f'CoverMap{time}.png')
        # # img.show()
        print('Car\'s position map')
        print(self.carPosMap)
        print('Cover map')
        print(self.coverMap)
        # print(coverimg)
    
    def resetMap(self):
        self.carList = []
        self.coverMap = np.zeros([self.mapHeight, self.mapWidth])
        self.carPosMap = np.zeros([self.mapHeight, self.mapWidth])
        self.rewardMap = np.zeros([self.mapHeight, self.mapWidth])
        self.time = 0
        self.server.resetServer()
        self.reward = 0
    
    def set_seed(self, seed):
        np.random.seed(seed)
        for car in self.carList:
            car.set_seed(seed)