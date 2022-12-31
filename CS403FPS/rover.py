import multiprocessing
import pathlib
import time
import traceback
import random
import parser1 as parser


class RunTimeError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f'[RUNTIME ERROR]: {self.msg}'

# The maximum amount of time that the rover can run in seconds
MAX_RUNTIME = 36000

#variables needed for certain features
cache = []
minerals = ["Iron", "Gold", "Diamond", "Nickel"]

# Rovers that exist
ROVER_1 = "Rover1"
ROVER_2 = "Rover2"

# Array of rovers
ROVERS = [
    ROVER_1,
    ROVER_2,
]

# Command file is stored within the rover directory. Here we're building one file
# for each of the rovers defined above
ROVER_COMMAND_FILES = {
    rover_name: pathlib.Path(pathlib.Path(__file__).parent.resolve(), f"{rover_name}.txt")
    for rover_name in ROVERS
}
for _, file in ROVER_COMMAND_FILES.items():
    with file.open("w") as f:
        pass

# Constant used to store the rover command for parsing
ROVER_COMMAND = {
    rover_name: None
    for rover_name in ROVERS
}

def get_command(rover_name):
    """Checks, and gets a command from a rovers command file.

    It returns True when something was found, and False
    when nothing was found. It also truncates the contents
    of the file if it found something so that it doesn't
    run the same command again (unless it was re-run from
    the controller/main program).
    """
    fcontent = None
    with ROVER_COMMAND_FILES[rover_name].open() as f:
        fcontent = f.read()
    if fcontent is not None and fcontent:
        ROVER_COMMAND[rover_name] = fcontent
        with ROVER_COMMAND_FILES[rover_name].open("w+") as f:
            pass
        return True
    return False

# Main Rover Class
class Rover():
    def __init__(self, name):
        self.name = name
        self.mapfile = 'map.txt'  # used to change map and then reload it
        self.direction = 0
        self.pos_x = 0
        self.pos_y = 0
        self.map = []
        self.front = ''
        self.inventory = []
        self.waypoint = False
        self.initialize()

    def print(self, msg):
        print(f"{self.name}: {msg}")

    def parse_and_execute_cmd(self, command):
        self.print(f"Running command: \n{command}")
        tree = parser.get_parse_tree(command)

        for i in tree.children:
            i.check_semantics()

        for i in tree.children:
            try:
                i.run(self)
            except TypeError as te:
                raise RunTimeError(te.args)

    def wait_for_command(self):
        start = time.time()
        while (time.time() - start) < MAX_RUNTIME:
            # Sleep 5 seconds before trying to check for
            # content again
            self.print("Waiting for command...")
            time.sleep(5)
            if get_command(self.name):
                self.print("Found a command...")
                try:
                    self.parse_and_execute_cmd(ROVER_COMMAND[self.name])
                except Exception as e:
                    self.print(f"Failed to run command: {ROVER_COMMAND[self.name]}")
                    self.print(traceback.format_exc())
                finally:
                    self.print("Finished running command.\n\n")

# Takes the map file, puts it into a 2D array and initializes the rover on a random tile with a random direction
    def initialize(self):
        self.map = []
        with open(self.mapfile, 'r') as m:
            for row in m.readlines():
                row.split('\n')
                newRow = []
                for c in row:
                    if c != '\n':
                        newRow.append(c)
                    elif c == '\n':
                        self.map.append(newRow)
            self.map.append(newRow)  #appends final row
# Place rover on map
        spawnable = 0
        self.direction = random.randint(0,3)
        xcoords =[]
        ycoords =[]
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == ' ':
                    spawnable += 1
                    xcoords.append(x)
                    ycoords.append(y)
        spawn_tile = random.randint(0,spawnable-1)
        self.map[xcoords[spawn_tile]][ycoords[spawn_tile]] = self.roverchar()
        self.pos_x = xcoords[spawn_tile]
        self.pos_y = ycoords[spawn_tile]
        self.print_map()

# Shows current state of map
    def print_map(self):
        print("printing map")
        for row in self.map:
            print(*row,sep="")

# changes the map and initializes rover on new map
    def switch_map(self,mnum):
        if mnum == 1:
            self.mapfile = 'map.txt'
        elif mnum == 2:
            self.mapfile = 'map2.txt'
        elif mnum == 3:
            self.mapfile = 'map3.txt'
        elif mnum == 4:
            self.mapfile = 'map4.txt'
        self.initialize()

# Helper function that changes the character of the rover to indicate direction
    def roverchar(self):
        icon = ''
        if self.direction == 0:
            icon = '^'
        elif self.direction == 1:
            icon = '>'
        elif self.direction == 2:
            icon = 'v'
        elif self.direction == 3:
            icon = '<'
        return icon

# Prints the results of all the queries
    def info(self):
        self.print_pos()
        self.looking()
        self.print(f"Looking at: {self.front}")
        self.facing()

# shows the rover's position
    def print_pos(self):
        position = [self.pos_x, self.pos_y]
        self.print(f"Position: {position}")

# Shows what the rover is looking at
    def looking(self):
        looking_at = []
        if self.direction == 0:
            self.front = self.map[self.pos_x - 1][self.pos_y]
            looking_at.append(self.pos_x - 1)
            looking_at.append(self.pos_y)
        elif self.direction == 1:
            self.front = self.map[self.pos_x][self.pos_y + 1]
            looking_at.append(self.pos_x)
            looking_at.append(self.pos_y + 1)
        elif self.direction == 2:
            self.front = self.map[self.pos_x + 1][self.pos_y]
            looking_at.append(self.pos_x + 1)
            looking_at.append(self.pos_y)
        elif self.direction == 3:
            self.front = self.map[self.pos_x][self.pos_y - 1]
            looking_at.append(self.pos_x)
            looking_at.append(self.pos_y - 1)
        return looking_at

# Prints the direction that the rover is facing
    def facing(self):
        print("Rover is facing: ")
        if self.direction == 0:
            print("Direction - North (0)")
        elif self.direction == 1:
            print("Direction - East (1)")
        elif self.direction == 2:
            print("Direction - South (2)")
        elif self.direction == 3:
            print("Direction - West (3)")

# Self-explanatory, rotates the rover and calls roverchar to change how it looks on the map
    def turnLeft(self):
        if self.direction == 0:  #North
            self.direction = 3
            self.map[self.pos_x][self.pos_y] = self.roverchar()
        else:
            self.direction -= 1
            self.map[self.pos_x][self.pos_y] = self.roverchar()

# Self-explanatory, rotates the rover and calls roverchar to change how it looks on the map
    def turnRight(self):
        if self.direction == 3: #West
            self.direction = 0
            self.map[self.pos_x][self.pos_y] = self.roverchar()
        else:
            self.direction += 1
            self.map[self.pos_x][self.pos_y] = self.roverchar()

# Moves the rover to a new space, has some helper code for the Waypoint function
    def move_tile(self):
        self.looking()
        if self.front == ' ':
            if self.direction == 0:
                self.pos_x -= 1
                self.map[self.pos_x][self.pos_y] = self.roverchar()
                if self.waypoint == True:
                    self.map[self.pos_x+1][self.pos_y] = 'W'
                    self.waypoint = False
                else:
                    self.map[self.pos_x+1][self.pos_y] = ' '

            elif self.direction == 1:
                self.pos_y += 1
                self.map[self.pos_x][self.pos_y] = self.roverchar()
                if self.waypoint == True:
                    self.map[self.pos_x][self.pos_y-1] = 'W'
                    self.waypoint = False
                else:
                    self.map[self.pos_x][self.pos_y-1] = ' '

            elif self.direction == 2:
                self.pos_x += 1
                self.map[self.pos_x][self.pos_y] = self.roverchar()
                if self.waypoint == True:
                    self.map[self.pos_x-1][self.pos_y] = 'W'
                    self.waypoint = False
                else:
                    self.map[self.pos_x-1][self.pos_y] = ' '

            elif self.direction == 3:
                self.pos_y -= 1
                self.map[self.pos_x][self.pos_y] = self.roverchar()
                if self.waypoint == True:
                    self.map[self.pos_x][self.pos_y+1] = 'W'
                    self.waypoint = False
                else:
                    self.map[self.pos_x][self.pos_y+1] = ' '
        else:
            self.print("Cannot move here, occupied tile")

# Drilling function, turns a depleted D space into an X
    def drill(self):
        space = self.looking()
        if self.front != 'D':
            self.print("Cannot Drill - Not a mining node (D space)")
        elif self.front == 'D':
            mineral = random.randint(0,3)
            self.inventory.append(minerals[mineral])
            self.map[space[0]][space[1]] = 'X'

# Shows what the rover has in its inventory
    def print_inv(self):
        print("INVENTORY:")
        iron_count,gold_count,dia_count,nick_count = 0,0,0,0
        for i in self.inventory:
            if i == 'Iron':
                iron_count += 1
            if i == 'Gold':
                gold_count += 1
            if i == 'Diamond':
                dia_count += 1
            if i == 'Nickel':
                nick_count += 1
        print(f"IRON x {iron_count}")
        print(f"GOLD x {gold_count}")
        print(f"DIAMOND x {dia_count}")
        print(f"NICKEL x {nick_count}")

# Lets the user know how many D spaces are remaining and their coordinates
    def envScan(self):
        total_nodes = 0
        locations = []
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 'D':
                    total_nodes += 1
                    locations.append([x,y])
        str(total_nodes)
        self.print(f"The total number of remaining nodes = {total_nodes}")
        if total_nodes != 0:
            self.print("They can be found at the following coordinates:")
        for i in locations:
            print(i)

# Destroys a wall right in front of the rover, can also be used to remove caches and waypoints
# Used also to prevent rover from getting stuck,
    def bomb(self):
        target = self.looking()
        if self.front == 'X' or self.front == 'C' or self.front == 'W': #destroy caches and waypoints
            self.print("BOOM! Target destroyed!")
            self.map[target[0]][target[1]] = ' '
        elif self.front == 'D' or self.front == ' ':
            self.print("Cannot detonate")

# Places a W after a movement to indicate a waypoint
    def waypoint_set(self):
        self.waypoint = True
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 'W':
                    self.waypoint = False
        self.print("After my next movement, the space immediately behind me will become a waypoint")

# Automatically jump to a waypoint previously set
    def moveto_waypoint(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y] == 'W':
                    self.map[self.pos_x][self.pos_y] = ' '
                    self.pos_x = x
                    self.pos_y = y
                    self.map[x][y] = self.roverchar()

# Places a C space into which your items can be dumped
    def cache_make(self):
        spot = self.looking()
        if self.front == ' ':
            self.map[spot[0]][spot[1]] = 'C'
        else:
            self.print("Invalid Tile, can only place cache on empty tiles")

# Dumps items into aforementioned cache
    def cache_dump(self):
        self.looking()
        if self.front == 'C':
            cache.append(self.inventory)
            self.inventory = []
        else:
            self.print("No cache to dump into")

# Prints 'S' to the left and right of the rover's position (Solar Panels)
    def charge(self):
        if self.map[self.pos_x][self.pos_y+1] != ' ' or self.map[self.pos_x][self.pos_y-1] != ' ':
            self.print("Not enough room to charge")
        elif self.map[self.pos_x][self.pos_y+1] == ' ' and self.map[self.pos_x][self.pos_y-1] == ' ':
            self.map[self.pos_x][self.pos_y+1] = 'S'
            self.map[self.pos_x][self.pos_y-1] = 'S'
            self.print("Solar Panels Deployed, Rover Charging")
            self.print_map()
            self.map[self.pos_x][self.pos_y+1] = ' '
            self.map[self.pos_x][self.pos_y-1] = ' '
            self.print("Charging Complete. Retracting Solar Panels")

def main():
    # Initialize the rovers
    rover1 = Rover(ROVER_1)
    rover2 = Rover(ROVER_2)
    my_rovers = [rover1,rover2]

    # Run the rovers in parallel
    procs = []
    for rover in my_rovers:
        p = multiprocessing.Process(target=rover.wait_for_command, args=())
        p.start()
        procs.append(p)

    # Wait for the rovers to stop running (after MAX_RUNTIME)
    for p in procs:
        p.join()


if __name__=="__main__":
    main()