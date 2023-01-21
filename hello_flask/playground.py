def decorate_function(function):
    def inner_functionality():
        str(function()) + str(function())
    return inner_functionality

@decorate_function
def print_something():
    print("Hello World!")

print_something()