__author__ = "Никольский В.А. | ЗЦИС-27"


import calc


while True:

    exit_cmd = ['exit', 'выход', 'stop', 'стоп', '0']

    command = input('\nВведите ip в формате a.b.c.d/e или команду для завершения\n')
    if command.strip().lower() in exit_cmd:
        break

    try:
        address = calc.IPCalc(command)
        print(f'Хосты: {address.hosts}')
        print(f'Адрес сети: {address.web_address}')
        print(f'Широковещательный адрес: {address.broadcast}')
        print(f'Маска в нормальном виде: {address.normal_mask}')
    except Exception as e:
        print(*e.args)

