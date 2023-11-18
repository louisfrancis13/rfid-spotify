#!/usr/bin/env python
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from time import sleep
from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()

DEVICE_ID=os.environ.get('DEVICE_ID')
CLIENT_ID=os.environ.get('CLIENT_ID')
CLIENT_SECRET=os.environ.get('CLIENT_SECRET')
REDIRECT_URI=os.environ.get('REDIRECT_URI')


while True:
    try:
        reader=SimpleMFRC522()
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                       client_secret=CLIENT_SECRET,
                                                       redirect_uri=REDIRECT_URI,
                                                       scope="user-read-playback-state,user-modify-playback-state"))
        
        # create an infinite while loop that will always be waiting for a new scan
        while True:
            print("Waiting for record scan...")
            id= reader.read()[0]
            print("Card Value is:",id)
            sp.transfer_playback(device_id=DEVICE_ID, force_play=True)
            
            # DONT include the quotation marks around the card's ID value, just paste the number
            if (id==993859695955):
                
                # playing a song
                sp.start_playback(device_id=DEVICE_ID, uris=['spotify:track:2T7Q6J4dcz2gwOPzqwogsT'])
                sleep(2)
                
            elif (id==652274267567):
                
                # playing an album
                sp.start_playback(device_id=DEVICE_ID, context_uri='spotify:playlist:0JGOiO34nwfUdDrD612dOp')
                sleep(2)
                
            # continue adding as many "elifs" for songs/albums that you want to play

    # if there is an error, skip it and try the code again (i.e. timeout issues, no active device error, etc)
    except Exception as e:
        print(e)
        pass

    finally:
        print("Cleaning  up...")
        GPIO.cleanup()
