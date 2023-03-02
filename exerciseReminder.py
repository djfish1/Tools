#!/usr/bin/env python3
import optparse
import random
import time
import tkinter.messagebox as msg
import tkinter.simpledialog as simp

def pickExercise():
    chest = ('pushups', 'wide-pushups')
    arms = ('curls', 'tricep extensions', 'reverse curls')
    shoulders = ('shoulder flies', 'lateral raises', 'front raises')
    legs = ('lunges', 'squats')
    back = ('bent rows', 'lower back raises')
    # Since there are more exercises for certain categories, first
    # randomly pick the category, so that way you don't cheat and
    # only work out body parts with more options
    categories = (chest, arms, shoulders, legs, back)
    category = random.choice(categories)
    exercise = random.choice(category)
    #print(category, exercise)
    return exercise

def doMainLoop(delayMin):
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
        time.sleep(delayMin * 60)

if __name__ == "__main__":
    op = optparse.OptionParser()
    op.add_option('-d', '--delay', type=float, dest='delay', help='Time (minutes) between reminders.', default=10)
    #op.add_option('-s', '--serverIp', type=str, dest='serverIp', help='Server IP', default=None)
    #op.add_option('-p', '--serverPort', type=int, dest='serverPort', help='Server Port', default=None)
    #op.add_option('-u', '--userName', type=str, dest='userName', help='User name (debug only)', default=None)
    (opts, args) = op.parse_args()
    doMainLoop(opts.delay)

