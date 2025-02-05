from logging import log


def get_nested_fields(ret_info: dict, _dict: dict, fields: list[str]):
    try:
        field_name = fields.pop(0)
    except IndexError:
        return ret_info

    try:
        value = _dict[field_name]

        if not fields:
            ret_info[field_name] = (
                {fields[-1]: value[fields[-1]]}
                if isinstance(value, dict) and fields[-1] in value
                else value
            )
            return ret_info

        if isinstance(value, list):
            ret_info[field_name] = []
            for item in value:
                if isinstance(item, dict):
                    nested_info = {}
                    ret_info[field_name].append(
                        get_nested_fields(nested_info, item, fields.copy())
                    )
                else:
                    ret_info[field_name].append(item)
        else:
            ret_info[field_name] = {}
            ret_info[field_name] = get_nested_fields(
                ret_info[field_name], value, fields
            )

    except (TypeError, KeyError):
        log(f'Could not find attribute "{field_name}"!', "ERROR")

    return ret_info
