import os

from sendgrid import Email, Personalization, SendGridAPIClient

from validations import validate_params
from app import app
from responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok, ResponseError
from flask import request
from sendgrid.helpers.mail import Mail
from models.template_language import TemplateLanguage
from flask_cors import cross_origin

@app.route("/send-template-mail", methods=['POST'])
@cross_origin()
def send_email_template():
    payload = request.get_json()
    params = [
        "name",
        "email",
        "subject",
        "message",
        "lang"
    ]

    dif_paramas = validate_params(params=params, request=payload)
    if dif_paramas:
        return BadRequest.with_results(
            error=-1,
            message="Payload incomplete",
            details=f"Fields: {dif_paramas}"
        )

    mail = Mail()
    mail.from_email = Email("manuel_ale94@outlook.com")
    mail.template_id = 'd-3b901435cfa64a688b71648d16784763'

    p = Personalization()
    p.add_to(Email(payload["email"]))
    data = TemplateLanguage(
        lang=payload["lang"],
        name=payload["name"],
        message=payload["message"]
    )
    p.dynamic_template_data = data
    mail.add_personalization(p)

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.client.mail.send.post(request_body=mail.get())
        if response.status_code != 202:
            return ResponseError.with_results(
                error=-1,
                message="Error sending email",
                details=response.body
            )

        return Ok.without_results(
            code=0,
            message="Email sended correctly"
        )
    except Exception as e:
        print(e)