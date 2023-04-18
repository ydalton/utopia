def identify(_inputLine):
    _commands = {
        "moveY":(".up()",".down()"),
        "moveX":(".right()",".left()"),
        "interact":(".interact(player.y, player.x, coins)")
    }

    _object = ""
    _do = ""
    _repeat = ""
    _error = False
    
    #identifying objects that the command applies to
    for letter in _inputLine:
        if letter == ".":
            break
        _object += letter

    #object error check
    if _object not in ["player", "cupboard"]:
        _error = True

    try:
        _inputCommand = _inputLine[len(_object)+1:_inputLine.index("(")]    #+1 because we do not want the .
        _repeat = _inputLine[_inputLine.index("(")+1:_inputLine.index(")")]     #+1 because we do not want the (

        if _inputCommand in _commands.keys():
            #movement +/-
            if (_inputCommand in ("moveY","moveX")):
                if _repeat == "":
                    _error = True   #movement orientation error
                elif int(_repeat) < 0:
                    _do = _commands[_inputCommand][1]
                elif int(_repeat) > 0:
                    _do = _commands[_inputCommand][0]
            
            else:
                _do = _commands[_inputCommand]
                _repeat = "1"
        #command error check
        else:
            _error = True
    except:
        _error = True

    if _do == ".interact(player.y, player.x)" and _object not in ["cupboard"]:
        _error = True

    return (_object, _do, _repeat, _error)
