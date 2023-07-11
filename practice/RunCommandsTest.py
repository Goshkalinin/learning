from dataclasses import dataclass


@dataclass
class Command:
    fn: callable
    params: []


def sum_fn(a, b):
    print(a + b)


def mult_fn(*args):
    result = 1
    for num in args:
        result *= num
    print(result)


def run_commands(commands, local_vars):
    for command in commands:
        function = command.fn
        params = command.params
        bound_params = []
        for param in params:
            bound_params.append(local_vars[param])
        function(*bound_params)


def commands():
    a = Command(sum_fn, ["x", "y"])
    b = Command(mult_fn, ["x", "y", "z"])

    return [a, b]

def main():
    x = 1
    y = 2
    z = 3
    cmds = commands()
    run_commands(cmds, locals())

main()
