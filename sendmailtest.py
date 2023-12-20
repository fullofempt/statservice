from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Функция для отправки письма
def send_email(receiver_email, subject, html_content):
    sender_email = 'test1@yandex.ru'
    password = 'xxxxxx'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Добавление HTML в письмо
    message.attach(MIMEText(html_content, 'html'))

    try:
        server = smtplib.SMTP('smtp.example.com', 587)  #SMTP порт провайдера
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        return True, "Письмо успешно отправлено"
    except Exception as e:
        return False, f"Ошибка: {e}"

# API
@app.route('/sendMail', methods=['POST'])
def send_mail():
    data = request.json
    receiver_email = data.get('recipient') #из бд взять мэйлы
    subject = "Тема письма"
    html_content = data.get('content') 
 
    # Проверка наличия необходимых полей 
    if not receiver_email or not html_content:
        return jsonify({'success': False, 'message': 'Отсутствует адресат или содержимое'}), 400
    
    if not '@' in receiver_email:
        return jsonify({'success': False, 'message': 'Некорректный адрес электронной почты'}), 400

    success, message = send_email(receiver_email, subject, html_content)
    if success:
        return jsonify({'success': True, 'message': message})
    else:
        return jsonify({'success': False, 'message': message}), 500

if __name__ == '__main__':
    app.run(debug=True)
