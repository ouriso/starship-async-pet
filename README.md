# starship-async-pet
Pet project to studying async python

It allows you to fly in space while enjoying the twinkle of the stars.  
The script generates randomly sparkling stars, a Starship that can be controlled by player 
and Garbage objects that can destroy the player's Starship.  
The game year is displayed in the lower right window corner. 
As time goes by, there is more and more garbage. Dodging it becomes more difficult, 
but at some point the player gets an OldTroopersBlaster weapon to destroy garbage.

## Installation
Install requirements
```
poetry install
poetry update
```
_On Windows system you should additionally install 'curses' implementation_
```
pip install windows-curses
```

## Running
```
poetry run python main.py
```
## Config
Main configuration parameters are located in config.py file  
`BASE_DELAY, in seconds` - awaiting of different objects depends on this param  
`COLUMNS_SPEED, ROWS_SPEED` - the number of characters by which the Starship will be shifted.  
Each instance of the Starship class has arguments 'offset_step_x/y' that are multiplied by these values.  
`STARS_DENSITY` - a parameter that determines the number of stars to be drawn depending on the size of the window.  
_<window_square> / STARS_DENSITY = <stars_number>_
`GAME_YEAR_DURATION` - a parameter that defines game year duration (in seconds)
`ITS_A_GUN_TIME` - a parameter that defines game year when player gets an OldTroopersBlaster weapon

## Controls
`Left, Up, Right, Down arrows` - to moving Starship  
`Space` - to do a Blaster shots (the base blaster shoots in a random direction).