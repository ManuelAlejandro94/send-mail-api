from flask_cors import cross_origin
from validations import validate_params
from responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok, ResponseError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From
import os
from models.language import Language
from flask import request
from utils.logs import create_log_id

def register_routes(app):
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

        log_id = create_log_id()
        app.logger.info(f'LOGID: {log_id} - Parámetros de entrada: {payload}')
        dif_params = validate_params(params=params, request=payload)
        if dif_params:
            app.logger.info(
                f'LOGID: {log_id} - BadRequest(error=-1, message="Payload incomplete", details="Fields: {dif_params}") - HTTP 422')
            return BadRequest.with_results(
                error=-1,
                message="Payload incomplete",
                details=f"Fields: {dif_params}"
            )

        my_mail = "manuel_ale94@outlook.com"

        message_mail = Mail(
            from_email=From(f'{my_mail}', "API Portfolio Manuel Alvarez"),
            to_emails=f'{payload["email"]}',
            subject=f'API Portfolio Subject: {payload["subject"]}',
            html_content=Language(
                lang=payload["lang"],
                name=payload["name"],
                message=payload["message"]
            )
        )
        message_mail.add_cc(my_mail)

        try:
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(message_mail)
            if response.status_code != 202:
                app.logger.info(
                    f'LOGID: {log_id} - BadRequest(error=-1, message="Error sending mail", details={response.body}) - HTTP 500')
                return ResponseError.with_results(
                    error=-1,
                    message="Error sending email",
                    details=response.body
                )

            app.logger.info(f'LOGID: {log_id} - OK(code=0, message="Email sended correctly") - HTTP 200')
            return Ok.without_results(
                code=0,
                message="Email sended correctly"
            )
        except Exception as e:
            print(e)
            raise e