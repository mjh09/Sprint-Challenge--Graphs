from room import Room
from player import Player
from world import World
from utils import Graph, Queue, Stack
import random
from ast import literal_eval
def bfs(graph, current_room):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # create an empty queue and enqueue A-PATH-TO the starting vertex ID
        # create a Set to store the visited vertices
        # while the queue is not empty ..
            # dequeue the first PATH
            # grab the last vertex from the PATH
            # if that vertex has not been visited ..
                # check if its the target
                    #if yes, return path
                #mark it as visited
                # add A PATH TO its neighbots to the back of the queue
                    # copt the path
                    # append the neighbor to the back
        dirs = ["n","s","e","w"]
        # create an empty Queue 
        queue = Queue()
        #push the starting vertex ID as list
        queue.enqueue([current_room])
        # create an empty Set to store the visited vertices
        visited = set()
        
        # while the queue is not empty ...
        while queue.size() > 0:
            
            # dequeue the first vertex
            path = queue.dequeue()
            vert = path[-1]
            
            # if that vertex has not been visited ..
            if vert not in visited:
                #check for target
                if "?" in graph.vertices[vert].values():
                    path_dirs = []
                    cur_idx = 0
                    next_idx = 1
                    last_room = path[-1]
                    print(path)    
                    for room in path:
                        if room == last_room:
                            break
                        cur_room = path[cur_idx]
                        next_room = path[next_idx]
                        room_dirs = list(graph.vertices[cur_room].keys())
                        
                        for d in room_dirs:
                            
                            if graph.vertices[cur_room][d] == next_room:
                                    path_dirs.append(d)
                                    cur_idx += 1
                                    next_idx += 1
                                    break
                         
                    return path_dirs
                # mark it is visited
                visited.add(vert)
                # then add all of its neighbors to the back of the queue
                for neighbor in graph.vertices[vert].values(): #self.get_neighbors(vert)
                    if neighbor not in path:
                    #copy path to avoid pass by reference
                        new_path = list(path) # make a copy
                        new_path.append(neighbor)
                        queue.enqueue(new_path)
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
#map_file = "maps/test_cross.txt"
#map_file = "maps/test_loop.txt"
#map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


prev_room = player.current_room.id
current_room = player.current_room.id
room_dirs = world.rooms[current_room].get_exits()
graph = Graph()
graph.add_vertex(player.current_room.id, room_dirs)

visited = set()
visited.add(current_room)

# dirs = ["n","s","e","w"]
# prev_dir = None

# ustack = Stack()
# ustack.push(current_room)

while len(visited) < len(world.rooms):
    # if len(traversal_path)> 2000:
    #      print('nope')
    #      break
    while "?" in graph.vertices[current_room].values():
        
        # dictionary of connected rooms
        neighbs = graph.vertices[current_room]
        print('current_room', current_room)
        print('neighbs', neighbs)
        
        # connected directions
        room_dirs = world.rooms[current_room].get_exits()
        print('rooms_dirs', room_dirs)
        
        # shuffle
        random.shuffle(room_dirs)
   
        for move in room_dirs:
            if neighbs[move] == "?":
                prev_room = player.current_room.id
                print('main prev room', prev_room)
                player.travel(move)
                print(move)
                traversal_path.append(move)
                print('travel_path_main', traversal_path)
                
                current_room = player.current_room.id
                print('current_room_main', current_room)
                room_dirs = world.rooms[current_room].get_exits()
                print('current room exits', room_dirs)
                if current_room not in visited:
                    visited.add(current_room)
                    print('visited',visited)
                    graph.add_vertex(player.current_room.id, room_dirs)
                    print('vertices', graph.vertices)
                
                # set previous rooms connected direction to room moved to
                graph.vertices[prev_room][move] = player.current_room.id
                
                print('prev_room', graph.vertices[prev_room])
                print('cur_room', graph.vertices[current_room])
                
                if move == 'n':
                    graph.vertices[current_room]['s'] = prev_room
                if move == 's':
                    graph.vertices[current_room]['n'] = prev_room
                if move == 'e':
                    graph.vertices[current_room]['w'] = prev_room
                if move == 'w':
                    graph.vertices[current_room]['e'] = prev_room
                
                
                print('cur_room', graph.vertices[current_room])
                print('len_visited',len(visited))
                print('tp',traversal_path)

                prev_room = player.current_room.id
                current_room = player.current_room.id
                break
    
    if len(visited) == len(world.rooms):
        break
    # # if len(traversal_path)> 30:
    # #     break
    # temp = traversal_path.copy()
    # print('temp',temp)
    # stack = Stack()
    # for move in temp:
    #     stack.push(move)
  
    if "?" not in graph.vertices[current_room].values():
        new_dirs = bfs(graph, current_room)
        print('new_dirs',new_dirs)
        # if len(new_dirs) < 1:
        #     break
        
        
        for dirs in new_dirs:
            
            prev_room = player.current_room.id
            player.travel(dirs)
            traversal_path.append(dirs)
            
            current_room = player.current_room.id
            
            
            print('this traversal path',traversal_path)
            print('this prev room', prev_room)
            print('this curr room',current_room)
        

# def dft(self, starting_vertex):
#         """
#         Print each vertex in depth-first order
#         beginning from starting_vertex.
#         """
#         # create an empty stack and push the starting vertex ID
#         stack = Stack()
#         stack.push(starting_vertex)
#         # create an empty Set to store the visited vertices
#         visited = set()
#         # while the stack is not empty ...
#         while stack.size() > 0:
#             # pop the first vertex
#             vert = stack.pop()
#             # if that vertex has not been visited ..
#             if vert not in visited:
#                 # mark it is visited
#                 visited.add(vert)
#                 print(vert)
#                 # then add all of its neighbors to the top of the stack
#                 for neighbor in self.vertices[vert]: #self.get_neighbors(vert)
#                     stack.push(neighbor)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
