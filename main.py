import re
from collections import UserDict
from datetime import datetime
from itertools import islice


class Record():
    def __init__(self, name, phone=None, birthday = None):
        self.name = name
        self.birthday = birthday
        self.phone= phone

    def add_phone(self, new_phone):
        new = Phone(new_phone)
        if len(new.value)>0:
            self.phone.value.append(new.value)

    def remove(self, phone):
        if type(self.phone.value)!=None:
            if self.phone.value == phone:
                self.phone.value = None
                return self.phone
            else:
                self.phone.value.remove(phone)
                return self.phone


    def change(self, phone, new_phone):
         if phone in self.phone.value:
             self.phone.value.remove(phone)
             self.phone.value.append(new_phone)
             return self.phone

    def days_until_birthday(self):
        if self.birthday.value:
            today = datetime.now().date()
            birthday = datetime.strptime(self.birthday.value, '%Y-%m-%d').date().replace(year=today.year)
            if birthday < today:
                birthday = birthday.replace(year=today.year + 1)
            days_until = (birthday - today).days
            return f'it {days_until} days until his birthday'
        return 'Date not set'

class AddressBook(UserDict):
    def add_record(self, record: Record):
        key = record.name.value
        self.data[key] = record
        return self.data

    def iterator(self, obj: dict, step):
        count = len(obj)
        start = 0
        end = step
        lst = [i for i in obj.keys()]
        while count > 0:
            if end > len(lst):
                end = len(lst)
            res = list(islice(lst, start, end))
            result = []
            for i in res:
                result.append(f'Name:{i}; phones: {obj[i].phone.value}; Date of birth :{obj[i].birthday.value}.')
            start += step
            end += step
            count -= step
            yield '\n'.join(result)


class Field:
    def __init__(self, value = None):
        self.value = value


class Name(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value
    @value.setter
    def value(self,value):
        if value.isalpha():
            self.__value = value
        else:
            raise KeyError
class Phone(Field):
    def __init__(self,value: list):
        self.__value = []
        self.value = value
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self,value):
        for i in value:
            if i.isdigit():
                self.__value.append(i)
            else:
                raise ValueError

class Birthday(Field):
    def __init__(self, value):
        self.__value = []
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        year = datetime.now().year
        if int(value[0])<=year and ( int(value[1]) in range(13)) and (int(value[2]) in range(32)):
            self.__value = f'{value[0]}-{value[1]}-{value[2]}'


def input_error(func):
    def excepter(*args):
        try:
           return func(*args)
        except KeyError:
            return ('Enter user name')
        except ValueError:
            return ('Give me name and phone please')
        except IndexError:
            return ('Give me name and phone please')
        except TypeError:
            return ('Give me name and phone please')
    return excepter

def hello():
    return ('How can I help you?')

@input_error
def add(lst):
    name = lst[1].capitalize()
    name=Name(name)
    birth=Birthday([1,1,1])
    pattern = re.compile(r'\d{4}-\d{1}-\d{1,2}')
    matches = (re.findall(pattern, lst[-1]))
    if len(matches)>0:
        matches = (re.findall(pattern, lst[-1]))[0]
        lst.remove(matches)
        f=matches.split('-')
        birth=Birthday(f)
    phone = Phone(lst[2:])
    rec=Record(name,phone, birth)
    contacts_list.add_record(rec)
    return('I add contact')

@input_error
def add_phone(lst):
    name = lst[1].capitalize()
    new_phone=lst[2]
    obj = contacts_list[name]
    obj.add_phone(new_phone)
    return ('I add another phone')

@input_error
def remove(lst):
    name = lst[1].capitalize()
    phone=lst[2]
    obj = contacts_list[name]
    obj.remove(phone)
    return ('I remove phone')

@input_error
def change(lst):
    name = lst[1].capitalize()
    new_phone=lst[3]
    phone = lst[2]
    obj = contacts_list[name]
    obj.change(phone,new_phone)
    return ('I change phone')

@input_error
def show_all(lst):
    step = int(lst[-1])
    gen_obj=contacts_list.iterator(contacts_list, step)
    for i in gen_obj:
        print(i)
        input('Press any button for next contacts')


@input_error
def phone(lst):
    name = lst[1].capitalize()
    return (contacts_list[name].phone.value)

@input_error
def birthday(lst):
     name = lst[1].capitalize()
     return  contacts_list[name].days_until_birthday()


commands_list={'append': add_phone, 'hello': hello, 'add': add, "change": change, 'phone': phone, 'show': show_all, 'remove':remove, 'birthday': birthday}

def handler(str):
    command=None
    str=str.lower()
    for i in commands_list:
        res = re.findall(i,str)
        if len(res)>0:
            command = i
            break
    name_phone=[]
    if command== 'hello':
        return hello()
    else:
        flag = False
        for i in str.split():
            if flag:
                name_phone.append(i)
            elif i == command:
                flag = True
                name_phone.append(i)
        return name_phone


contacts_list = AddressBook()
def main():
    while True:
        mess = input('>>> ').lower()
        if mess == 'exit':
            print('bye')
            break
        res=handler(mess)
        if type(res) == list and len(res)>0:
            print(commands_list[res[0]](res))
        elif type(res) != list:
            print(res)
        else:
            print('I"m waiting for a command.')



if __name__ == '__main__':
    print('This bot create for your contacts list \n'
          'He can add new contact, change contact number \n'
           'or show you full list of contacts')
    print('for doing something print a command then space then contact name space number')
    print('Bot commands: add - for add contact\n'
    'change - for change contact number\n'
    'phone - to know user phone\n'
    'show all - showed full contacts list\n'
    'append - for add new number in contact\n'
    'remove - for delete contact number\n'
    'For end print exit')
    main()




