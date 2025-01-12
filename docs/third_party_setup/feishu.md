# Feishu Bot Setup

## Step 1. Create a Feishu Group

Create a Feishu group and invite yourself only.

## Step 2. Add a Bot to the Group

Create a Feishu bot in `Settings` > `Bots` > `Bot` > `Add Bot` > `Custom Bot` > `Add`.
The Webhook URL will be generated after creating the bot. **Copy it and it will be filled into the "hook" field in the configuration file.**
In the "Security Settings" section, select `Set signature verification`, then a key will be created. **This key will be filled into the "secure_key" field in the configuration file.**
