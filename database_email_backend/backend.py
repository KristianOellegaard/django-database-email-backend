#-*- coding: utf-8 -*-
from email.MIMEBase import MIMEBase
from django.core.mail.backends.base import BaseEmailBackend
from database_email_backend.models import Email, Attachment
from django.utils.encoding import force_unicode


class DatabaseEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        if not email_messages:
            return
        for message in email_messages:
            email = Email.objects.create(
                from_email = force_unicode(u'%s' % message.from_email),
                to_emails = force_unicode(u', '.join(message.to)),
                cc_emails = force_unicode(u', '.join(message.cc)),
                bcc_emails = force_unicode(u', '.join(message.bcc)),
                all_recipients = force_unicode(u', '.join(message.recipients())),
                subject = u'%s' % force_unicode(message.subject),
                body = u'%s' % force_unicode(message.body),
                raw = u'%s' % force_unicode(message.message().as_string())
            )
            for attachment in message.attachments:
                if isinstance(attachment, tuple):
                    filename, content, mimetype = attachment
                elif isinstance(attachment, MIMEBase):
                    filename = attachment.get_filename()
                    content = attachment.get_payload(decode=True)
                    mimetype = None
                else:
                    continue
                Attachment.objects.create(
                    email=email,
                    filename=filename,
                    content=content,
                    mimetype=mimetype
                )
