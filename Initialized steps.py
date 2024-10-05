import logging
from apscheduler.schedulers.background import BackgroundScheduler
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator
from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask
from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask
from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask


class SensorAdapterManager:
    def __init__(self):
        self.configUtil = ConfigUtil()

        self.pollRate = self.configUtil.getInteger(
            section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.POLL_CYCLES_KEY,
            defaultVal=ConfigConst.DEFAULT_POLL_CYCLES)

        self.useEmulator = self.configUtil.getBoolean(
            section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.ENABLE_EMULATOR_KEY)

        self.locationID = self.configUtil.getProperty(
            section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.DEVICE_LOCATION_ID_KEY,
            defaultVal=ConfigConst.NOT_SET)

        if self.pollRate <= 0:
            self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES

        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            self.handleTelemetry, 'interval', seconds=self.pollRate,
            max_instances=2, coalesce=True, misfire_grace_time=15)

        self.dataMsgListener = None
        self.humidityAdapter = None
        self.pressureAdapter = None
        self.tempAdapter = None

        if self.useEmulator:
            logging.info("Emulators will be used for sensors.")
        else:
            logging.info("Simulators will be used for sensors.")
            self._initEnvironmentalSensorTasks()

    def _initEnvironmentalSensorTasks(self):
        humidityFloor = self.configUtil.getFloat(
            section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.HUMIDITY_SIM_FLOOR_KEY,
            defaultVal=SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY)

        humidityCeiling = self.configUtil.getFloat(
            section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.HUMIDITY_SIM_CEILING_KEY,
            defaultVal=SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY)

        pressureFloor = self.configUtil.getFloat(
            section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.PRESSURE_SIM_FLOOR_KEY,
            defaultVal=SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)

        pressureCeiling = self.configUtil.getFloat(
            section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.PRESSURE_SIM_CEILING_KEY,
            defaultVal=SensorDataGenerator.HI_NORMAL_ENV_PRESSURE)

        tempFloor = self.configUtil.getFloat(
            section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.TEMP_SIM_FLOOR_KEY,
            defaultVal=SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP)

        tempCeiling = self.configUtil.getFloat(
            section=ConfigConst.CONSTRAINED_DEVICE, key=ConfigConst.TEMP_SIM_CEILING_KEY,
            defaultVal=SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)

        self.dataGenerator = SensorDataGenerator()

        humidityData = self.dataGenerator.generateDailyEnvironmentHumidityDataSet(
            minValue=humidityFloor, maxValue=humidityCeiling, useSeconds=False)

        pressureData = self.dataGenerator.generateDailyEnvironmentPressureDataSet(
            minValue=pressureFloor, maxValue=pressureCeiling, useSeconds=False)

        tempData = self.dataGenerator.generateDailyIndoorTemperatureDataSet(
            minValue=tempFloor, maxValue=tempCeiling, useSeconds=False)

        self.humidityAdapter = HumiditySensorSimTask(dataSet=humidityData)
        self.pressureAdapter = PressureSensorSimTask(dataSet=pressureData)
        self.tempAdapter = TemperatureSensorSimTask(dataSet=tempData)


#### 2. **Data Message Listener Setter**

This
method
allows
us
to
set
a
listener
for handling telemetry data.

```python


def setDataMessageListener(self, listener):
    if listener:
        self.dataMsgListener = listener

