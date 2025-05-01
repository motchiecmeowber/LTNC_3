from StaticError import *
from Symbol import *
from functools import *

def check_identifier_name(name):
    return bool (name and name[0].islower() and all (c.isalnum() or c == '_' for c in name))

def check_type(type):
    return type in ["number", "string"]

def check_value(value):
    return value.isdigit()

def check_string(value):
    return bool (len(value) >= 2 and value[0] == "'" and value[-1] == "'" and all (c.isalnum() for c in value[1:-1]))

def check_redeclared(symbol, name, level):
    return bool (any (s[0] == name and s[2] == level for s in symbol))

def check_undeclared(symbol, name, level):
    match = [s for s in reversed(symbol) if s[0] == name and s[2] <= level]
    return match[0] if match else None

def insert(symbol, name, type, level):
    instruction = f"INSERT {name} {type}"

    if check_identifier_name(name) and check_type(type):
        if check_redeclared(symbol, name, level):
            raise Redeclared(instruction)
        return symbol + [[name, type, level]], level, "success"
    raise InvalidInstruction(instruction)

def assign(symbol, name, value, level):
    instruction = f"ASSIGN {name} {value}"

    if check_identifier_name(name) and (check_value(value) or check_string(value)):
        filtered = check_undeclared(symbol, name, level)
        if filtered:
            symbol_type = filtered[1]
            
            if check_value(value) and symbol_type != "number":
                raise TypeMismatch(instruction)
            elif check_string(value) and symbol_type != "string":
                raise TypeMismatch(instruction)
            else:
                value_symbol = check_undeclared(symbol, value, level)
                if value_symbol and value_symbol[1] != symbol_type:
                    raise TypeMismatch(instruction)
                
            return symbol, level, "success"
        raise Undeclared(instruction)
    raise InvalidInstruction(instruction)

def begin(symbol, level):
    return symbol, level + 1, None

def end(symbol, level):
    if level == 0:
        raise UnknownBlock()
    return [s for s in symbol if s[2] < level], level - 1, None

def lookup(symbol, name, level):
    instruction = f"LOOKUP {name}"

    if check_identifier_name(name):
        s = check_undeclared(symbol, name, level)
        if s:
            return symbol, level, str(s[2])
    raise Undeclared(instruction)

def print(symbol, level):
    active_symbols = [(s[0], s[2]) for s in symbol if s[2] <= level]
    if not active_symbols:
        return symbol, level, ""
    unique_symbols = reduce(lambda acc, pair: ([f"{pair[0]}//{pair[1]}"] + acc[0], acc[1] | {pair[0]}) if pair[0] not in acc[1] else acc,
                  reversed(active_symbols), ([], set()))[0]
    '''
    acc: tuple (name//level, seen)
    pair: tuple (name, level)

    if pair[0] not in acc[1] -> add to acc[0] and update acc[1]
    else pass

    | : union

    reduce()[0]: return list
    '''
    return symbol, level, " ".join(unique_symbols) 

def rprint(symbol, level):
    active_symbols = [(s[0], s[2]) for s in symbol if s[2] <= level]
    if not active_symbols:
        return symbol, level, ""
    unique_symbols = reduce(lambda acc, pair: (acc[0] + [f"{pair[0]}//{pair[1]}"], acc[1] | {pair[0]}) if pair[0] not in acc[1] else acc,
                  reversed(active_symbols), ([], set()))[0]
    return symbol, level, " ".join(unique_symbols)

def process_command(commands, symbol, level):
    cmds = commands.split(" ")
    if not cmds:
        raise InvalidInstruction(cmds)
    
    cmd = cmds[0]
    if cmd == "INSERT" and len(cmds) == 3:
        return insert(symbol, cmds[1], cmds[2], level)
    elif cmd == "ASSIGN" and len(cmds) == 3:
        return assign(symbol, cmds[1], cmds[2], level)
    elif cmd == "BEGIN" and len(cmds) == 1:
        return begin(symbol, level)
    elif cmd == "END" and len(cmds) == 1:
        return end(symbol, level)
    elif cmd == "LOOKUP" and len(cmds) == 2:
        return lookup(symbol, cmds[1], level)
    elif cmd == "PRINT" and len(cmds) == 1:
        return print(symbol, level)
    elif cmd == "RPRINT" and len(cmds) == 1:
        return rprint(symbol, level)
    else:
        raise InvalidInstruction(commands)

def simulate(list_of_commands):
    def process(commands, symbol, level, result):
        if not commands:
            if level > 0:
                raise UnclosedBlock(f"{level}")
            return result
        
        try:
            new_symbol, new_level, new_result = process_command(commands[0], symbol, level)
            return process(commands[1:], new_symbol, new_level, result + [new_result])
    
        except Exception as e:
            return [str(e)]
    
    try:
        return process(list_of_commands, [], 0, [])        
    except Exception as e:
        return [str(e)]

    """
    Executes a list of commands and processes them sequentially.

    Args:
        list_of_commands (list[str]): A list of commands to be executed.

    Returns:
        list[str]: A list of return messages corresponding to each command.
    """
