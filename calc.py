__author__ = "Никольский В.А. | ЗЦИС-27"


class IPCalc:
    """IP-калькулятор"""

    def __init__(self, ip):
        self.full_address = ip
        self.ip = self.full_address.split('/')[0]
        self.check_ip()
        self.ip_binary = ((self.__get_oct(1) << 24) | (self.__get_oct(2) << 16)
                          | (self.__get_oct(3) << 8) | self.__get_oct(4))

        self.mask = int(self.full_address.split('/')[1])
        self.check_mask()
        self.subnet_mask = (0xFFFFFFFF << (32 - self.mask)) & 0xFFFFFFFF

    def __str__(self):
        return "IP-Калькулятор"

    @property
    def hosts(self):
        """Количество хостов"""
        if self.mask == 32 or self.mask == 31:
            return 0

        host_bits = 32 - self.mask
        return (2 ** host_bits) - 2

    @property
    def web_address(self):
        """Адрес сети"""
        # Вычисляем адрес сети (побитовое AND между IP и маской)
        network_address_binary = self.ip_binary & self.subnet_mask

        # Преобразуем адрес сети обратно в октеты
        network_octets = self.__calc_octets(network_address_binary)

        return self.format_dotted(network_octets)

    @property
    def broadcast(self):
        """Широковещательный адрес"""
        # Инвертируем маску, чтобы получить "wildcard mask" (например, для /24 это 0x000000FF)
        wildcard_mask = ~self.subnet_mask & 0xFFFFFFFF

        # Вычисляем широковещательный адрес (IP OR wildcard_mask)
        broadcast_binary = self.ip_binary | wildcard_mask

        # Преобразуем обратно в октеты
        broadcast_octets = self.__calc_octets(broadcast_binary)

        return self.format_dotted(broadcast_octets)

    @property
    def normal_mask(self):
        """Маска в виде a.b.c.d"""
        # Преобразуем числовую маску в вид 255.255.255.0
        mask_octets = self.__calc_octets(self.subnet_mask)

        return self.format_dotted(mask_octets)

    def __get_oct(self, oct_num: int):
        """
        Получить октет из IP
        :param oct_num: номер октета
        :return: int(октет)
        """
        if oct_num not in range(1, 5):
            raise Exception('Выберите октет от 1 до 4')

        return int(self.ip.split('.')[oct_num-1])

    def check_ip(self):
        """Валидация ip"""
        if len(self.ip.split('.')) != 4:
            raise Exception('IP должен содержать 4 октета')

        for i in range(1, 5):
            if 0 > self.__get_oct(i) or self.__get_oct(i) > 255:
                raise Exception(f'Октет {i} должен быть в пределах 0 < n < 255')

    def check_mask(self):
        """Валидация маски"""
        if not 0 <= self.mask <= 32:
            raise ValueError("Длина маски подсети должна быть в диапазоне 0-32")

    @staticmethod
    def __calc_octets(param):
        """
        Перевести из шестнадцатеричной системы в десятичную
        :param param: число для перевода
        :return: число в десятичном виде
        """
        res = [
            (param >> 24) & 0xFF,
            (param >> 16) & 0xFF,
            (param >> 8) & 0xFF,
            param & 0xFF
        ]
        return res

    @staticmethod
    def format_dotted(address):
        """
        Форматировать в октетный вид
        :param address: адрес
        :return: адрес в формате a.b.c.d
        """
        return '.'.join(map(str, address))
