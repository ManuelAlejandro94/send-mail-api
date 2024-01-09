def validate_params(params, request):
    """Valida que existan los parámetros de entrada"""
    keys = []
    for key in request.keys():
        keys.append(key)
    campos_faltantes = list(set(params).difference(keys))
    return campos_faltantes