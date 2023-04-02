import datetime


def value( value):
    year = datetime.datetime.now().year
    if int(value[0]) <= year and (int(value[1]) in range(13)) and (int(value[2]) in range(32)):
        res = f'{value[0]}.{value[1]}.{value[2]})'
        return res


print(value([2025,2,2]))
