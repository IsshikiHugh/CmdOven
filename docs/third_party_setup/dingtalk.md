# DingTalk Bot Setup

## Step 1. Create a DingTalk Group

Since DingTalk currently doesn't *directly* allow you to create a group with yourself only, you can invite two random people and create a minimal 3 people group. Feel free to remove them after adding your robots. (Maybe directly remove them also works.)

## Step 2. Add a Bot to the Group

Start creating DingTalk bot here: `Group Setting` > `Group Management` > `Bot` > `Add Robot` > `Custom`.
While setting the bot, choose "Custom Keywords" option in "Security Settings" section, and fill your custom secure key. **This key will be filled into the "secure_key" field in the configuration file.**

After finishing adding the robot, you can get the webhook here: `Group Setting` > `Group Management` > `Bot` > your_bot > `webhook`. **Copy it and it will be filled into the "hook" field in the configuration file.**