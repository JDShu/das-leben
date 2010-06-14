import pickle
import os.path

def main():
    print "Welcome to the psyche manager."
    state_list = load_file("state_list.l")
    loaded_in = load_file("default.in")
    loaded_ne = load_file("default.ne")
    command = raw_input("Command: ").split()
    temp_noesis = {}
    l = len(command)
    while True:
        l = len(command)
        if l == 0:
            pass
        elif command[0] == "quit":
            break
        elif command[0] == "help":
            print_help()
        elif command[0] == "load":
            if l < 3:
                print "load command incomplete"
            else:
                if command[1] == "in":
                    loaded_in = load_file(command[2])
                elif command[1] == "ne":
                    loaded_ne = load_file(command[2])
                else:
                    print "invalid file type"
        elif command[0] == "status":
            if l == 1:
                print "---IN TABLE---"
                print_dict(loaded_in)
                print "---NE TABLE---"
                print_dict(loaded_ne)
            else:
                if command[1] in loaded_ne:
                    category = "noesis"
                    print command[1], ": ",
                    for y in loaded_in[command[1]]:
                        print y,
                    print ""
                elif command[1] in loaded_in:
                    category = "interaction"
                else:
                    print command[1], "does not exist"
        
        elif command[0] == "save":
            save_dict(loaded_in, "default.in")
            save_dict(loaded_ne, "default.ne")
        elif command[0] == "new":
            if l == 2:
                if command[1] == "noesis":
                    add_noesis( state_list, loaded_ne )                    
                elif command[1] == "interaction":
                    add_interaction(loaded_ne, loaded_in)
                else:
                    print "can't add", command[1]
            else:
                print "not implemented"
        elif command[0] == "delete":
            if l==2:
                if command[1] == "noesis":
                    delete( "Noesis", loaded_ne )
                elif command[1] == "interaction":
                    delete("Interaction", loaded_in )
                else:
                    print "cannot delete", command[1]
            else:
                print "not implemented"        
        else:
            print "Invalid Command"
        command = raw_input("Command: ").split()
                
def load_file( filename ):
    if os.path.exists(filename):
        F = open(filename, "rb")
        try:
            print "Load succeeded: ", filename
            D = pickle.load(F)
            F.close()
            return D
        except:
            print "failed to load"
    else:
        print filename, " does not exist."

def save_dict( dict, filename):
    F = open(filename, "wb")
    pickle.dump(dict, F)
    print "saved", filename
    
def print_dict( loaded ):
    if loaded == None:
        print "nothing loaded"
    else:
        for x in loaded:
            print x, ": ",
            for y in loaded[x]:
                print y,
            print ""
        
def print_help():
    print "Available commands are: help, load, status"

def add_interaction( loaded_ne, loaded_in ):
    new_interaction = unique_input("Interaction", loaded_in)
    temp_list = []
    while True:
        noesis = raw_input( "Noesis to add to this interaction: " )
        if noesis == "finished":
            if len(temp_list) != 0:
                loaded_in[new_interaction] = temp_list
            else:
                print "Interaction not added"
            break
        elif noesis == "cancel":
            break
        elif noesis not in loaded_ne:
            print "Noesis doesn't exist"
        elif noesis in temp_list:
            print "Noesis already added"
        else:
            temp_list += [noesis]
            temp_list.sort()
            print temp_list
            

def unique_input( instance, existing ):
    while True:
        new_instance = raw_input(instance + " name: ")
        if new_instance not in existing:
            return new_instance
        else:
            print instance, "already exists"
        
def add_noesis( state_list, loaded_ne ):
    #while True:
    #    new_noesis = raw_input("Noesis name: ")
    #    if new_noesis not in loaded_ne:
    #        break
    #    else:
    #        print "Noesis already exists"
    new_noesis = unique_input("Noesis", loaded_ne)
    temp_list = []
    while True:
        state = raw_input("State to Modify: ")
        if state =="finished":
            if len(temp_list) == 0:
                print "Noesis not added"
            else:
                loaded_ne[new_noesis] = temp_list
                print_dict(loaded_ne)
            break

        elif state == "current":
            print temp_list
        elif state == "help":
            print state_list
        elif state not in state_list:
            print state, "not a modifiable emotion"        
        else:
            while True:
                entry = raw_input("Modify " + state + " by: " )
                if entry == "cancel":
                    break
                try:
                    value = int(entry)
                    if exists_already(temp_list, state):
                        for i,t in enumerate(temp_list):
                            if t[0] == state:
                                index = i
                                break
                        if value != 0:
                            temp_list[index] = (state, value)
                        else:
                            temp_list.pop(index)
                    elif value == 0:
                        break
                    else:
                        temp_list += [(state, value)]
                    temp_list.sort()
                    print temp_list
                    break
                except ValueError:
                    print "Must enter an integer. Try again."

def exists_already( L, value ):
    exists = False
    for t in L:
        if t[0] == value:
            exists = True
            break
    return exists

def delete(instance, loaded_ne ):
    while True:
        to_delete = raw_input(instance + " to delete: ")
        if to_delete == "cancel":
            break
        elif to_delete in loaded_ne:
            del loaded_ne[to_delete]
            print_dict(loaded_ne)
            break
        else:
            print to_delete, "is not an existing", instance

if __name__ == "__main__":
    main()
