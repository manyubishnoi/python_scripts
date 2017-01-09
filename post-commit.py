#!/usr/bin/env python
#
# This script sends emails in the same format as SVN default commit emails. 
#
# __author__ = manyubishnoi@gmail.com

import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from subprocess import check_output

def generate_blue_text_color(input_file):
    html_blue = """
      <html>
        <head>
        <style>
        p1 {
            color: blue;
            text-align: left;
            font-size: 15px;
           }
        </style>
        </head>
        <body>
          <p1></br>"""+str(input_file)+"""</p1>
        </body>
      </html>
      """
    return html_blue

def generate_blue_bg_color(input_line):
    html_blue = """
      <html>
        <head>
        <style>
        p2 {
            color: white;
            text-align: center;
            font-size: 15px;
            font-family: monospace;
           }
        </style>
        </head>
       <body>
          <div style="background-color:rgb(50, 104, 169)">
          <p2></br><b>"""+str(input_line)+"""</b></br></p2>
        </body>
      </html>
      """
    return html_blue

def generate_red_bg_color(input_line):
    html_red = """
      <html>
        <head>
        <style>
        p3 {
            color: black;
            text-align: left;
            font-size: 12px;
            font-family: monospace;
           }
        </style>
        </head>
        <body>
          <div style="background-color:rgb(254, 220, 218)">
          <p3>"""+str(input_line)+"""</br></p3>
        </body>
      </html>
      """
    return html_red

def generate_green_bg_color(input_line):
    html_green = """
      <html>
        <head>
        <style>
        p4 {
            color: black;
            text-align: left;
            font-size: 12px;
            font-family: monospace;
           }
        </style>
        </head>
        <body>
          <div style="background-color:rgb(193, 255, 198)">
          <p4>"""+str(input_line)+"""</br></p4>
        </body>
      </html>
      """
    return html_green

def generate_grey_bg_color(input_line):
    html_green = """
      <html>
        <head>
        <style>
        p5 {
            color: black;
            text-align: left;
            font-size: 12px;
            font-family: monospace;
           }
        </style>
        </head>
        <body>
          <div style="background-color:rgb(243, 247, 247)">
          <p5>"""+str(input_line)+"""</br></p5>
        </body>
      </html>
      """
    return html_green

def generate_header(input_line):
    header = """
      <html>
        <head>
        <style>
        p6 {
            color: white;
            text-align: left;
            font-size: 12px;
           }
        </style>
        </head>
        <body>
          <div style="background-color:rgb(50, 104, 169);padding:3px">
          <p6>"""+str(input_line)+"""</br></p6>
          </div>
        </body>
      </html>
      """
    return header

def generate_commit_template(input_line):
    header = """
      <html>
        <head>
        <style>
        p7 {
            color: black;
            text-align: left;
            font-size: 12px;
            font-family: monospace;
           }
        </style>
        </head>
        <body>
          <div style="background-color:rgb(255,255,180)">
          <p7>"""+str(input_line)+"""</br></p7>
          </div>
        </body>
      </html>
      """
    return header

def send_emails(commit_log, modified_files_list, verbose_diff_data_list):
    email_list = []
    msg = MIMEMultipart()
    line_break = "\n\n"
    line_break_MIME = MIMEText(line_break, 'plain')

    msg['Subject'] = 'Git commit notification'
    msg['From'] = 'me@gmail.com'

    # Getting the email ID of the last committer. 
    email_regex = re.compile('<(.*)>')
    email_only = re.findall(email_regex,commit_log[1])
    email_list.append(email_only[0])

    msg['To'] = email_list[0]

    for aline in commit_log[0:3]:
        colored_file = generate_header(aline)
        email_compatible_file_format = MIMEText(colored_file, 'html')
        msg.attach(email_compatible_file_format)
    
    log_string = """<b></br>Log Message:</b></br></br>"""
    text_part1 = MIMEText(log_string, 'html')
    msg.attach(text_part1)

    for aline in commit_log[4:]:
        if len(aline) > 0:
            colored_file = generate_commit_template(aline)
            email_compatible_file_format = MIMEText(colored_file, 'html')
            msg.attach(email_compatible_file_format)

    paths_string = "<b></br></br>Modiflied Paths:</br></b>"
    text_part2 = MIMEText(paths_string, 'html')
    msg.attach(text_part2)

    for afile in modified_files_list:
        colored_file = generate_blue_text_color(afile)
        email_compatible_file_format = MIMEText(colored_file, 'html')
        msg.attach(email_compatible_file_format)
        
    diff_string = "<b></br>Diff:</br></b>"
    text_part3 = MIMEText(diff_string, 'html')
    msg.attach(text_part3)

    for each in verbose_diff_data_list:
        email_compatible_format = ""
        if re.search("diff --git ",each):
            msg.attach(line_break_MIME)
            colored_line = generate_blue_bg_color(each)
            
        elif re.match("\+",each):
            colored_line = generate_green_bg_color(each)

        elif re.match("-",each):
            colored_line = generate_red_bg_color(each)
        else:
            colored_line = generate_grey_bg_color(each)
    
        email_compatible_diff_format = MIMEText(colored_line, 'html')
        msg.attach(email_compatible_diff_format)
 
    server = smtplib.SMTP('smtp.gmail.com')
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


# Get the git log entry of the new commit
git_last_commit_log = check_output(['git', 'log', '-1'])
git_last_commit_log_list = git_last_commit_log.split('\n')

#git_last_commit_msg = check_output(['git', 'log', '-1', '--pretty=%B'])
#git_last_commit_msg_list = git_last_commit_msg.split('\n')

files_changed = check_output(['git', 'diff', '--name-status', 'HEAD^..HEAD'])
files_changed_list = files_changed.split('\n')

verbose_diff = check_output(['git', 'diff', 'HEAD^..HEAD'])
verbose_diff_list = verbose_diff.split('\n')

send_emails(git_last_commit_log_list, files_changed_list, verbose_diff_list)

