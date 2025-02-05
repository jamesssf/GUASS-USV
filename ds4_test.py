#import evdev
from evdev import InputDevice, categorize, ecodes

#cree un objet gamepad | creates object gamepad
gamepad = InputDevice('/dev/input/event2')

#affiche la liste des device connectes | prints out device info at start
print(gamepad)

#affiche les codes interceptes |  display codes
for event in gamepad.read_loop():
    print("WHY!?!?!?")
    #Boutons | buttons 
    if event.type == ecodes.EV_KEY:
        print(event.code)
    #Gamepad analogique | Analog gamepad
    elif event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        print(ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value)
