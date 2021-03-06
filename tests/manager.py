# encoding: utf-8
import unittest
from plugnplay import Manager, Interface, Plugin


class SomeInterface(Interface):
    pass


class PlugA:
    pass


class PlugB:
    pass


class ManagerTest(unittest.TestCase):

    def setUp(self):
        self.man = Manager()

    '''
        Tests that the managar can register one implementor
        of one interface
    '''
    def test_add_first_implementor_of_an_interface(self):
        self.man.add_implementor(SomeInterface, PlugA())
        self.assertEquals(1, len(self.man.implementors(SomeInterface)))
        self.assertTrue(isinstance(self.man.implementors(SomeInterface)[0], PlugA))

    def test_add_second_implementor_of_an_interface(self):
        self.man.add_implementor(SomeInterface, PlugA())
        self.man.add_implementor(SomeInterface, PlugB())
        self.assertEquals(2, len(self.man.implementors(SomeInterface)))

    '''
        The list of implementors of an Interface should be empty if it has no
        implementors yet.
    '''
    def test_return_empty_list_of_implementors(self):
        self.assertEquals(0, len(self.man.implementors(SomeInterface)))


class FilteredImplementorsTest(unittest.TestCase):

    def setUp(self):
        self.man = Manager()

    def test_simple_call_back_no_parameters(self):
        def _simple_callback_filter(implementor):
            return implementor.__class__.__name__.endswith("A")

        def _simple_callback_filter_all_implementors(implementor):
            return False

        implementor_a = PlugA()
        self.man.add_implementor(SomeInterface, implementor_a)
        self.man.add_implementor(SomeInterface, PlugB())
        assert 2 == len(self.man.implementors(SomeInterface))
        filtered_implementors = self.man.implementors(SomeInterface, _simple_callback_filter)
        assert 1 == len(filtered_implementors)
        assert [implementor_a] == filtered_implementors

        # Test the filter that filters-out all implementors
        assert 0 == len(self.man.implementors(SomeInterface, _simple_callback_filter_all_implementors))

    def test_filter_with_parameters(self):
        class MyInterface(Interface):
            pass

        class A(Plugin):
            implements = [MyInterface, ]

        class AB(Plugin):
            implements = [MyInterface, ]

        class AC(Plugin):
            implements = [MyInterface, ]

        def _filter_with_arguments(implementor, size=1):
            return len(implementor.__class__.__name__) == size

        assert 3 == len(MyInterface.implementors())
        assert 2 == len(MyInterface.implementors(filter_callback=_filter_with_arguments, size=2))
        assert 2 == len(MyInterface.implementors(_filter_with_arguments, 2))
        assert 1 == len(MyInterface.implementors(_filter_with_arguments))
