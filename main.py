import re



contacts_list={}
def input_error(func):
    def excepter(lst):
        try:
           return func(lst)
        except KeyError:
            print ('Enter user name')
        except ValueError:
            print ('Give me name and phone please')
        except IndexError:
            print('Give me name and phone please')
        except TypeError:
            print ('Give me name and phone please')
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
        return commands_list[command]
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
        elif mess == 'hello':
            mess = (commands_list[mess]())
            print(mess)
        elif mess == 'show all':
            mess = (commands_list[mess]())
            print(mess)
        else:
            res = handler(mess)
            try:
                conclusion = commands_list[res[0]](res)
                if conclusion!= None:
                    print(conclusion)
            except IndexError:
                print('I"m waiting for a command.')