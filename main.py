import re



contacts_list={}
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
    contacts_list.update({name:lst[2]})
    return(f'I add contact {name} with phone {lst[2]}')

@input_error
def change(lst):
    name =lst[1].capitalize()
    contacts_list.update({name: lst[2]})
    return(f'I change contact {name} with phone {lst[2]}')

@input_error
def phone(lst):
    name = lst[1].capitalize()
    return (contacts_list[name])


def show_all():
    return (contacts_list)


commands_list={'hello': hello, 'add': add, "change": change, 'phone': phone, 'show all': show_all}
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
    'For end print exit')
    main()