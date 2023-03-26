import re
from collections import UserDict

class AddressBook(UserDict):
        def add_record(self, record):
            key = record.name.value
            self.data[key] = record
            return self.data


class Record():
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def add_phone(self, name, new_phone):
        if type(self.phone.phone) == str:
            res=list(self.phone.phone)
            res.append(new_phone)
            ret=Record(name, res)
            return ret
        else:
            self.phone.phone.append(new_phone)
            ret=Record(name, self.phone)
            return ret

    def remove(self, name, phone):
        if self.phone.phone == phone:
            return None
        else:
            self.phone.phone.remove(phone)
            return Record(name, self.phone)


    def change(self, name, phone, new_phone):
         if phone in self.phone.phone:
             self.phone.phone.remove(phone)
             self.phone.phone.append(new_phone)
             return Record(name,self.phone)

class Field():
    def __init__(self, name, info):
        self.name = name
        self.info = info

class Name(Field):
    def __init__(self, value, info = None):
        self.value = value
        super().__init__(value, info)


class Phone(Field):
    def __init__(self, phone, info = None):
        self.phone = phone
        super().__init__(phone, info)




def input_error(func):
    def excepter(*args):
        try:
           return func(*args)
        except KeyError:
            return ('Enter user name')
        except ValueError:
            return ('Give me name and phone please3')
        except IndexError:
            return ('Give me name and phone please2')
        except TypeError:
            return ('Give me name and phone please1')
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
    res =obj.add_phone(name, new_phone)
    contacts_list.update({name:res})
    return ('I add another phone')

@input_error
def remove(lst):
    name = lst[1].capitalize()
    new_phone=lst[2]
    obj = contacts_list[name]
    res =obj.remove(name, new_phone)
    contacts_list.update({name:res})
    return ('I remove phone')

@input_error
def change(lst):
    name = lst[1].capitalize()
    new_phone=lst[3]
    phone = lst[2]
    obj = contacts_list[name]
    res=obj.change(name, phone,new_phone)
    contacts_list.update({name: res})
    return ('I change phone')

def show_all():
    str=''
    for k,v in contacts_list.items():
        v=v.phone.phone
        str+=f"{k}:{','.join(v)}\n"
    return str


@input_error
def phone(lst):
    name = lst[1].capitalize()
    return (contacts_list[name].phone.phone)


commands_list={'append number': add_phone, 'hello': hello, 'add': add, "change": change, 'phone': phone, 'show all': show_all, 'remove':remove}

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




