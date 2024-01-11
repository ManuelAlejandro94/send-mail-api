from flask import Flask, request
from validations import validate_params
from responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok, ResponseError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From
import os
from models.language import Language
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)

@app.route("/send-email", methods=['POST'])
@cross_origin()
def send_email():

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

    message_mail = Mail(
        from_email=From('manuel_ale94@outlook.com', "API Portfolio Manuel Alvarez"),
        to_emails=f'{payload["email"]}',
        subject=f'API Portfolio Subject: {payload["subject"]}',
        html_content=Language(
            lang=payload["lang"],
            name=payload["name"],
            message=payload["message"]
        )
    )

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message_mail)
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
        raise e

import dynamic_template.template_service