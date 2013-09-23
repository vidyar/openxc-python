LITERS_PER_GALLON = 3.78541178
LITERS_PER_UL = .000001
KM_PER_MILE = 1.609344
KM_PER_M = .001

totalOdometerAtRestart = 0
fuelConsumedSinceRestartLiters = 0
rollingOdometerSinceRestart = 0

def handleInverted(signal, value):
    return sendJSONMessage(signal['generic_name'], str(value * -1))

def handleFuelFlow(signal, signals, value, multiplier):
    global fuelConsumedSinceRestartLiters
    if value < signal['lastValue']:
        value = signal['maxValue'] - signal['lastValue'] + value
    else:
        value = value - signal['lastValue']

    fuelConsumedSinceRestartLiters += multiplier * value
    return fuelConsumedSinceRestartLiters

def handleFuelFlowGallons(signal, signals, value):
    return handleFuelFlow(signal, signals, value, LITERS_PER_GALLON)

def handleFuelFlowMicroliters(signal, signals, value):
    return handleFuelFlow(signal, signals, value, LITERS_PER_UL)

def handleRollingOdometer(signal, signals, value, multiplier):
    global rollingOdometerSinceRestart
    if value < signal['lastValue']:
        rollingOdometerSinceRestart += (signal['maxValue'] -
                signal['lastValue'] + value)
    else:
        rollingOdometerSinceRestart += value - signal['lastValue']

    return (firstReceivedOdometerValue(signals) +
            (multiplier * rollingOdometerSinceRestart))

def handleRollingOdometerKilometers(signal, signals, value):
    return handleRollingOdometer(signal, signals, value, 1)

def handleRollingOdometerMiles(signal, signals, value):
    return handleRollingOdometer(signal, signals, value, KM_PER_MILE)

def handleRollingOdometerMeters(signal, signals, value):
    return handleRollingOdometer(signal, signals, value, KM_PER_M)

def firstReceivedOdometerValue(signals):
    global totalOdometerAtRestart
    if totalOdometerAtRestart == 0:
        odometerSignal = lookupSignal("total_odometer", signals)
        if odometerSignal is not None and odometerSignal['received']:
            totalOdometerAtRestart = odometerSignal['lastValue']
    return totalOdometerAtRestart

def handleStrictBoolean(signal, signals, value):
    return value != 0
