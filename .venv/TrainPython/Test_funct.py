import unittest
import PyExampleTest
import PyExampleTestClass

class NameTestCase(unittest.TestCase):

    def test_first_last_name(self):
        full = PyExampleTest.full_name('carl', 'johnson')
        full2 = PyExampleTest.full_name('caRL', 'jOHNSON')
        self.assertEqual(full, 'Carl Johnson')
        self.assertEqual(full2, 'Carl Johnson')


class SquaresTestCase(unittest.TestCase):

    def test_square(self):
        t_1 = PyExampleTest.squares(4)
        self.assertEqual(t_1, [0, 1, 4, 9])
        self.assertNotEqual(t_1, [0, 1, 4, 8])

class NumberReturnTrueFalse(unittest.TestCase):

    def test_function(self):
        t_1 = PyExampleTest.is_even(2)
        self.assertEqual(t_1, True)

class CarTestCase(unittest.TestCase):

    # Создаем базовое условие setUp - название метода.!!!
    def setUp(self):
        self.car_1 = PyExampleTestClass.Car('Ford', 'Mondeo', 2019, 'black')

    def test_repaint(self):
        # Проверяем начальный цвет black
        self.assertEqual(self.car_1.color, 'black')
        self.car_1.repaint('red')
        self.assertEqual(self.car_1.color, 'red')
        self.car_1.drive(1000)
        self.assertEqual(self.car_1.total_drive_km, 1000)

class TruckTestCase(unittest.TestCase):

    def setUp(self):
        self.truck = PyExampleTestClass.Truck('Ford', 'Mondeo', 2019,
                                              'black', 3)

    def test_quant_trucks(self):
        self.assertEqual(self.truck.tralers, 3)
        self.truck.attach_traler(6)
        self.assertEqual(self.truck.tralers, 9)
        self.truck.repaint('red')
        self.assertEqual(self.truck.color, 'red')





unittest.main()
