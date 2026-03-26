#
# test_buzzer.py
#
#
from orbit import Buzzer
import uasyncio as asyncio
from time import sleep

async def wait(buzzer):
    print('starting wait')
    await asyncio.sleep(2)
    buzzer.stop_async()

async def play_song(buzzer):
    print('starting play_song')
    notes = [262, 0, 294, 330, 349, 392, 440, 494, 523]
    beats = [0.05 for note in notes]
    print(f'Playing a song using frequency notation: {notes}')
    await buzzer.play_async(notes, beats, repeat=Buzzer.FOREVER)
    print('ending play_song')


if __name__ == '__main__':
    buzzer = Buzzer(pin=22)
    
    try:
        print('Trying interrupted looped song')
        asyncio.run( asyncio.gather(wait(buzzer), play_song(buzzer)))
        sleep(1)
        
        print('Async buzzer')
        asyncio.run(buzzer._play_note_async(200, 0.5))
        sleep(1)
    
        notes = [262, 0, 294, 330, 349, 392, 440, 494, 523]
        beats = [0.15 for note in notes]
        print(f'Async playing a song using frequency notation: {notes}')
        asyncio.run(buzzer.play_async(notes, beats))
        sleep(1)
    
        # Single beep
        print('Single beep')
        buzzer.beep()
        sleep(1)
        
        # Single beep
        print('Multiple beep')
        buzzer.beep(repeat=2, freq=500)
        sleep(1)
        
        # Print beginning and ending sounds
        print('Begin and end sounds')
        buzzer.begin_sound()
        buzzer.end_sound()
        sleep(1)

        # Play a song using notes notation
        notes = ["C", "R", "D", "E", "F", "G", "X", "A", "B", "C" ]
        beats = [0.25 for note in notes]
        print(f'Playing a song using notes notation: {notes}')
        buzzer.play(notes, beats)
        sleep(1)
        
        # Play a song using frequency notation
        notes = [262, 0, 294, 330, 349, 392, 440, 494, 523]
        beats = [0.1 for note in notes]
        print(f'Playing a song using frequency notation: {notes}')
        buzzer.play(notes, beats, repeat=2)
    
    except KeyboardInterrupt:
        print('Program ended.')
