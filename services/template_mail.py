import os

from sendgrid import Email, Personalization, SendGridAPIClient

from validations import validate_params
from responses import ResponseErrorBadRequest as BadRequest, ResponseOk as Ok, ResponseError
from flask import request
from sendgrid.helpers.mail import Mail
from models.template_language import TemplateLanguage
from flask_cors import cross_origin
from utils.logs import create_log_id

def register_routes(app):

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
        mail = Mail()
        mail.from_email = Email(f"{my_mail}")
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
        mail.add_cc(my_mail)

        try:
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.client.mail.send.post(request_body=mail.get())
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