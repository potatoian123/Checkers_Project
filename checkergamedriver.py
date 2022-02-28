from checkers_working import *
checklist = ['y','n']

start = input("Do you want to play checkers (Y/N): ")
while start.lower() not in checklist:
    start = input("Please indicate if you want to play")

if start.lower() == 'y':
    startGame()
else:
    print('Why are you running this program then?')
