class Language:

    def __new__(cls, lang, name, message):
        body = ''
        if lang == "es":
            body = cls.__es_lang(name=name, message=message)
        elif lang == "en":
            body = cls.__en_lang(name=name, message=message)
        return body

    @classmethod
    def __es_lang(cls, name, message) -> str:
        html_body = f'<h2>Gracias por contactarme {name}</h2>' +\
                    '<h3>Me enviaste una nueva solicitud de contacto con el siguiente mensaje:</h3>' +\
                    f'<strong>{message}</strong>'
        return html_body

    @classmethod
    def __en_lang(cls, name, message) -> str:
        html_body = f'<h2>Thanks for contact me {name}</h2>' +\
                    '<h3>You send a new contact request with the next message:</h3>' +\
                    f'<strong>{message}</strong>'
        return html_body
