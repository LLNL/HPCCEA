
# VNC Tutorial

1. Download VNC Viewer
  a. If do not have VNC Viewer, go to MacPatch → Software → VNC Viewer → Install
2. Open VNC Viewer
3. Enter **czvnc.llnl.gov:5999** in the search bar at the top
4. Enter your OUN as the User, and Pin + RSA Token as the Password
5. Select action: start server (or if you have a previous session - Connect to server)
6. Go to Applications → System Tools → Konsole (you'll need 2 konsoles)
7. In one Konsole:
  a. Log into lgw2-pub
  b. Open remote firefox instance running on lgw2-pub

```
firefox --no-remote
```
8. In another Konsole:
  a. Log into cluster (krypton, nickel, etc)
  b. Run your flask app (See the Hello World Flask App Tutorial)