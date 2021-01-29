def make_valid_dict(query_params: dict):
    params = dict()
    for key, value in query_params.items():
        if len(value) == 1:
            params.update({key: value[0]})
        else:
            param = {key: None} if isinstance(value, str) and value == 'null' else {key: value}
            params.update(param)
    return params
