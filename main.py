import datetime


class Wallet:
    """Класс для управления кошельком."""

    def __init__(self, date: datetime, category: str, amount: int, description: str) -> None:
        """Инициализирует объект кошелька.

        Args:
            date (datetime): Дата операции.
            category (str): Категория операции (Доход или Расход).
            amount (int): Сумма операции.
            description (str): Описание операции.
        """
        self.date: datetime = date
        self.category: str = category
        self.amount: int = amount
        self.description: str = description

    @staticmethod
    def create_record(date: datetime, category: str, amount: int, description: str) -> 'Wallet':
        """Создает новую запись кошелька.

        Args:
            date (datetime): Дата операции.
            category (str): Категория операции (Доход или Расход).
            amount (int): Сумма операции.
            description (str): Описание операции.

        Returns:
            Wallet: Объект записи кошелька.
        """
        return Wallet(date, category, amount, description)

    @staticmethod
    def save_record_to_file(record, filename: str) -> None:
        """Сохраняет запись кошелька в файл.

        Args:
            record (Wallet): Запись кошелька.
            filename (str): Имя файла для сохранения.
        """
        with open(filename, 'a') as file:
            file.write(f"Дата: {record.date.strftime('%d.%m.%Y')}\n")
            file.write(f"Категория: {record.category}\n")
            file.write(f"Сумма: {record.amount}\n")
            file.write(f"Описание: {record.description}\n\n")

    @staticmethod
    def read_records_from_file(filename: str) -> list['Wallet']:
        """Читает записи кошелька из файла.

        Args:
            filename (str): Имя файла для чтения.

        Returns:
            list[Wallet]: Список записей кошелька.
        """
        records = []
        with open(filename, 'r') as file:
            lines = file.readlines()
            record_info = {}
            for line in lines:
                if line.strip() != "":
                    key, value = line.split(": ")
                    record_info[key] = value.strip()
                else:
                    if 'Дата' in record_info and 'Категория' in record_info and 'Сумма' in record_info and 'Описание' in record_info:
                        records.append(
                            Wallet(datetime.datetime.strptime(record_info['Дата'], '%d.%m.%Y'),
                                   record_info['Категория'],
                                   int(record_info['Сумма']), record_info['Описание']))
                    record_info = {}
        return records

    @staticmethod
    def calculate_balance(records: list['Wallet'], new_record: 'Wallet' = None) -> tuple[int, int, int]:
        """Вычисляет баланс кошелька.

        Args:
            records (list[Wallet]): Список записей кошелька.
            new_record (Wallet): Новая запись кошелька (необязательно).

        Returns:
            tuple[int, int, int]: Кортеж с доходами, расходами и балансом.
        """
        income: int = 0
        expenses: int = 0
        for record in records:
            if record.category == 'Доход':
                income += record.amount
            elif record.category == 'Расход':
                expenses += record.amount
        if new_record:
            if new_record.category == 'Доход':
                income += new_record.amount
            elif new_record.category == 'Расход':
                expenses += new_record.amount
        balance = income - expenses
        return income, expenses, balance

    @staticmethod
    def edit_record(records, date: datetime, category: str, amount: int, description: str) -> bool:
        """Редактирует существующую запись кошелька.

        Args:
            records: Список записей кошелька.
            date (datetime): Дата записи для редактирования.
            category (str): Категория записи для редактирования (Доход или Расход).
            amount (int): Сумма записи для редактирования.
            description (str): Описание записи для редактирования.

        Returns:
            bool: True, если запись была найдена и отредактирована, иначе False.
        """
        for record in records:
            if record.date == date and record.category == category and record.amount == amount and record.description == description:
                print("Запись найдена. Введите новые данные.")
                new_date_str = input("Введите новую дату в формате (дд.мм.гггг): ")
                new_date = datetime.datetime.strptime(new_date_str, '%d.%m.%Y')
                new_category = input("Введите новую категорию (Доход/Расход): ")
                new_amount = int(input("Введите новую сумму: "))
                new_description = input("Введите новое описание: ")
                record.date = new_date
                record.category = new_category
                record.amount = new_amount
                record.description = new_description
                print("Запись обновлена.")
                return True
        print("Запись не найдена.")
        return False

    @staticmethod
    def search_records(records, search_term: str, search_type: str) -> list['Wallet']:
        """Ищет записи кошелька по заданному критерию.

        Args:
            records: Список записей кошелька.
            search_term (str): Искомое значение.
            search_type (str): Тип поиска (категория, дата или сумма).

        Returns:
            list[Wallet]: Список найденных записей кошелька.
        """
        search_results = []
        for record in records:
            if search_type == 'категория' and search_term.lower() in record.category.lower():
                search_results.append(record)
            elif search_type == 'дата' and search_term == record.date.strftime('%d.%m.%Y'):
                search_results.append(record)
            elif search_type == 'сумма' and search_term == str(record.amount):
                search_results.append(record)
        return search_results


all_records = Wallet.read_records_from_file('wallet_data.txt')

print("Что вы хотите сделать?")
print("1. Добавить новую запись")
print("2. Редактировать запись")
print("3. Поиск записи")
choice = int(input("Введите номер действия: "))

if choice == 1:
    while True:
        date_str = input("Введите дату записи в формате (дд.мм.гггг): ")
        try:
            date = datetime.datetime.strptime(date_str, '%d.%m.%Y')
            break
        except ValueError:
            print("Неправильный формат даты. Пожалуйста, введите дату в формате (дд.мм.гггг).")

    while True:
        category = input("Введите категорию (Доход/Расход): ").capitalize()
        if category in ["Доход", "Расход"]:
            break
        else:
            print("Неправильная категория. Введите 'Доход' или 'Расход'.")

    while True:
        try:
            amount = int(input("Введите сумму: "))
            break
        except ValueError:
            print("Неправильный формат суммы. Пожалуйста, введите целое число.")

    description = input("Введите описание: ")
    new_record = Wallet.create_record(date, category, amount, description)
    Wallet.save_record_to_file(new_record, 'wallet_data.txt')

elif choice == 2:
    while True:
        date_to_edit_str = input("Введите дату записи для редактирования в формате (дд.мм.гггг): ")
        try:
            date_to_edit = datetime.datetime.strptime(date_to_edit_str, '%d.%m.%Y')
            break
        except ValueError:
            print("Неправильный формат даты. Пожалуйста, введите дату в формате (дд.мм.гггг).")

    while True:
        category_to_edit = input("Введите категорию для редактирования (Доход/Расход): ").capitalize()
        if category_to_edit in ["Доход", "Расход"]:
            break
        else:
            print("Неправильная категория. Введите 'Доход' или 'Расход'.")

    while True:
        try:
            amount_to_edit = int(input("Введите сумму для редактирования: "))
            break
        except ValueError:
            print("Неправильный формат суммы. Пожалуйста, введите целое число.")

    description_to_edit = input("Введите описание для редактирования: ")
    Wallet.edit_record(all_records, date_to_edit, category_to_edit, amount_to_edit, description_to_edit)

elif choice == 3:
    search_type = input("Введите тип поиска (категория/дата/сумма): ").lower()
    search_term = input("Введите искомое значение: ")
    found_records = Wallet.search_records(all_records, search_term, search_type)
    for record in found_records:
        print(
            f"Дата: {record.date.strftime('%d.%m.%Y')}, Категория: {record.category}, Сумма: {record.amount}, Описание: {record.description}")

income, expenses, balance = Wallet.calculate_balance(all_records, new_record)
current_date = datetime.datetime.now()
current_date_only = current_date.date()

print("Текущая дата:", current_date_only)
print("Доходы: ", income)
print("Расходы: ", expenses)
print("Баланс: ", balance)
