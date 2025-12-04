# Seiscomp_Utils
Bash and Python scrips around Seiscomp

Event_mail.job :

Bash script called from Seiscomp *scalert* when a new event is declared. It uses *scbulletin*, *scxmldump* and *scmapcut* (https://www.seiscomp.de/) to create a bulletin and an image map to be attached to an email and a Telegram messages. Linux mailutils and telegram-send utils (https://github.com/rahiel/telegram-send) must be installed and configured.


check_seedlink_problems.job :

Bash script to look for seedlink problems in network of seismic stations and send an alert by email and Telegram. A Time delay is configurable and an alert is sent when one or more stations overpass this delay. Another message is sent if the problem is solved in one or more stations.  slinktool (https://github.com/EarthScope/slinktool), Linux mailutils and telegram-send utils (https://github.com/rahiel/telegram-send) must be installed and configured.

It is advisable to run this script on a different computer than the seiscomp server.
