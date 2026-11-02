from json import loads


def parser_where(command, user_input) -> dict:
    try:
        command[3] == "where"
    except IndexError:
        return
    else:
        clause = user_input.split('where', 1)[1].strip()
        key, value = clause.split('=', 1)
        return {key.strip(): loads(value.strip())}


def parser_update(command, user_input):
    try:
        command[3] == "set"
    except IndexError:
        return
    else:
        clause = user_input.split('set', 1)[1].strip()
        set_clause, where_clause = clause.split('where', 1)
        key_s, value_s = set_clause.split('=', 1)
        key_w, value_w = where_clause.split('=', 1)
        return ({key_s.strip(): loads(value_s.strip())},
                {key_w.strip(): loads(value_w.strip())})

