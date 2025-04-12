import os
from datetime import datetime
import types


def logger(old_function):
    def new_function(*args, **kwargs):
        result = old_function(*args, **kwargs)
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        name = old_function.__name__
        args_list = ', '.join(repr(arg) for arg in args)
        kwargs_list = ', '.join(f'{key}={value}' for key, value in kwargs.items())
        str_result = str(result)
        record = f'{date:<20} | {name:<20} | {str_result:<60} | {args_list:<120} | {kwargs_list}\n'
        with open('main_2.log', 'a') as f:
            f.write(record)
        return result
    return new_function


class FlatIterator:

    def __init__(self, original_list):
        self.flat_list = self.get_elements_list(original_list)

    def __iter__(self):
        self.cursor = -1
        return self

    def __next__(self):
        self.cursor += 1
        if self.cursor >= len(self.flat_list):
            raise StopIteration
        else:
            return self.flat_list[self.cursor]
    
    @logger
    def get_elements_list(self, list_: list):
        result = []
        for item in list_:
            if isinstance(item, list):
                result.extend(self.get_elements_list(item))
            else:
                result.append(item)  
        return result

@logger    
def flat_generator(original_list):
    for item in original_list:
        if isinstance(item, list):
            yield from flat_generator(item)
        else:
            yield item  

@logger
def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

@logger
def test_2():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)

@logger
def test_3():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

@logger
def test_4():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']

    assert isinstance(flat_generator(list_of_lists_2), types.GeneratorType)


if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    test_4()