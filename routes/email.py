from flask import Blueprint, request, jsonify, current_app
from libs.functions import sendMail

email_route = Blueprint('email_route', __name__)
@email_route.route('/sendemail', methods=['POST'])
def sendemail():
    subject = '..::WEBSITE MESSAGE::..'
    to_name = 'sacm'
    to_email = current_app.config['MAIL_USERNAME']
    from_email = request.json.get('from_email', None)
    message = request.json.get('message', None)
    html_msg = ('<div><p>This is a message from your web, check the information below:</p><p>Contact email: '+from_email+'</p><p>Contact message: '+message+'</p></div>')

    if not from_email:
        return jsonify({"error": "Email is required"}), 422
    if not message:
        return jsonify({"error": "Message is required"}), 422

    sendMail(subject, to_name, to_email, to_email, html_msg)
    return jsonify({"success": "Email send successfully"}), 200
