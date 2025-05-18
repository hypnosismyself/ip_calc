import unittest
from calc import IPCalc


class TestIPCalc(unittest.TestCase):
    """Тестовый комплект для проверки IP-калькулятора"""

    def test_valid_ip(self):
        """Проверка корректных IP-адресов"""
        ip = IPCalc("192.168.1.1/24")
        self.assertEqual(ip.ip, "192.168.1.1")
        self.assertEqual(ip.mask, 24)

        ip = IPCalc("10.0.0.1/16")
        self.assertEqual(ip.ip, "10.0.0.1")
        self.assertEqual(ip.mask, 16)

    def test_invalid_ip(self):
        """Проверка невалидных IP-адресов"""
        with self.assertRaises(Exception):
            IPCalc("192.168.1/24")  # Не хватает октета

        with self.assertRaises(Exception):
            IPCalc("192.168.1.256/24")  # Октет > 255

        with self.assertRaises(Exception):
            IPCalc("192.168.1.-1/24")  # Октет < 0

    def test_invalid_mask(self):
        """Проверка невалидных масок"""
        with self.assertRaises(ValueError):
            IPCalc("192.168.1.1/33")  # Маска > 32

        with self.assertRaises(ValueError):
            IPCalc("192.168.1.1/-1")  # Маска < 0

    def test_hosts(self):
        """Проверка количества хостов"""
        self.assertEqual(IPCalc("192.168.1.1/24").hosts, 254)
        self.assertEqual(IPCalc("192.168.1.1/16").hosts, 65534)
        self.assertEqual(IPCalc("192.168.1.1/31").hosts, 0)  # Специальный случай
        self.assertEqual(IPCalc("192.168.1.1/32").hosts, 0)  # Специальный случай

    def test_web_address(self):
        """Проверка адреса сети"""
        self.assertEqual(IPCalc("192.168.1.100/24").web_address, "192.168.1.0")
        self.assertEqual(IPCalc("10.0.0.1/8").web_address, "10.0.0.0")
        self.assertEqual(IPCalc("172.16.0.1/16").web_address, "172.16.0.0")
        self.assertEqual(IPCalc("192.168.1.1/32").web_address, "192.168.1.1")

    def test_broadcast(self):
        """Проверка широковещательного адреса"""
        self.assertEqual(IPCalc("192.168.1.100/24").broadcast, "192.168.1.255")
        self.assertEqual(IPCalc("10.0.0.1/8").broadcast, "10.255.255.255")
        self.assertEqual(IPCalc("172.16.0.1/16").broadcast, "172.16.255.255")
        self.assertEqual(IPCalc("192.168.1.1/32").broadcast, "192.168.1.1")

    def test_normal_mask(self):
        """Проверка маски в нормальном виде"""
        self.assertEqual(IPCalc("192.168.1.1/24").normal_mask, "255.255.255.0")
        self.assertEqual(IPCalc("192.168.1.1/16").normal_mask, "255.255.0.0")
        self.assertEqual(IPCalc("192.168.1.1/8").normal_mask, "255.0.0.0")
        self.assertEqual(IPCalc("192.168.1.1/32").normal_mask, "255.255.255.255")
