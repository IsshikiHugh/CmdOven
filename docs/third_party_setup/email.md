# Email Setup

## Step.1 Enable the SMTP service
This step is for sending emails.

Open your mail in the web browser and find the SMTP setting. 

Usually at: `Settings` > `POP3/IMAP/SMTP`

You might be asked to send a message to a specified number or verify your identification to enable this service.

Once you finish the procedure they asked, you will receive a generated code, which works as a password; keep it carefully. Remeber to take down the **SMTP server address** and the **SMTP server port** of your email, which are usually found in the `POP3/IMAP/SMTP` settings .

For QQ and icloud email boxes, smtp_port is **587**; 126 email box is **25**. Other email boxs are left to be tested. You can just fill it in the config file if your email is one of them.

## Setp.2 Fill in your information in the configuration file.

To obtain notification by email, you need to set some parameters：
1. `smtp_server` : smtp server address of your email provider.
2. `smtp_port` : smtp server port to sending emails, obtained at `Step.1`.
3. `sender_email` : email address which is used to send emails, whose SMTP service is enabled at `Step.1` 
4. `sender_pwd` : the generated code you received at `Step.1`.
5. `receiver_email` : email address which is used to receive emails.

All the necessary information is gathered when you finish `Step.1`. Fill in the infomation in `~/.config/oven/cfg.yaml`