from multiprocessing.connection import answer_challenge

# elevatorID= 1
# CallButtonID = 1 

class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators):
        self.ID = _id
        self.amountOfFloors = _amountOfFloors
        self.amountOfElevators = _amountOfElevators
        self.status = "status"
        self.elevatorList = []
        self.callButtonList = []
        self.createElevators(_amountOfFloors, _amountOfElevators)
        self.createCallButtons(_amountOfFloors)
        
        
    def createCallButtons(self, _amountOfFloors):
        callButtonID = 1
        buttonFloor = 1
        for i in range(_amountOfFloors):
            if buttonFloor < _amountOfFloors:
                callButton = CallButton(callButtonID, buttonFloor, 'up')
                self.callButtonList.append(callButton)
                callButtonID += 1
                
            if buttonFloor > 1:
                callButton = CallButton(callButtonID, buttonFloor, 'down')
                self.callButtonList.append(callButton)
                callButtonID += 1
        
            buttonFloor += 1
    
    
    def createElevators(self, _amountOfFloors, _amountOfElevators):
        elevatorID = 1
        for i in range(_amountOfElevators):
            elevator = Elevator(elevatorID, _amountOfFloors)
            self.elevatorList.append(elevator)
            elevatorID += 1
    
    def requestElevator (self, floor, direction):
        elevator = self.findElevator(floor, direction) 
        elevator.floorRequestList.append(floor)
        elevator.move()
        return elevator

    def findElevator (self, requestedFloor, requestedDirection):
        bestElevatorInformations = {
        "bestElevator" : 0,
        "bestScore" : 5,
        "referenceGap" : 10000000
        }
        for elevator in list(self.elevatorList):
            if requestedFloor == elevator.currentFloor and elevator.status == "stopped" and requestedDirection == elevator.direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(1, elevator, bestElevatorInformations, requestedFloor)
                
            elif requestedFloor > elevator.currentFloor and elevator.direction == "up" and requestedDirection == elevator.direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(2, elevator, bestElevatorInformations, requestedFloor)

            elif requestedFloor < elevator.currentFloor and elevator.direction == "down" and requestedDirection == elevator.direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(2, elevator, bestElevatorInformations, requestedFloor)

            elif elevator.status == "idle":
                bestElevatorInformations = self.checkIfElevatorIsBetter(3, elevator, bestElevatorInformations, requestedFloor)
        
        return bestElevatorInformations["bestElevator"]        


    def checkIfElevatorIsBetter (self, scoreToCheck, newElevator, bestElevatorInformations, floor):
        if scoreToCheck < bestElevatorInformations["bestScore"]:
            bestElevatorInformations["bestScore"] = scoreToCheck
            bestElevatorInformations["bestElevator"] = newElevator
            bestElevatorInformations["referenceGap"] = abs(newElevator.currentFloor - floor)
        
        elif bestElevatorInformations["bestScore"] == scoreToCheck:
            gap = abs(newElevator.currentFloor - floor)
            if bestElevatorInformations["referenceGap"] > gap:
                bestElevatorInformations["bestElevator"] = newElevator
                bestElevatorInformations["referenceGap"] = gap
                
        return bestElevatorInformations

        
            


class Elevator:
    def __init__(self, _id, _amountOfFloors):
        self.ID = _id
        self.amountOfFloors = _amountOfFloors
        self.status = "status"
        self.currentFloor = 1
        self.direction = "null"
        self.door = Door(_id)
        self.floorRequestButtonList =[]
        self.floorRequestList = []
        self.floorRequestsButtons(_amountOfFloors)
        
    def floorRequestsButtons(self, _amountOfFloors):
        buttonFloor = 1
        floorRequestButtonId = 1
        for i in range(_amountOfFloors):
            floorRequestButton = FloorRequestButton(floorRequestButtonId, buttonFloor)
            self.floorRequestButtonList.append(floorRequestButton)
            buttonFloor += 1
            floorRequestButtonId +=1
        
        
    def requestFloor(self, floor):
        self.floorRequestList.append(floor)
        self.move()
        
    def move(self):
        while len(self.floorRequestList) != 0:
            destination = self.floorRequestList[0]
            self.status = "moving"
            if self.currentFloor < destination:
                self.direction = "up"
                self.sortFloorList()
                while self.currentFloor < destination:
                    self.currentFloor +=1
                    self.screenDisplay = self.currentFloor
            
            elif self.currentFloor > destination:
                self.direction = "down"
                self.sortFloorList()
                while self.currentFloor > destination:
                    self.currentFloor -= 1
                    self.screenDisplay = self.currentFloor
                    
            self.status = "stopped"
            self.floorRequestList.pop(0)
        
        self.status = "idle"
        
    def sortFloorList(self):
        if self.direction == "up":
            sorted(self.floorRequestList , reverse=False)
        
        elif self.direction == "down":
            sorted(self.floorRequestList , reverse=True)


class CallButton:
    def __init__(self, _id, _floor, _direction):
        self.ID = _id
        self.floor = _floor
        self.direction = _direction
        self.status = "status"

class FloorRequestButton:
    def __init__(self, _id, _floor):
        self.ID = _id
        self.status = "status"
        self.floor = _floor

class Door:
    def __init__(self, _id):
        self.ID = _id
        self.status = "status"