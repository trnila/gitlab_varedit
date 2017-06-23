def create(variables):
    def n(val):
        if "\n" in val:
            return '"{0}"'.format(val)
        return val

    return "\n".join(["=".join([var[0], n(var[1])]) for var in variables.items()])


def parse(text):
    in_key = True
    in_quote = False
    result = {}
    key = ""
    value = ""
    do_append = False

    def append():
        result[key.strip()] = value.strip().strip("'\"")

    for c in text:
        if c == "\"" and (not value or (value and value[-1] != '\\')):
            if in_quote:
                do_append = True
            else:
                in_quote = True
        elif c == "=":
            in_key = False
        elif c == "\n" and key and not in_quote:
            do_append = True
        elif in_quote or c not in [" ", "\n", "="]:
            if in_key:
                key += c
            else:
                value += c

        if do_append:
            append()
            key = ""
            value = ""
            in_key = True
            in_quote = False

            do_append = False

    if key:
        append()

    return result


def diff(before, after):
    return {
        'add': list(after.keys() - before.keys()),
        'delete': list(before.keys() - after.keys()),
        'update': [k for k in before.keys() if k in after and after[k] != before[k]]
    }
