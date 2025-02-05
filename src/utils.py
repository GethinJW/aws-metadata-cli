from logging import log

def get_nested_fields(ret_info: dict, _dict: dict, fields: list[str]):
    try:
        field_name = fields.pop(0)
    except IndexError:
        return ret_info
    try:
        ret_info[field_name] = _dict[field_name]
        return get_nested_fields(ret_info[field_name], _dict[field_name], fields)
    except TypeError as _err:
        log(f"Could not find attribute \"{field_name}\"!", "ERROR")