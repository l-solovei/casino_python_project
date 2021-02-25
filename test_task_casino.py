import random
casino_list = []
game_machine_list = []

class User:
    def __init__(self, name: str, money: float):
        self.name = name
        if money >= 0:
            self.money = float(money)
        else:
            self.money = 0.0
            print('Недопустима сума грошей')

    def play(self, money: float) -> float:
        if money > self.money or money <= 0:
            print(f'Недостатньо грошей. Поточний баланс: {self.money}')
        else:
            try:
                play_machine = random.choice(
                    [available_gm for available_gm in game_machine_list if available_gm.getMoney >= money * 3])
                self.money -= money
                win_money = play_machine.play(money)
                self.money += win_money
                print(f'Ви виграли: {win_money}.')
            except IndexError:
                print('Введіть меншу суму')
            finally:
                print(f'Поточний баланс: {self.money}')
                return self.money

    def __str__(self):
        return f'Відвідувач - {self.name} - доступний баланс {self.money}'


class SuperAdmin(User):
    def __init__(self, name, money=0):
        super().__init__(name, money)

    def createCasino(self):
        casino_name = input('Введіть назву казино: ')
        for casino in casino_list:
            if casino_name == casino.name:
                print('Казино з такою назвою вже існує')
            else:
                new_casino = Casino(casino_name)
                print(f'Казино - \'{new_casino.name}\' - успішно створено')
                return new_casino

    def createGameMachine(self, money: float):
        new_game_machine = GameMachine(money)
        return new_game_machine

    def getMoney(self, number: float):
        calculate_money = 0.0
        try:
            game_machine_list_sorted = sorted(game_machine_list, key=lambda game_machine: game_machine.getMoney, reverse=True)
            print(game_machine_list_sorted)
            for game_machine in game_machine_list_sorted:
                if calculate_money == number:
                    break
                else:
                    calculate_money_2 = number - calculate_money  # скільки залишилось забрати
                    calculate_money += game_machine.getMoney - game_machine.takeMoney(calculate_money_2)
            print(f'Вилучено: {calculate_money}')
            return calculate_money
        except TypeError:
            return 0.0

    def addMoneyToCasino(self, number: float):
        if len(game_machine_list):
            money_for_one_game_machine = number / len(game_machine_list)
            for game_machine in game_machine_list:
                game_machine.addMoney(money_for_one_game_machine)
        else:
            print('Ігрові автомати відсутні!')

    def addMoneyToGameMachine(self, id: int, number: float):
        if id in [game_machine.id for game_machine in game_machine_list]:
            for game_machine in game_machine_list:
                if id == game_machine.id:
                    game_machine.addMoney(number)
                    break
        else:
            print('Ігрового автомату з таким id не знайдено!')

    def deleteGameMachine(self, id: int):
        if len(game_machine_list) > 1:
            if id in [game_machine.id for game_machine in game_machine_list]:
                for game_machine in game_machine_list:
                    if id == game_machine.id:
                        all_money = game_machine.getMoney
                        game_machine_list.remove(game_machine)
                        del game_machine
                        money_for_one_game_machine = all_money / len(game_machine_list)
                        for game_machine in game_machine_list:
                            game_machine.addMoney(money_for_one_game_machine)
                        break
            else:
                print('Ігрового автомату з таким id не знайдено!')
        else:
            print('В казино має бути хоча б один ігровий автомат!')

    def __str__(self):
        return f'Адміністратор - {self.name} - доступний баланс {self.money}'


class Casino:
    def __init__(self, name: str):
        self.name = name
        casino_list.append(self)

    @property
    def getMoney(self) -> float:
        money = 0.0
        for game_machine in game_machine_list:
            money += game_machine.getMoney
        print(f'Загальна сума грошей в казино: {money}')
        return money

    @property
    def getMachineCount(self):
        print(f'Кількість ігрових автоматів в казино: {len(game_machine_list)}')
        return len(game_machine_list)

    def __str__(self):
        return f'{self.name}'

    def __repr__(self):
        return f'{self.name}'


class GameMachine:
    class_counter = 1
    def __init__(self, number: float):
        if number >= 0:
            self.__number = float(number)
            self.id = GameMachine.class_counter
            GameMachine.class_counter += 1
            game_machine_list.append(self)
            print(f'Ігровий автомат - успішно створено')
        else:
            self.__number = 0.0
            print('Недопустима сума грошей')

    @property
    def getMoney(self) -> float:
        return self.__number

    def takeMoney(self, number: float) -> float:
        if number <= 0:
            print('Недопустима сума грошей')
        elif self.getMoney - number < 0:
            print(f'Недостатньо грошей! Поточний баланс {self.getMoney}. Вилучаємо доступну суму.')
            self.__number -= self.getMoney
            return self.__number
        else:
            self.__number -= number
            return self.__number

#    можна зробити сеттер: @getMoney.setter
    # але тоді: def getMoney(self, number: float) -> float:
    def addMoney(self, number: float) -> float:
        if number >= 0:
            self.__number += number
            return self.__number
        else:
            print('Недопустима сума грошей')

    def play(self, number: float) -> float:
        self.addMoney(number)
        random_num = str(random.randint(100, 999))
        print(f'Випало: {random_num}')
        for num in random_num:
            if random_num.count(num) == 2:
                self.takeMoney(number * 2)
                return number * 2
            elif random_num.count(num) == 3:
                self.takeMoney(number * 3)
                return number * 3

    def __str__(self):
        return f'{self.__class__.__name__}{self.id} - доступний баланс {self.getMoney}'

    def __repr__(self):
        return f'{self.__class__.__name__}{self.id} - доступний баланс {self.getMoney}'