from django.shortcuts import render
from django.http import HttpResponse
import email, smtplib, ssl, os, requests
import requests
from bs4 import BeautifulSoup

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# fetch page from url
page = requests.get(
    "https://mailerbulk.000webhostapp.com/test.php")
soup = BeautifulSoup(page.content, 'html.parser')

# Create your views here.
def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'mail_script.html')

def after_index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    # sending loops
    texts = []
    for tr in soup.find_all('tr')[1:]:
        tds = tr.find_all('td')
        # print(tds[0].text, tds[1].text, tds[2].text, tds[3].text)
        subject = "Maintenance Reciept"
        body = "Your maintenance reciept of month november"
        sender_email = "kartikresidency.devrangers@gmail.com"
        receiver_email = tds[2].text
        password = "Kartikresidency@1"
        
        #creating url for reciept 
        murl="https://mailerbulk.000webhostapp.com/upload/"
        furl="".join([murl,tds[3].text])
        #downloading pdf from online
        output_dir=''
        response=requests.get(furl)
        if response.status_code == 200:
            file_path=os.path.join(output_dir, os.path.basename(furl))
            with open(file_path, 'wb') as f:
                f.write(response.content)

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        filename = tds[3].text  # In same directory as script

        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:

            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)

        os.remove(tds[3].text)
        print("mail sent")
        texts.append("mail sent")
        
    return render(request, 'mail_script.html', {'texts' : texts})
