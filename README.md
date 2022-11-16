# starship-async-pet
Pet project to studying async python

It allows you to fly in space while enjoying the twinkle of the stars.  
The script generates randomly sparkling stars and a Starship that can be controlled by player.

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

## Controls
`Left, Up, Right, Down arrows` - to moving Starship  
`Space` - to do a Blaster shots (the base blaster shoots in a random direction).