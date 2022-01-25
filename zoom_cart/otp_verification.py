import frappe
from frappe.utils import logger
import random
from datetime import datetime
from pytz import timezone



frappe.utils.logger.set_log_level("DEBUG")
logger = frappe.logger("zcart", allow_site=True, file_count=50)

@frappe.whitelist(allow_guest=True)

## Generate random otp, save against the email in otp verification doctype
## otp sent to email
def otp_verification(email):
    user = frappe.db.get_all('User',fields=['name'],filters={'email':email})

    for user_data in user:
        user_doc=frappe.get_doc("User",user_data['name'])
        otp=frappe.new_doc('OTP Password Verification')
        otp.user=user_doc.name
        num='0123456789'
        rand="".join(random.sample(num,5))
        otp.otp=rand
        otp.insert()

        content="Dear "+user_doc.first_name+","+'<br>' +"Your OTP to change password is " + rand
        recipient=user_doc.email
        send_email=frappe.sendmail(recipients=[recipient],sender=user_doc.owner,subject="Zoom Cart OTP Verification",content=content)

        frappe.email.doctype.email_queue.email_queue.send_now(send_email)

        return "OTP sent successfully"

@frappe.whitelist(allow_guest=True)
## verify the otp with user and change password
def password_change(otp,password):
    otp_doc=frappe.db.get_all("OTP Password Verification",fields=["name"],filters={"otp":otp})

    if otp_doc:
        for otp_field in otp_doc:
            otp_file=frappe.get_doc("OTP Password Verification",otp_field['name'])

            ind_time=datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
            cur_time=datetime.now()
            ind_time_date=datetime.strptime(ind_time, '%Y-%m-%d %H:%M:%S.%f')
            time_diff=ind_time_date-otp_file.creation

            if '1:00:00.000000'>=str(time_diff):
                user=frappe.get_doc("User",otp_file.user)
                user.new_password=password
                user.save(ignore_permissions=True)

                return "Password Changed Successfully"
            else:
                return "Your OTP has expired"

    else:
        return "Incorrect OTP"

@frappe.whitelist(allow_guest=True)
def signup(email,name,password):

    new_user=frappe.new_doc("User")
    users=frappe.db.get_all("User")

    for user in users:
        if user.name==email:
            return "You have already registered with email {}".format(email)

    new_user.email=email
    new_user.first_name=name
    new_user.new_password=password

    new_user.insert()
    new_user.save(ignore_permissions=True)

    user_reg=frappe.get_doc('User',new_user.email)

    default_role = frappe.db.get_value("Portal Settings", None, "default_role")
    if default_role:
        user_reg.add_roles(default_role)

    logger.info(f"{email} updated")

    return "You have successfully registered with email {}".format(email)





    













