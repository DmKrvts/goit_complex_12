import pickle
from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    ...

class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if value.isdigit() and len(value) == 10:
            self._value = value
        else:
            print(f"The number {value} has Invalid format, please make sure it has 10 digits.")

class Birthday(Field):
    @Field.value.setter
    def value(self, value: str):
        self._value = datetime.strptime(value, '%Y.%m.%d').date()

class Record:
    def __init__(self, name, birthday = None):
        self.name = Name(name)
        self.phones = []
        if birthday:
            self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        try:
            if self.birthday:
                current_date = datetime.now().date()
                record_nearest_birthday = self.birthday.value.replace(year=current_date.year)
                
                if record_nearest_birthday < current_date:
                    record_nearest_birthday = self.birthday.value.replace(year=current_date.year + 1)
                    days_until_birthday = (record_nearest_birthday - current_date).days
                   
                    print(f"Record: {self.name.value}, Nearest Birthday: {record_nearest_birthday}, Days until Birthday: {days_until_birthday}")
                return days_until_birthday
                
        except AttributeError:
            print(f"Contact name: {self.name.value}, do not have birthday record")
     
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))            

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None
    
    def remove_phone(self, phone):
        self.phones.remove(self.find_phone(phone))

    def edit_phone(self, phone, new_phone):
        existing_phone = self.find_phone(phone)
        if existing_phone:
            existing_phone.value = new_phone
        else:
            print(f"Phone number {phone} not found")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):

    def add_record(self, record):
        key = record.name.value
        self.data[key] = record

    def find(self, name):
        key = Name(name).value
        return self.data.get(key)

    def delete(self, name):
        key = Name(name).value
        
        if self.find(key):
            del self.data[key]

    def check(self, request):
        result = []
        for key, values in self.data.items():
            if request in key:
                result.append(key)
            for phone_number in values.phones:
                if request in str(phone_number.value):
                    result.append((key, phone_number.value))
        if result:
            for item in result:
                print(f'Match found: {item}')
        else:
            print('No matches found.')
        return result


    def dump(self):
        with open("file", 'wb') as file:
            for key, value in self.data.items():
               pickle.dump((key, value), file)
    
    def load(self):
        with open("file", "rb") as f:
            while True:
                try:
                   record_id, record = pickle.load(f)
                   self.data[record_id] = record
                except EOFError:
                    break   

    def iterator(self, item_number: int):
        print(f"Received item_number: {item_number}")
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += f'{item}: {record}\n'
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''

def main():
    
    book = AddressBook()

    try:
        book.load()
    except FileNotFoundError:
        print("please note, there is currently no backup file")

    while True:
        command = input("Enter a command: ").lower()

        if command in ["good bye", "close", "exit"]:
            book.dump()
            print("Good bye.")
            break

        elif command == "hello":
            print("hi, I`m your AddressBook bot\n  ")
        
        elif command == "show":
            for name, record in book.data.items():
                print(record)

        elif command.startswith("add"):
            try:
                record = Record(*command.split()[1:])
            except ValueError as e:
                print(e)
            consider_phone_number = input(f"provide phone numbers for {record.name} as list or press enter to skip: ")
            for phone in consider_phone_number.split():
                record.add_phone(phone)
            book.add_record(record)

        elif command.startswith("find"):
            record = book.find(command.split()[1])
            print(f"you may now check if {record.name} has birthday, or add, edit and remove {record.name} phones")
            record_command = input("Enter a record command: ").lower()
            if record_command == "skip":
                continue
            elif record_command == "birthday":
                record.days_to_birthday()
            elif record_command.startswith('add'):
                record.add_phone(record_command.split()[1])
            elif record_command.startswith('remove'):
                record.remove_phone(record_command.split()[1])
            elif record_command.startswith('edit'):
                record.edit_phone(record_command.split()[1:])
        
        elif command.startswith("check"):
            book.check(command.split()[1])

        elif command.startswith("delete"):            
            book.delete(command.split()[1])
            
        
if __name__ == '__main__':
    
    main()

   


    
    