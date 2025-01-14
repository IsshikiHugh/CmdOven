# Email Setup

## Step.1 Enable the SMTP service

You are required to enable the SMTP service of your email provider to send emails. Here are some common email providers and the steps to enable the SMTP service:

1. Enter your web client of your email and find the SMTP setting. It's usually under: `Settings` > `POP3/IMAP/SMTP`
2. Enable the SMTP service. Usually you can get a generated independent password for security reasons. You are suggested to use that generated password instead of your original email password. This password will be required later.
3. You need to find out which SMTP port is used to send emails by your email provider. Here are some common ports:
    - QQ mail / iCloud mail : 587
    - 126 mail : 25
    - TODO: more email providers (Help Wanted)

## Configuration Fields Explanation

- `smtp_server` : smtp server address of your email provider.
- `smtp_port` : smtp server port to sending emails, obtained at `Step.1`.
- `sender_email` : email address which is used to send emails, whose SMTP service is enabled at `Step.1`
- `sender_pwd` : the generated code you received at `Step.1`.
- `receiver_email` : email address which is used to receive emails.