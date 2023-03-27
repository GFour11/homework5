import re
from collections import UserDict


class Record():
    def __init__(self, name, phone=None):
        self.name = name
        self.phone = phone

    def add_phone(self, new_phone):
        if type(self.phone.value)!= list:
            res=list(self.phone.value)
            res.append(new_phone)
            self.phone = res
            return res
        else:
            self.phone.value.append(new_phone)
            ret=self.phone
            return ret

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

class AddressBook(UserDict):
    def add_record(self, record: Record):
        key = record.name.value
        self.data[key] = record
        return self.data


class Field:
    def __init__(self, value = None):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    pass


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
    phone = Phone(lst[2:])
    rec=Record(name,phone)
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

def show_all():
    str=''
    for k,v in contacts_list.items():
        v=v.phone.value
        if len(v)>0:
            str+=f"{k}:{','.join(v)}\n"
        else:
            str += f"{k}:{None}\n"
    return str

@input_error
def phone(lst):
    name = lst[1].capitalize()
    return (contacts_list[name].phone.value)


commands_list={'append': add_phone, 'hello': hello, 'add': add, "change": change, 'phone': phone, 'show all': show_all, 'remove':remove}

def handler(str):
    command=None
    str=str.lower()
    for i in commands_list:
        res = re.findall(i,str)
        if len(res)>0:
            command = i
            break
    name_phone=[]
    if command == 'show all':
        return show_all()
    elif command== 'hello':
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




