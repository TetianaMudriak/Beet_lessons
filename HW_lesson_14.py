from functools import wraps
import math


def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__name__, 'called with', *args, **kwargs)
        return func(*args, **kwargs)

    return wrapper


@logger
def add(a, b):
    return a + b


def stop_words(words: list):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_res = func(*args, **kwargs)
            for word in words:
                func_res = func_res.replace(word, '*')

            return func_res

        return wrapper

    return inner


@stop_words(['pepsi', 'BMW'])
def create_slogan(name: str):
    return f"{name} drinks pepsi in his brand new BMW!"


def arg_rules(type_: type, max_length: int, contains: list):
    def inner(func):
        @wraps(func)
        def wrapper(*args):
            for item in args:
                if not isinstance(item, type_):
                    print('Wrong type! Please enter string')
                    return False
                elif len(item) > max_length:
                    print('Too long! Please enter shorter than 15 symbols')
                    return False
                for symbol in contains:
                    if symbol not in item:
                        print(
                            f'Your name should contain some symbols '
                            f'from list: {contains}')
                        return False
                else:
                    print(func(*args))

        return wrapper

    return inner


@arg_rules(type_=str, max_length=15, contains=['05', '@'])
def create_slogan2(name: str):
    return f"{name} drinks pepsi in his brand new BMW!"


def super_box_print(border_symbol: str, box_width: int):
    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            func_result = func(*args, *kwargs)
            txt = func_result.split(" ")
            for word in txt:
                if len(word) > (box_width - 2):
                    print("Sorry, your string longer than box width!")
                    return

            print(border_symbol * box_width)

            for word in txt:
                half_space = math.ceil((box_width - len(word) - 2) / 2)
                if box_width % 2 == 0 and len(word) % 2 != 0:
                    space1 = ' ' * half_space
                    space2 = ' ' * (half_space - 1)
                elif box_width % 2 != 0 and len(word) % 2 == 0:
                    space1 = ' ' * half_space
                    space2 = ' ' * (half_space - 1)
                else:
                    space1 = ' ' * half_space
                    space2 = space1

                print("{0}{1}{2}{3}{4}".format(border_symbol, space1,
                                               word, space2, border_symbol))
            print(border_symbol * box_width)

            return func_result

        return wrapper

    return inner


@super_box_print('#', 20)
def enter_string(text: str):
    return text


def main():
    # Task 1
    add(4, 5)

    # Task 2
    print(create_slogan('Tania'))

    # Task 3
    create_slogan2('johndoe05@gmail.com')
    create_slogan2('S@SH05')
    create_slogan2(12)
    create_slogan2('SSH0')

    # Additional task
    enter_string('This is the long string in super box')


if __name__ == '__main__':
    main()
