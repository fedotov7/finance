import json
import datetime

class MoneyTracker:
    def __init__(self):
        self.filename = "money.json"
        self.balance = 0
        self.history = []
        self.load_data()
    
    def load_data(self):
        """��������� ������ �� �����"""
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.balance = data['balance']
                self.history = data['history']
        except:
            self.balance = 0
            self.history = []
    
    def save_data(self):
        """��������� ������ � ����"""
        data = {
            'balance': self.balance,
            'history': self.history[-10:]  # ��������� ��������� 10 ��������
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_income(self, amount, description):
        """��������� �����"""
        self.balance += amount
        operation = {
            'date': datetime.datetime.now().strftime("%d.%m %H:%M"),
            'type': '�����',
            'amount': amount,
            'description': description,
            'balance': self.balance
        }
        self.history.append(operation)
        self.save_data()
        print(f" +{amount} ���. ({description})")
    
    def add_expense(self, amount, category):
        """��������� ������"""
        if amount > self.balance:
            print(" ������������ �������!")
            return False
        
        self.balance -= amount
        operation = {
            'date': datetime.datetime.now().strftime("%d.%m %H:%M"),
            'type': '������', 
            'amount': amount,
            'category': category,
            'balance': self.balance
        }
        self.history.append(operation)
        self.save_data()
        print(f" -{amount} ���. ({category})")
        return True
    
    def show_balance(self):
        """���������� ������� ������"""
        print(f"\n ���� ������: {self.balance} ���.")
        
        # ������ ���� �� �������
        today = datetime.datetime.now().strftime("%d.%m")
        today_expenses = [op for op in self.history 
                         if op['type'] == '������' and today in op['date']]
        
        if today_expenses:
            total_today = sum(op['amount'] for op in today_expenses)
            print(f" ������� ���������: {total_today} ���.")
    
    def show_history(self):
        """���������� ������� ��������"""
        print("\n ��������� ��������:")
        if not self.history:
            print("������� �����")
            return
        
        for op in self.history[-5:]:  # ��������� 5 ��������
            symbol = "+" if op['type'] == '�����' else "-"
            if op['type'] == '�����':
                print(f"{op['date']} {symbol}{op['amount']} ���. ({op['description']})")
            else:
                print(f"{op['date']} {symbol}{op['amount']} ���. ({op['category']})")
        
        print(f" ������: {self.history[-1]['balance']} ���.")

def main():
    tracker = MoneyTracker()
    
    print("=== ������ ��������� ����� ===")
    
    while True:
        print("\n1. �������� �����")
        print("2. �������� ������") 
        print("3. �������� ������")
        print("4. ������� ��������")
        print("5. �����")
        
        choice = input("\n������ ��������: ")
        
        if choice == '1':
            try:
                amount = int(input("����� ������: "))
                description = input("������ ������ (�������, �������� � �.�.): ")
                tracker.add_income(amount, description)
            except ValueError:
                print("����� �����!")
        
        elif choice == '2':
            try:
                amount = int(input("����� �������: "))
                categories = ["���", "���������", "�����������", "�������", "������"]
                print("���������:", ", ".join(categories))
                category = input("���������: ")
                if category not in categories:
                    category = "������"
                tracker.add_expense(amount, category)
            except ValueError:
                print("����� �����!")
        
        elif choice == '3':
            tracker.show_balance()
        
        elif choice == '4':
            tracker.show_history()
        
        elif choice == '5':
            tracker.show_balance()
            print("�� ��������!")
            break
        
        else:
            print("�������� �����!")

if __name__ == "__main__":
    main()
