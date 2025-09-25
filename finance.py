import json
import datetime

class MoneyTracker:
    def __init__(self):
        self.filename = "money.json"
        self.balance = 0
        self.history = []
        self.load_data()
    
    def load_data(self):
        """Загружает данные из файла"""
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.balance = data['balance']
                self.history = data['history']
        except:
            self.balance = 0
            self.history = []
    
    def save_data(self):
        """Сохраняет данные в файл"""
        data = {
            'balance': self.balance,
            'history': self.history[-10:]  # сохраняем последние 10 операций
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_income(self, amount, description):
        """Добавляет доход"""
        self.balance += amount
        operation = {
            'date': datetime.datetime.now().strftime("%d.%m %H:%M"),
            'type': 'доход',
            'amount': amount,
            'description': description,
            'balance': self.balance
        }
        self.history.append(operation)
        self.save_data()
        print(f" +{amount} руб. ({description})")
    
    def add_expense(self, amount, category):
        """Добавляет расход"""
        if amount > self.balance:
            print(" Недостаточно средств!")
            return False
        
        self.balance -= amount
        operation = {
            'date': datetime.datetime.now().strftime("%d.%m %H:%M"),
            'type': 'расход', 
            'amount': amount,
            'category': category,
            'balance': self.balance
        }
        self.history.append(operation)
        self.save_data()
        print(f" -{amount} руб. ({category})")
        return True
    
    def show_balance(self):
        """Показывает текущий баланс"""
        print(f"\n Твой баланс: {self.balance} руб.")
        
        # Анализ трат за сегодня
        today = datetime.datetime.now().strftime("%d.%m")
        today_expenses = [op for op in self.history 
                         if op['type'] == 'расход' and today in op['date']]
        
        if today_expenses:
            total_today = sum(op['amount'] for op in today_expenses)
            print(f" Сегодня потрачено: {total_today} руб.")
    
    def show_history(self):
        """Показывает историю операций"""
        print("\n Последние операции:")
        if not self.history:
            print("История пуста")
            return
        
        for op in self.history[-5:]:  # последние 5 операций
            symbol = "+" if op['type'] == 'доход' else "-"
            if op['type'] == 'доход':
                print(f"{op['date']} {symbol}{op['amount']} руб. ({op['description']})")
            else:
                print(f"{op['date']} {symbol}{op['amount']} руб. ({op['category']})")
        
        print(f" Баланс: {self.history[-1]['balance']} руб.")

def main():
    tracker = MoneyTracker()
    
    print("=== ТРЕКЕР КАРМАННЫХ ДЕНЕГ ===")
    
    while True:
        print("\n1. Добавить доход")
        print("2. Добавить расход") 
        print("3. Показать баланс")
        print("4. История операций")
        print("5. Выйти")
        
        choice = input("\nВыбери действие: ")
        
        if choice == '1':
            try:
                amount = int(input("Сумма дохода: "))
                description = input("Откуда деньги (подарок, зарплата и т.д.): ")
                tracker.add_income(amount, description)
            except ValueError:
                print("Введи число!")
        
        elif choice == '2':
            try:
                amount = int(input("Сумма расхода: "))
                categories = ["еда", "транспорт", "развлечения", "покупки", "другое"]
                print("Категории:", ", ".join(categories))
                category = input("Категория: ")
                if category not in categories:
                    category = "другое"
                tracker.add_expense(amount, category)
            except ValueError:
                print("Введи число!")
        
        elif choice == '3':
            tracker.show_balance()
        
        elif choice == '4':
            tracker.show_history()
        
        elif choice == '5':
            tracker.show_balance()
            print("До свидания!")
            break
        
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    main()
