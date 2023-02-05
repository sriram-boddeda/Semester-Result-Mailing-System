import csv
import pdfkit 
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

fromaddr = "FromEmail"
toaddr = "ToEmail"
fromPassword = "Password"

# instance of MIMEMultipart 
msg = MIMEMultipart() 

# storing the senders email address 
msg['From'] = fromaddr

# storing the receivers email address 
msg['To'] = toaddr

# storing the subject 
msg['Subject'] = "Semester Result"

# string to store the body of the mail 
body = "3-2 Sem Results"

# attach the body with the msg instance 
msg.attach(MIMEText(body, 'plain')) 


path = r"data.csv"
file1=open(path, newline='')
read=csv.reader(file1)

dic={'O':10,'S':9,'A':8,'B':7,'C':6,'D':5,'F':0,'ABSENT':0}
roll=["rolNum1","rolNum2","rolNum3","rolNum4"]
data={roll[0]:"studentEmail1",roll[1]:"studentEmail2",roll[2]:"studentEmail3"}

path1 = r"report_card.html"
file = open(path1,'w')
def cals(r):
    cal=0
    c=0
    st="<html><head></head><body><h3 align = 'center'>Semester Result</h3><h4 align = 'center'>Roll Number : "+r+"</h4><table align = 'center'><tr><th>Subject Name</th><th>Grade</th><th>Credits</th></tr>"
    for row in read:
        if(row[0]==r):
            cal += dic[row[3]]*int(row[4])
            c += int(row[4])
            st += "<tr><td>"+row[2]+"</td><td>"""+row[3]+"</td><td>"+row[4]+"</td><tr>"
            #st+=(row[2]+" "*(40-len(row[2]))+" "+"   "+row[3]+"   "+"   "+row[4]+"   \n")
    st+="</table><p align = 'center'>CGPA : {:.1f}".format(cal/c)+"</p>"
    st += "</body></html>"
    return st
file.write(cals(roll[1]))
file.close()

pdfkit.from_file('report_card.html', 'out.pdf') 

filename = "out.pdf"
attachment = open("out.pdf", "rb") 

# instance of MIMEBase and named as p 
p = MIMEBase('application', 'octet-stream') 

# To change the payload into encoded form 
p.set_payload((attachment).read()) 

# encode into base64 
encoders.encode_base64(p) 

p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 

# attach the instance 'p' to instance 'msg' 
msg.attach(p) 

# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 

# start TLS for security 
s.starttls() 

# Authentication 
s.login(fromaddr, fromPassword) 

# Converts the Multipart msg into a string 
text = msg.as_string() 

# sending the mail 
s.sendmail(fromaddr, toaddr, text) 

# terminating the session 
s.quit()
