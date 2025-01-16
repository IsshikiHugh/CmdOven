# Bark Setup

## Step.1 Get your device token

Your are required to download Bark and register your device. A code will be generated to represents your device. You can find your code at `Settings` > `Info` > `Device Token`

## Configuration Fields Explanation

- `device_token` : device token to identify your device.
- `level` : Push Levels of notifications.
  - active: Default, immediately wakes the screen to display the notification.
  - timeSensitive: Time-sensitive notifications, can be shown during Focus Mode.(To be tested, not works for me.)
  - passive: Adds the notification to the list without waking the screen.
  - critical: Yes it's critical!
  
- `group` : Group messages. Notifications will be displayed in the notification center by group.
You can also view different groups in the history list.
- `url` : The URL to redirect to when the push notification is tapped.