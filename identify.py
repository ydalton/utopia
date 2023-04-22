def identify(_inputLine):
    #commands for players linked to the in-code commands
    _commands = {
        "moveY":(".up()",".down()"),
        "moveX":(".right()",".left()"),
        "interact":(".interact(player.y, player.x)")
    }

    #output variables
    _object = ""
    _do = ""
    _repeat = ""
    _error = False
    
    #identifying objects that the command applies to
    for letter in _inputLine:
        if letter == ".":
            break
        _object += letter

    #valid object error check
    if _object not in ["player", "cupboard"]:
        _error = True
        print("error 1")

    try:    #handles the error of command not having ()
        _inputCommand = _inputLine[len(_object)+1:_inputLine.index("(")]    #extracting inputerd command by getting string from the end of object till start of brackets
        _repeat = _inputLine[_inputLine.index("(")+1:_inputLine.index(")")]     #extracting the repetition of the command from inbetween the brackets
        
        #improper command error check
        if _inputCommand in _commands.keys():

            #movement +/- on the axis
            if (_inputCommand in ("moveY","moveX")):
                if _repeat == "":
                    _error = True   #movement orientation error
                    print("error 2")
                elif int(_repeat) < 0:
                    _do = _commands[_inputCommand][1]
                elif int(_repeat) > 0:
                    _do = _commands[_inputCommand][0]
            
            else:
                _do = _commands[_inputCommand]
                if _repeat == "": 
                    _repeat = "1"

        else:
            _error = True
            print("error 3")

    except:
        _error = True
        print("error 4")

    #checking if moveX/Y commands are used with correct objects
    if _do in ("moveY","moveX") and _object not in ["player"]:
        _error = True
        print("error 5")

    #checking if interact command is used with correct objects
    if _do == ".interact(player.y, player.x)" and _object not in ["cupboard"]:
        _error = True
        print("error 6")

    return (_object, _do, _repeat, _error)
