import email
import imaplib
import quopri
from datetime import datetime, timedelta


class EmailReader:

    @staticmethod
    def get_first_text_block(email_message_instance):
        maintype = email_message_instance.get_content_maintype()
        if maintype == 'multipart':
            for part in email_message_instance.get_payload():
                if part.get_content_maintype() == 'text':
                    return part.get_payload()
        elif maintype == 'text':
            return email_message_instance.get_payload()

    @staticmethod
    def read_email(user_email, user_password, imap, to_filter=None, wait_time=0, expected_subject=None, expected_email_count=1):
        mail = imaplib.IMAP4_SSL(imap)
        mail.login(user_email, user_password)
        if to_filter is None:
            custom_filter = "ALL"
        else:
            custom_filter = '(TO "%s")' % to_filter
        if expected_subject is not None:
            custom_filter = '%s (SUBJECT "%s")' % (custom_filter, expected_subject)
        start_time = datetime.now()
        out = []
        while True:
            mail.list()
            mail.select()
            result, data = mail.search(None, custom_filter)
            if result == 'OK':
                email_contents = []
                id_list = data[0].split()
                if len(id_list) > 0 and len(id_list) == expected_email_count:
                    for mail_id in id_list:
                        result, data = mail.fetch(mail_id, '(RFC822)')
                        if result == 'OK':
                            email_contents.append(data[0][1])
                        else:
                            print(result)
                    if len(email_contents) > 0:
                        for email_content in email_contents:
                            email_content = email.message_from_bytes(email_content)
                            to_str = email_content['To']
                            from_str = email.utils.parseaddr(email_content['From'])
                            tet_block = EmailReader.get_first_text_block(email_content)
                            decoded_string = str(quopri.decodestring(tet_block))
                            body_str = decoded_string.replace('\\r\\r\\n', '').replace('\\r\\n', '')
                            out.append({'To': to_str, 'From': from_str, 'Body': body_str})
                    break
                if datetime.now() - start_time > timedelta(seconds=wait_time):
                    break
            else:
                print(result)
        return out
