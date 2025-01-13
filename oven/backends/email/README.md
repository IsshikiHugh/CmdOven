# Email Backend
A simple python mailing script.

Add your E-mail config at **~/.config/oven/cfg.yaml** and modify backend to email:
```bash
backend: email

email:
  # 
  smtp_server: smtp_server=<?> # smtp.sample.com
  smtp_port: smtp_port=<?> 
  sender_email: sender_email=<?> # sample@sample.com
  sender_pwd: sender_pwd=<?> 
  receiver_email: receiver_email=<?> # sample@sample.com
```

For QQ and icloud email boxes, smtp_port is **587**; 126 email box is **25**. Other email boxs are left to be tested.