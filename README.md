# CS403FP
Final Project for CS 403

Instructions:

Run rover.py in one command prompt window and main in another
with a rover command file as an additional argument. (python rover.py)
and example: (python main.py parsing-tests\test.txt). Make sure
that the files are being run in the correct directory.
Rover will parse and run the command, the list of commands
is as follows:

- rover . move_tile # Moves the rover a single space
- rover . turnLeft # Rotates the rover 90 degrees left
- rover . turnRight # Rotates the rover 90 degrees right
- rover . info # Gives the rover's position, direction, tile
looked at by rover and a visual of the map.
- rover . print_pos # prints the coordinates of the rover
- rover . switch_map int # changes the map and initializes
the rover on the new map.
- rover . looking # returns the tile the rover is looking at
- rover . facing # returns the rover's direction
- rover . drill # puts a random mineral in inventory after
using the command on a D space, changes to X after use.
- rover . print_inv # shows the contents of the inventory
- rover . envScan # returns the amount and positions of all
remaining D spaces.
- rover . bomb # destroys space in front of rover, cannot
be used on D or empty spaces. Can be used to free the rover if
trapped.
- rover . waypoint_set # places a W space which can be travelled
to with:
- rover. moveto_waypoint # swaps rover and waypoint positions,
removes waypoint.
- rover . cache_make # places a C space into which items can be
placed.
- rover . cache_dump # places items into cache.
- rover . print_map # shows the current state of the map
- rover . charge # places an S to represent a solar panel
on either side of the rover briefly.

Other General Notes:

- switch_map takes an extra argument of an integer between
1 and 4 inclusive, with each value representing a map. Additional
maps cannot be added without altering switch_map in rover.py
- move_tile only moves a single tile, must be looped in command
files to move in a line. 
- movement only happens in a straight line in the direction
the rover is facing, use turnLeft and turnRight to change direction