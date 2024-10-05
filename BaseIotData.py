class BaseIotData:
    def __init__(self, name: str = "Not Set", typeID: int = -1):
        self.name = name
        self.typeID = typeID
        self.statusCode = 0
        self.timeStamp = None

    def updateTimeStamp(self):
        # Implement time-stamping logic here (e.g., with datetime.now())
        pass

    # Accessor methods for shared properties
    def getName(self) -> str:
        return self.name

    def getTypeID(self) -> int:
        return self.typeID

    def getStatusCode(self) -> int:
        return self.statusCode

    def getTimeStamp(self):
        return self.timeStamp

    def setName(self, name: str):
        self.name = name

    def setTypeID(self, typeID: int):
        self.typeID = typeID

    def setStatusCode(self, statusCode: int):
        self.statusCode = statusCode
        self.updateTimeStamp()

    def _handleUpdateData(self, data):
        # This method will be overridden by subclasses
        pass
