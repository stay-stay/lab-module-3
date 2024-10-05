import random
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataSet


class BaseSensorSimTask:
    # Define class-scoped constants for min and max sensor value
    DEFAULT_MIN_VAL = ConfigConst.DEFAULT_VAL
    DEFAULT_MAX_VAL = 100.0

    def __init__(self, name: str = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE,
                 dataSet: SensorDataSet = None, minVal: float = DEFAULT_MIN_VAL, maxVal: float = DEFAULT_MAX_VAL):
        # Set class-scoped variables to constructor parameters
        self.dataSet = dataSet
        self.name = name
        self.typeID = typeID
        self.dataSetIndex = 0  # Tracks the index of the dataSet
        self.useRandomizer = False  # Flag for using random values

        self.latestSensorData = None  # Holds the latest SensorData

        # If no dataSet is provided, use randomizer for generating telemetry
        if not self.dataSet:
            self.useRandomizer = True
            self.minVal = minVal
            self.maxVal = maxVal

    # Method to return the name of the sensor
    def getName(self) -> str:
        return self.name

    # Method to return the type ID of the sensor
    def getTypeID(self) -> int:
        return self.typeID

    # Method to generate telemetry (sensor readings)
    def generateTelemetry(self) -> SensorData:
        # Create a new SensorData instance
        sensorData = SensorData(typeID=self.getTypeID(), name=self.getName())
        sensorVal = ConfigConst.DEFAULT_VAL

        # If randomizer is used, generate a random value between min and max
        if self.useRandomizer:
            sensorVal = random.uniform(self.minVal, self.maxVal)
        else:
            # Get the next dataSet entry
            sensorVal = self.dataSet.getDataEntry(index=self.dataSetIndex)
            self.dataSetIndex += 1

            # If index exceeds dataSet size, reset to 0
            if self.dataSetIndex >= self.dataSet.getDataEntryCount():
                self.dataSetIndex = 0

        # Set the sensor value and store the latest data
        sensorData.setValue(sensorVal)
        self.latestSensorData = sensorData

        # Return the latest sensor data
        return self.latestSensorData

    # Method to get the current telemetry value (latest sensor reading)
    def getTelemetryValue(self) -> float:
        # If no sensor data exists, generate new telemetry
        if not self.latestSensorData:
            self.generateTelemetry()

        # Return the current value of the latest sensor data
        return self.latestSensorData.getValue()
