#Send email API

##Description

This is a Flask project to send emails using Sendgrid, include two endpoints.
One endpoint use a customizing mail and the another one use a template where we send the values with fill it.
The endpoints include a param `lang` for select language of email:
* `es` for Spanish
* `en` for English

This because the API is plannning for be used by my portfolio webpage and his functionality of change language.

##Endpoints
The app has only 2 endpoints:
```
    POST /send-email
    POST /send-template-mail
```
All fields required

###Examples
Both endpoints use the same json
```
{
    "name": "My Name",
    "email": "mail_to_send@example.com",
    "subject": "Template Test",
    "message": "This is a test to send emails with the current template",
    "lang": "en"
}
```