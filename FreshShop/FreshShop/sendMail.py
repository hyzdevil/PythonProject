import smtplib #登陆邮件服务器，进行邮件发送
from email.mime.text import MIMEText #负责构建邮件格式

subject = "吴小梦的酒局邀请"
content = "python学不好怎么办？老铁"
sender = "huangyunzhong1001@163.com"
recver = """978246791@qq.com,
847464064@qq.com,
1693211121@qq.com,
931903956@qq.com,
1078126319@qq.com,
952537174@qq.com,
2373332166@qq.com,
1184976784@qq.com,
1403617606@qq.com,
1946648105@qq.com"""

password = "hyz580237"

message = MIMEText(content,"plain","utf-8")
message["Subject"] = subject
message["To"] = recver
message["From"] = sender

smtp = smtplib.SMTP_SSL("smtp.163.com",465)
smtp.login(sender,password)
smtp.sendmail(sender,recver.split(",\n"),message.as_string())
smtp.close()