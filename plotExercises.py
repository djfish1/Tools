#!/usr/bin/env python3
import datetime
import math
import matplotlib as mat
import matplotlib.pyplot as plt
import numpy
import os
import time

if __name__ == '__main__':
    f = plt.figure()
    SEC_PER_DAY = 24 * 3600
    now = datetime.datetime.fromtimestamp(time.time())
    nowDateTime = datetime.datetime(now.year, now.month, now.day)
    #minMinTime = now
    allExData = {}
    for fName in os.listdir('ExerciseLogs'):
        if fName.endswith('.log'):
            ex, _ = os.path.splitext(fName)
            data = numpy.matrix(numpy.loadtxt(os.path.join('ExerciseLogs', fName)))
            time = data[:, 0]
            numReps = data[:, 1]
            repCountByDay = {}
            for t, nr in zip(time, numReps):
                dt = datetime.datetime.fromtimestamp(float(t))
                dtRound = datetime.datetime(dt.year, dt.month, dt.day)
                deltaT = nowDateTime - dtRound
                days = -deltaT.days
                #print(days)
                repCountByDay[days] = repCountByDay.get(days, 0) + int(nr)
                
            allExData[ex] = repCountByDay
    iOff = 0
    delta = 0.5 / len(allExData)
    for ex, exData in allExData.items():
        plt.bar(numpy.array(list(exData.keys())) + iOff * delta, numpy.array(list(exData.values())), width=delta, label=ex)
        iOff += 1

    plt.xlabel('Days relative to now')
    plt.ylabel('Num reps')
    plt.legend()
    plt.show()

