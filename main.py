import re
from collections import UserDict
from datetime import datetime
from itertools import islice
import pickle
import os


class Record():
    def __init__(self, name, phone=None, birthday = None):
        self.name = name
        self.birthday = birthday
        self.phones= phone

    def add_phone(self, new_phone):
            self.phones.value.append(new_phone)

    def remove(self, phone):
        if type(self.phones.value)!=None:
            if self.phones.value == phone:
                self.phones.value = None
                return self.phones
            else:
                self.phones.value.remove(phone)
                return self.phones


    def change(self, phone, new_phone):
         if phone in self.phones.value:
             self.phones.value.remove(phone)
             self.phones.value.append(new_phone)
             return self.phones

    def days_until_birthday(self):
        if self.birthday:
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
                if obj[i].birthday:
                    result.append(f'Name:{i}; phones: {obj[i].phones.value}; Date of birth :{obj[i].birthday.value}.')
                else:
                    result.append(f'Name:{i}; phones: {obj[i].phones.value}')
            start += step
            end += step
            count -= step
            yield '\n'.join(result)

    def save_in_file(self):
        if os.path.isfile('data.bin'):
            with open('data.bin', 'wb') as fh:
                pickle.dump(self, fh)
        else:
            with open('data.bin', 'wb') as fh:
                pickle.dump(self, fh)


    @staticmethod
    def open_from_file():
        if os.path.isfile('data.bin'):
            with open('data.bin', 'rb') as fh:
                return pickle.load(fh)
        else:
            return AddressBook()

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
    birth=None
    pattern = re.compile(r'\d{4}-\d{1}-\d{1,2}')
    matches = (re.findall(pattern, lst[-1]))
    if len(matches)>0:
        matches = (re.findall(pattern, lst[-1]))[0]
        lst.remove(matches)
        match=matches.split('-')
        birth=Birthday(match)
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
    return "That's all contacts"

@input_error
def phone(lst):
    name = lst[1].capitalize()
    return (contacts_list[name].phones.value)

@input_error
def birthday(lst):
     name = lst[1].capitalize()
     return  contacts_list[name].days_until_birthday()

@input_error
def search_line(contact_list: dict , request):
    if len(request)==0:
        return 'I"m waiting for a command.'
    request=request.capitalize()
    result = []
    for key, value in contact_list.items():
        res_k = re.findall(request, key)
        res_v = re.findall(request, ' '.join(value.phones.value))
        if len(res_k)>0 or len(res_v)>0:
            result.append(f'{key}:{",".join(value.phones.value)}')
    if len(result)>0:
        return  '\n'.join(result)
    else:
        return 'I"m waiting for a command.'




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


contacts_list = AddressBook.open_from_file()
def main():
    while True:
        mess = input('>>> ').lower()
        if mess == 'exit':
            contacts_list.save_in_file()
            print('bye')
            break
        res=handler(mess)
        if type(res) == list and len(res)>0:
            print(commands_list[res[0]](res))
        elif type(res) != list:
            print(res)
        elif res==[]:
            print(search_line(contacts_list, mess))



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




