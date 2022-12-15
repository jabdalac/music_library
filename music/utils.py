

def get_file_path(request, file):
    """
    Funcion que retorna el path del atributo field
    """
    if file:
        return request.build_absolute_uri(file.url)
    return None