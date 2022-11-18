import json
import os
import random
import shutil
import signal
import socket
import string
import subprocess
import sys
import threading
import time

state = "idle"
nodeIPaddrs = []
Process = ""
processID = ""
isManualCMD = ""


def handlePolling(state):
    """Respond to polling from other nodes with state information"""
    # *TCP current state to polling node*
    pass


def waitForProcessCMD() -> tuple:
    return True, "process"


def startProcessThread(process):
    pass


def handleMigration():
    pass


def handleReboot():
    pass


def handleShutdown():
    pass


def readVoltagefromGPIO() -> float:
    """Read voltage from GPIO"""
    return 0.0


def readCurrentfromGPIO() -> float:
    """Read current from GPIO"""
    return 0.0


def isLossOfPower() -> bool:
    """Decide when node is losing power"""
    voltage = readVoltagefromGPIO()
    current = readCurrentfromGPIO()
    threshold = 0.5
    return (voltage < threshold or current < threshold)


def startProcessThread(process):
    """Handle starting a process"""
    # If no checkpoint
    # *Start Process in separate thread*
    # Else if checkpoint
    # *Start process in separate thread and resume from checkpoint*
    pass


def NetworkScan() -> None:
    """Scan network ping scan for available nodes"""
    global nodeIPaddrs
    #import netifaces
    selfIP = socket.gethostbyname(socket.gethostname())
    for i in range(1, 255):
        ip = "192.168.137." + str(i)
        response = os.system("ping -c 1 " + ip)
        if response == 0:
            nodeIPaddrs.append(ip)
    # incomplete


def manualInput() -> bool:
    """Handle manual input from user"""
    return False


def waitForMigrateCMD() -> tuple[bool, bool]:
    """Handle migrate command"""
    if (isLossOfPower()):  # Check for loss of power or manual input command
        return True, False
    elif manualInput():
        return True, True
    else:
        return False, False


def pollNodeforState(address) -> str:
    """Poll node at given address to get state"""
    # *TCP address for Node State*
    statefromNode = "idle"
    return statefromNode


def waitForProcessCMD():
    # #Check specified directory for files
    # Process = (check directory, if not empty, then it should contain a process and checkpoint)
    # If Process != none
    # Return Process, true
    # Else
    #	Return none, false
    pass


def CheckpointandSaveProcessToDisk(processID, process):
    """Handle case of no available nodes, checkpoint process to current working directory"""
    # *Run bash Script to checkpoint node and Save to receiving directory on current node*
    # *That way, on startup any files inside the directory will immediately be restored from
    # Checkpoint and resumed on system*
    pass


def checkpointAndMigrateProcessToNode(processID, process, ipToSend):
    # Handle checkpointing and migration
    # *Run bash Script to checkpoint node and SCP to address in specific directory*
    # *Delete process and supporting files on current node*
    pass


def migrateProcessToAvaliableNode(processID, process):
    global state
    ipToSend = None
    for address in nodeIPaddrs:
        state = pollNodeforState(address)
        if state == "idle":
            if ipToSend == None:
                ipToSend = address
            else:
                # * Possible comparison for other factors like time, weather, etc.*
                ipToSend = address
    if ipToSend == None:
        CheckpointandSaveProcessToDisk(processID, process)
    else:
        checkpointAndMigrateProcessToNode(processID, process, ipToSend)


def getProcessID() -> int:
    # *Get process ID from process*
    return 0


def sendProcessResultsToUser():
    pass


def handleStates(state):
    """Main FSM"""
    if state == "idle":  # Idle State, should look inside project directory for files to run
        processReceived, process = waitForProcessCMD()
        if processReceived:
            state = "processing"
            startProcessThread(process)

    if state == "processing":  # Processing State, continue processing until finished or until migration command initiated
        migrate, isManualCMD = waitForMigrateCMD()
        if migrate:
            state = "migrating"
            processID = getProcessID()  # If complete, send output logs or finished process results back to user
        elif process.isComplete():
            state = "idle"
            sendProcessResultsToUser()
    if state == "migrating":
        migrateProcessToAvaliableNode(processID, process)
        # if migration command is manual, then keep the node in idle, else send to shutdown state
        if isManualCMD:
            state = "idle"
        else:
            state = "shutdown"
    # Node will shut down eventually with loss of power, but potentially leaving the option to return to
    # Idle state if power does return and node somehow still can operate
    if state == "shutdown":
        if not isLossOfPower():
            state = "idle"
    return state


if __name__ == '__main__':
    state = "idle"
    # while True:
    #    state = handleStates(state)
    #    handlePolling(state)