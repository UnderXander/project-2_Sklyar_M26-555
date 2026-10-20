


database = {}
def create_table(command: list):
    global database
    columns = command[2:]
    data = list()
    data_type = list()
    for i in range(len(columns)):
        data.append(columns[i].split(sep=':')[0])
        data_type.append(columns[i].split(sep=':')[1])
    print(data)
    database[str(command[1])] = {'ID': f'{}', f'{command[2]}'}
create_table(['create_table', 'users', 'name:str', 'age:int'])