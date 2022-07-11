#### Status-Tracker

Status Tracker is exactly what it says. As a result of having a certain status, the bot will reward the user with a role. This bot's script isn't the cleanest, but it gets the job done and if you aren't very experienced, it's better than nothing. This can be used when giving away prizes or just wanting to let your members show off how much they support your server.

#### How does it work?

Whenever the event **on_member_update** is triggered, status tracker will check the users status and if the users status matches the configuration than the bot will add the role reward that was setup in the configuration however, if the user has the role and wrong status the bot will go ahead and remove the role. The bot also logs all these updates within the set status update channel.

#### Commands

```
 Name       | Description                 |
- - - - - - | - - - - - - - - - - - - - - |
 Help       |  Helpful information        |   
 Stats      |  Bot information            |
 Ping       |  Check Latency              |
 Checklist  |  Check's bots permissions   |
 Check-all  |  Check's everyone status    |
 Server     |  Configuration              |
```

#### Wiki 

```py
print("Commands" + "https://status-tracker.gitbook.io/status-tracker/dashboard/commands")
print("FAQ" + "https://status-tracker.gitbook.io/status-tracker/dashboard/faq")
```

#### Supports

- [x] MongoDB
- [x] Slash commands
- [x] Dropdown Menus
- [x] Buttons

#### Tasks
I plan to make this script better, it's been nearly a year now and I learnt a lot of new things and a lot of new discord features have come out!

- [ ] User friendly
- [ ] Easy setup
- [ ] Re-code
