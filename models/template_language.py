class TemplateLanguage:

    def __new__(cls, lang, name, message):
        obj = {}
        if lang == "es":
            obj = cls.__es_lang(name=name, message=message)
        elif lang =="en":
            obj = cls.__en_lang(name=name, message=message)
        return obj

    @classmethod
    def __es_lang(cls, name, message) -> dict:
        obj_es = {
            "header": f'Gracias por contactarme {name}',
            "header3": "Me enviaste una nueva solicitud de contacto con el siguiente mensaje:",
            "message": message
        }
        return obj_es

    @classmethod
    def __en_lang(cls, name, message) -> dict:
        obj_en = {
            "header": f'Thanks for contact me {name}',
            "header3": "You send a new contact request with the next message:",
            "message": message
        }
        return obj_en