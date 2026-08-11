from flask_mail import Message
from extension import mail


def otp_verification(email, otp):
    msg = Message(
        'Your Verification Code',
        sender="no-reply@gmail.com",
        recipients=[email]
    )
    msg.body = f'Your 6 digit verification code: {otp}'
    mail.send(msg)



#  Simple OTP verification


# def otp_verification():
    
#     recipients = ['kikoyummy115@gmail.com']
    
#     msg = Message(
#         subject="Hello From Flask!",
#         sender="smakjit@NUM.edu",
#         recipients=recipients
#     )
    
#     msg.body = "This is a test email send from a flask"
    
#     mail.send(msg)
    
#     return "Email send to multiple recipients"