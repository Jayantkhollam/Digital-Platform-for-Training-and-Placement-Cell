import pandas as pd
import os
from twilio.rest import Client
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

def save_faculty_data(fac_email,fac_password,fac_r_password,fac_name,fac_l_name,fac_mobile,fac_dept):
    row = {'Name': fac_name,'Last Name': fac_l_name,'Email': fac_email, 'Mobile': fac_mobile,
                    'Password': fac_password, 'confirm_password': fac_r_password,'Department':fac_dept}
    if os.path.exists('Documents/faculty_data.xlsx'):
        df = pd.read_excel('Documents/faculty_data.xlsx')
        append_data = pd.Series(row, name=len(df))
        df = df.append(append_data).reset_index(drop=True)
        df.to_excel('Documents/faculty_data.xlsx',index=False)
    else:
        df = pd.DataFrame(columns = ['Name','Last Name','Email', 'Mobile','Password', 'confirm_password','Department'])
        append_data = pd.Series(row, name=len(df))
        df = df.append(append_data).reset_index(drop=True)
        df.to_excel('Documents/faculty_data.xlsx',index=False)

def save_student_data(stu_email,stu_password,stu_r_password,stu_name,stu_l_name,stu_mobile,stu_dept,stu_year,stu_gender,fy,sy,ty,be,year,cast):
    row = {'Name': stu_name,'Last Name': stu_l_name,'Email': stu_email, 'Mobile': stu_mobile,
                    'Password': stu_password, 'confirm_password': stu_r_password,'Department':stu_dept,'Year':stu_year,'Gender':stu_gender,
                    'FY CGPA':fy,'SY CGPA':sy,'TY CGPA':ty,'B.Tech CGPA':be,'Year of Admission':year,'Caste':cast}
    if os.path.exists('Documents/student_data.xlsx'):
        df = pd.read_excel('Documents/student_data.xlsx')
        append_data = pd.Series(row, name=len(df)) 
        df = df.append(append_data).reset_index(drop=True)
        df.to_excel('Documents/student_data.xlsx',index=False)
        df_1 = df[['Name','Last Name','Email', 'Mobile','Department','Year','Gender','FY CGPA','SY CGPA','TY CGPA','B.Tech CGPA','Year of Admission','Caste']]
        df_1.to_excel('static/student_data_show.xlsx',index=False)
    else:
        df = pd.DataFrame(columns = ['Name','Last Name','Email', 'Mobile','Password', 'confirm_password','Department','Year','Gender','FY CGPA','SY CGPA','TY CGPA','B.Tech CGPA','Year of Admission','Caste'])
        append_data = pd.Series(row, name=len(df))
        df = df.append(append_data).reset_index(drop=True)
        df.to_excel('Documents/student_data.xlsx',index=False)
        df_1 = df[['Name','Last Name','Email', 'Mobile','Department','Year','Gender']]
        df_1.to_excel('static/student_data_show.xlsx',index=False)

def download_stu_data(dept,year):
    df = pd.read_excel('Documents/student_data.xlsx')
    df_1 = df[['Name','Last Name','Gender','Caste','Email','Mobile','Department','Year','Year of Admission','FY CGPA','SY CGPA','TY CGPA','B.Tech CGPA']]
    download_df = df_1[(df_1['Year'] == year) & (df_1['Department'] == dept)]
    download_df.to_excel('Documents/stu_download_data.xlsx',index=False)


def create_message(c_name,date,time,role,message):
    msg = f"""Company Name: {c_name}

    Job Title: {role}

    Drive Time: {date}, {time}

    {message}

    How to Apply:
    Interested candidates should bring a copy of their resume and portfolio to our office during the drive time specified above. We look forward to meeting you!


        """

    return msg

def send_whatsapp_message(to_numbers, message):
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)
    try:
        for to_number in to_numbers:
            message = client.messages.create(
                body=message,
                from_='whatsapp:',
                to=f'whatsapp:+91{to_number}'
            )
            print(f"Message sent successfully to {to_number}: {message.sid}")
    except Exception as e:
        print(f"Error occurred: {e}")

def send_email(to_emails, msg_body, file_path):
    print(file_path)
    from_email = ''
    password = ''
    body = msg_body

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['Subject'] = "Campus Notification!"
    msg.attach(MIMEText(body, 'plain'))

    # Attach the PDF file
    if file_path!=None:
        with open(file_path, 'rb') as f:
            part = MIMEApplication(f.read(), Name='attachment.pdf')
        part['Content-Disposition'] = 'attachment; filename="attachment.pdf"'
        msg.attach(part)

    try:
        # Connect to the server
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(from_email, password)

        for to_email in to_emails:
            try:
                msg['To'] = to_email
                server.sendmail(from_email, to_email, msg.as_string())
                print(f"Email sent successfully to {to_email}!")
            except smtplib.SMTPDataError as e:
                print(f'SMTPDataError for {to_email}: {e}')
            except Exception as e:
                print(f'Error for {to_email}: {e}')
            time.sleep(2)  # Delay to avoid hitting rate limits

        server.quit()
    except smtplib.SMTPDataError as e:
        print(f'SMTPDataError: {e}')
    except Exception as e:
        print(f'Error: {e}')

    # server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    # server.starttls()
    # server.login(from_email, password)

    # for to_email in to_emails:
    #     msg['To'] = to_email
    #     server.sendmail(from_email, to_email, msg.as_string())
    #     print(f"Email sent successfully to {to_email}!")

    # server.quit()

# def send_email(to_emails, msg_body,file_path):
#     from_email = 'ncerproject24@hotmail.com'
#     password = 'password@ncer'
#     body = msg_body

#     msg = MIMEMultipart()
#     msg['From'] = from_email
#     msg['Subject'] = "Campus Notification"

#     msg.attach(MIMEText(body, 'plain'))

#     server = smtplib.SMTP('smtp-mail.outlook.com', 587)
#     server.starttls()
#     server.login(from_email, password)
    
#     for to_email in to_emails:
#         msg['To'] = to_email
#         server.sendmail(from_email, to_email, msg.as_string())
#         print(f"Email sent successfully to {to_email}!")

#     server.quit()

def save_alumni_data(al_name,al_email,al_password,al_pass_year):
    row = {'Name': al_name,'Email': al_email,'Password': al_password, 'Passout Year': al_pass_year}
    if os.path.exists('Documents/alumni_data.xlsx'):
        df = pd.read_excel('Documents/alumni_data.xlsx')
        append_data = pd.Series(row, name=len(df))
        df = df.append(append_data).reset_index(drop=True)
        df.to_excel('Documents/alumni_data.xlsx',index=False)
    else:
        df = pd.DataFrame(columns = ['Name','Email','Password','Passout Year'])
        append_data = pd.Series(row, name=len(df))
        df = df.append(append_data).reset_index(drop=True)
        df.to_excel('Documents/alumni_data.xlsx',index=False)

def save_alumni_form_data(al_name,al_c_name,al_position,al_email,al_avail):
    row = {'Name': al_name,'Company Name': al_c_name,'Position': al_position, 'Email': al_email,'Availability' : al_avail}
    if os.path.exists('Documents/alumni_form_data.xlsx'):
        df = pd.read_excel('Documents/alumni_form_data.xlsx')
        append_data = pd.Series(row, name=len(df))
        df = df.append(append_data).reset_index(drop=True)
        df.to_excel('Documents/alumni_form_data.xlsx',index=False)
    else:
        df = pd.DataFrame(columns = ['Name','Company Name','Position','Email','Availability'])
        append_data = pd.Series(row, name=len(df))
        df = df.append(append_data).reset_index(drop=True)
        df.to_excel('Documents/alumni_form_data.xlsx',index=False)


def send_email_alumni(to_emails, msg_body, file_path):
    from_email = 'nceralumni@hotmail.com'
    password = 'password@ncer'
    body = msg_body

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['Subject'] = "Alumni Connection!"
    msg.attach(MIMEText(body, 'plain'))

    # Attach the PDF file
    with open(file_path, 'rb') as f:
        part = MIMEApplication(f.read(), Name='resume.pdf')
    part['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    msg.attach(part)

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(from_email, password)

    for to_email in to_emails:
        msg['To'] = to_email
        server.sendmail(from_email, to_email, msg.as_string())
        print(f"Email sent successfully to {to_email}!")

    server.quit()