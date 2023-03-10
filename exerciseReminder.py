#!/usr/bin/env python3
import optparse
import os
import random
import sys
import time
import tkinter.messagebox as msg
import tkinter.simpledialog as simp

chest = ('pushups', 'wide-pushups')
arms = ('curls', 'tricep extensions', 'skull crushers', 'reverse curls', 'hammer curls')
shoulders = ('shoulder flies', 'military presses', 'front raises')
back = ('bent rows', 'lower back raises', 'pull backs', 'pull downs')
legs = ('lunges', 'squats', 'calf raises')
core = ('situps', 'side bends', 'leg raises')
stretching = ('hamstring stretch', 'back-stretch')

def pickExercise():
    # Since there are more exercises for certain categories, first
    # randomly pick the category, so that way you don't cheat and
    # only work out body parts with more options
    categories = (chest, arms, shoulders, legs, back, core, stretching)
    category = random.choice(categories)
    exercise = random.choice(category)
    #print(category, exercise)
    return exercise

def logExercise(ex, numReps, testMode=False):
    now = time.time()
    exNoSpace = ex.replace(' ', '_')
    logDir = 'ExerciseLogs' if not testMode else 'TestExLogs'
    fullLogDir = os.path.join(sys.path[0], logDir)
    if not os.path.isdir(fullLogDir):
        os.mkdir(fullLogDir)
    with open(os.path.join(fullLogDir, exNoSpace + '.log'), 'a') as f:
        f.write('{0:.3f} {1:d}\n'.format(now, numReps))
        f.flush()

def doMainLoop(delayMin, testMode):
    done = {}
    while True:
        resp = False
        doneText = ''
        for k, v in done.items():
            doneText = '\n'.join((doneText, '{0:s}: {1:d}'.format(k, v)))
        while resp is False:
            ex = pickExercise()
            resp = msg.askyesnocancel('Exercise time.',
                    message='\n'.join(('Do some ' + ex + '?',
                        'Yes = did it!',
                        'No = pick new exercise',
                        'Cancel = quit',
                        doneText)))
        if resp is None:
            if msg.askyesno('Quit?', message='Really quit?'):
                break
        elif resp:
            numReps = simp.askinteger('Repetitions', prompt='How many ' + ex + ' did you do?')
            if numReps is not None:
                done[ex] = done.get(ex, 0) + numReps
                logExercise(ex, numReps, testMode)
        if random.uniform(0, 1) < 0.33:
            msg.showwarning('Water break', message='Make sure you drink enough water.')
        time.sleep(delayMin * 60)

if __name__ == "__main__":
    op = optparse.OptionParser()
    op.add_option('-d', '--delay', type=float, dest='delay', help='Time (minutes) between reminders.', default=10)
    op.add_option('-t', '--test', action='store_true', dest='test', help='Set to test mode.', default=False)
    (opts, args) = op.parse_args()
    if opts.test:
        opts.delay = 0.1
    random.seed(None)
    doMainLoop(opts.delay, opts.test)

