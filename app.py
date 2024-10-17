from flask import Flask, render_template, request, session, redirect,jsonify, send_file, make_response
from functions import save_faculty_data, save_student_data,download_stu_data,create_message,send_whatsapp_message,send_email,save_alumni_data
from functions import save_alumni_form_data, send_email_alumni
import pandas as pd
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/alumni.html')
def alumni():
    alumni_data_base = pd.read_excel('Documents/alumni_form_data.xlsx')
    df_1 = alumni_data_base[alumni_data_base['Availability'] == 'on']
    df_1.to_excel('static/alumni_avail_data.xlsx',index=False)
    return render_template('alumni.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/sign_in.html')
def sign_in():
    return render_template('sign_in.html')

@app.route('/register', methods=['POST'])
def info():
    fac_data_base = pd.read_excel('Documents/faculty_data.xlsx')
    stu_data_base = pd.read_excel('Documents/student_data.xlsx')
    fac_email = request.form.get('fac_email')
    fac_password = request.form.get('fac_password')
    fac_r_password = request.form.get('fac_re_password')
    fac_name = request.form.get('fac_f_name')
    fac_l_name = request.form.get('fac_l_name')
    fac_mobile = request.form.get('fac_mobile')
    fac_dept = request.form.get('fac_department')
    if fac_email != None:
        if fac_email  in fac_data_base['Email'].values:
            return render_template('register.html',status_teacher = "You have Already Registered")
        else:
            save_faculty_data(fac_email,fac_password,fac_r_password,fac_name,fac_l_name,fac_mobile,fac_dept)
            return render_template('register.html',status_teacher = "Registered Successfully")
    stu_email = request.form.get('stu_email')
    stu_password = request.form.get('stu_password')
    stu_r_password = request.form.get('stu_re_password')
    stu_name = request.form.get('stu_f_name')
    stu_l_name = request.form.get('stu_l_name')
    stu_mobile = request.form.get('stu_mobile')
    stu_dept = request.form.get('stu_department')
    stu_year = request.form.get('stu_year')
    stu_gender = request.form.get('stu_gender')
    first = request.form.get('first_year_cgpa')
    second = request.form.get('second_year_cgpa')
    third = request.form.get('third_year_cgpa')
    final = request.form.get('fourth_year_cgpa')
    adm_year = request.form.get('year_admission')
    cast = request.form.get('caste')
    if stu_email != None:
        if stu_email  in stu_data_base['Email'].values:
            return render_template('register.html',status_student = "You have Already Registered")
        else:
            save_student_data(stu_email,stu_password,stu_r_password,stu_name,stu_l_name,stu_mobile,stu_dept,stu_year,stu_gender,
                              first,second,third,final,adm_year,cast)
            return render_template('register.html',status_student = "Registered Successfully")
        

@app.route('/sign_in', methods=['POST'])
def Sign_In():
    fac_data_base = pd.read_excel('Documents/faculty_data.xlsx')
    stu_data_base = pd.read_excel('Documents/student_data.xlsx')
    fac_email = request.form.get('fac_email')
    fac_password = request.form.get('fac_password')
    idx = fac_data_base[fac_data_base['Email'] == fac_email]['Password'].index
    if fac_email != None:
        if fac_email in fac_data_base['Email'].values and fac_password == fac_data_base[fac_data_base['Email'] == fac_email]['Password'][idx[0]]:
            return render_template('inner_faculty.html')
        else:
            return render_template('sign_in.html', status_teacher = "Wrong credentials! Please try again.")
    stu_email = request.form.get('stu_email')
    stu_password = request.form.get('stu_password')
    idx = stu_data_base[stu_data_base['Email'] == stu_email]['Password'].index
    if stu_email != None:
        if stu_email in stu_data_base['Email'].values and stu_password == stu_data_base[stu_data_base['Email'] == stu_email]['Password'][idx[0]]:
            return render_template('inner_student.html')
        else:
            return render_template('sign_in.html', status_student = "Wrong credentials! Please try again.")
        
@app.route('/download_stu_data', methods=['POST'])
def down_data():
    dept = request.form.get('dept')
    year = request.form.get('year')
    download_stu_data(dept.upper(),year)
    rendered_template = render_template('inner_faculty.html')
    response = make_response(rendered_template)
    response.headers['Content-Disposition'] = 'attachment; filename=student_data.xlsx'
    response.headers['Content-type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    excel_file_path = 'Documents/stu_download_data.xlsx'
    response.set_data(open(excel_file_path, 'rb').read())
    
    return response

@app.route('/send_message', methods=['POST'])
def send():
    stu_data_base = pd.read_excel('Documents/student_data.xlsx')
    c_name = request.form.get('c_name')
    date = request.form.get('d_date')
    time = request.form.get('d_time')
    role = request.form.get('j_role')
    dept = request.form.get('dept')
    msg = request.form.get('message')
    f = request.files['campus_file']
    f_name = secure_filename(f.filename)
    print('filename')
    print(len(f_name))
    msg_body = create_message(c_name,date,time,role,msg)
    print('asagsdj',c_name)
    print(msg_body)
    numbers = list(stu_data_base[stu_data_base['Department'] == dept.upper()]['Mobile'])
    if dept == "All Departments":
        emails = list(stu_data_base['Email'])
    else:
        emails = list(stu_data_base[stu_data_base['Department'] == dept.upper()]['Email'])
    print(emails)
    if len(f_name)>0:
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'static/campus attachment', secure_filename(f.filename))
        print(file_path)
        f.save(file_path)
        print('file saved')
        send_email(emails,msg_body,file_path)
    else:
        send_email(emails,msg_body,None)
    print(numbers)
    send_whatsapp_message(numbers,msg_body)
    return render_template('inner_faculty.html')

@app.route('/alumnu_registration', methods=['POST'])
def alu_register():
    alumni_data_base = pd.read_excel('Documents/alumni_data.xlsx')
    al_name = request.form.get('al_name')
    al_email = request.form.get('al_email')
    al_pass = request.form.get('al_pass')
    al_year = request.form.get('al_g_year')
    if al_name != None:
        save_alumni_data(al_name,al_email,al_pass,al_year)
    return render_template('alumni.html')

@app.route('/alumni_login', methods=['POST'])
def alu_login():
    alumni_data_base = pd.read_excel('Documents/alumni_data.xlsx')
    al_email = request.form.get('al_mail')
    al_pass = request.form.get('al_password')
    idx = alumni_data_base[alumni_data_base['Email'] == al_email]['Password'].index
    if al_email != None:
        if al_email in alumni_data_base['Email'].values and al_pass == alumni_data_base[alumni_data_base['Email'] == al_email]['Password'][idx[0]]:
            return render_template('inner_alumni.html')
        else:
            return render_template('alumni.html')

@app.route('/alumnu_form', methods=['POST'])
def alu_form():
    alumni_data_base = pd.read_excel('Documents/alumni_form_data.xlsx')
    al_name = request.form.get('al_name')
    al_c_name = request.form.get('al_c_name')
    al_position = request.form.get('al_position')
    al_email = request.form.get('al_email')
    al_avail = request.form.get('al_avail')
    if al_name != None:
        save_alumni_form_data(al_name,al_c_name,al_position,al_email,al_avail)
    return render_template('inner_alumni.html')

@app.route('/process_selected_data', methods = ['GET','POST'])
def alumni_data():
    global alumni_email
    selected_data = request.json.get('selectedData')
    alumni_email = selected_data[0][0]
    al = [alumni_email]
    print(alumni_email, 'list = ',al)
    return render_template('alumni.html')

@app.route('/email_alumni', methods = ['GET','POST'])
def send_email_to_alu():
    global f_name
    # stu_name = request.form.get('stu_name')
    # stu_email = request.form.get('stu_email')
    stu_message = request.form.get('stu_msg')
    print(alumni_email)
    f = request.files['resume']
    f_name = secure_filename(f.filename)
    basepath = os.path.dirname(__file__)
    file_path = os.path.join(basepath, 'static/resume', secure_filename(f.filename))
    f.save(file_path)
    print('static/resume/'+f_name)
    send_email_alumni([alumni_email],stu_message,'static/resume/'+f_name)
    return render_template('alumni.html')

 
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')