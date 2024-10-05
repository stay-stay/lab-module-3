import logging
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.ActuatorData import ActuatorData


class BaseActuatorSimTask:
    """
    Base class for actuator simulation tasks.
    """

    def __init__(self, name: str = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE,
                 simpleName: str = "Actuator"):
        # Initialize the latest actuator response
        self.latestActuatorResponse = ActuatorData(typeID=typeID, name=name)
        self.latestActuatorResponse.setAsResponse()

        # Store the name, typeID, and simpleName for logging purposes
        self.name = name
        self.typeID = typeID
        self.simpleName = simpleName

        # Store the last known command and value
        self.lastKnownCommand = ConfigConst.DEFAULT_COMMAND
        self.lastKnownValue = ConfigConst.DEFAULT_VAL

    def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        """
        Private method to simulate actuator activation.
        """
        msg = "\n*******\n* O N *\n*******\n" + self.name + " VALUE -> " + str(val) + "\n======="
        logging.info("Simulating %s actuator ON: %s", self.name, msg)

        # For now, return 0 to indicate success
        return 0

    def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        """
        Private method to simulate actuator deactivation.
        """
        msg = "\n*******\n* OFF *\n*******"
        logging.info("Simulating %s actuator OFF: %s", self.name, msg)

        # For now, return 0 to indicate success
        return 0

    def updateActuator(self, data: ActuatorData) -> ActuatorData:
        """
        Update the actuator based on the provided ActuatorData.
        """
        if data and self.typeID == data.getTypeID():
            statusCode = ConfigConst.DEFAULT_STATUS
            curCommand = data.getCommand()
            curVal = data.getValue()

            # Check if the command and value are the same as the last known values
            if curCommand == self.lastKnownCommand and curVal == self.lastKnownValue:
                logging.debug("New actuator command and value is a repeat. Ignoring: %s %s", str(curCommand),
                              str(curVal))
            else:
                logging.debug("New actuator command and value to be applied: %s %s", str(curCommand), str(curVal))

                # Execute the command based on ON or OFF
                if curCommand == ConfigConst.COMMAND_ON:
                    logging.info("Activating actuator...")
                    statusCode = self._activateActuator(val=data.getValue(), stateData=data.getStateData())
                elif curCommand == ConfigConst.COMMAND_OFF:
                    logging.info("Deactivating actuator...")
                    statusCode = self._deactivateActuator(val=data.getValue(), stateData=data.getStateData())
                else:
                    logging.warning("ActuatorData command is unknown. Ignoring: %s", str(curCommand))
                    statusCode = -1

                # Update the last known command and value
                self.lastKnownCommand = curCommand
                self.lastKnownValue = curVal

                # Create the ActuatorData response
                actuatorResponse = ActuatorData()
                actuatorResponse.updateData(data)
                actuatorResponse.setStatusCode(statusCode)
                actuatorResponse.setAsResponse()

                # Update the latest actuator response
                self.latestActuatorResponse.updateData(actuatorResponse)

                return actuatorResponse

        return None

