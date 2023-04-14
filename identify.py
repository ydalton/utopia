def identify(_inputLine):
    _commands = {
        "moveY":("point.up()","point.down()"),
        "moveX":("point.right()","point.left()")
    }

    _object = ""
    _do = ""
    _error = False
    
    #identifying objects that the command applies to
    for letter in _inputLine:
        if letter == ".":
            break
        _object += letter

    #object error check
    if _object == "":
        _error = True

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
    #command error check
    else:
        _error = True

    

    return (_object, _do, _repeat, _error)
