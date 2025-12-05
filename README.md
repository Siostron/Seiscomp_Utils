# Seiscomp_Utils
Bash and Python scrips around Seiscomp

- # CreateInventory/Inventory_date_hour.py

  Python script to create a xml Inventory from station Response files using Obspy (https://github.com/obspy/obspy/wiki/) and Inventory (https://github.com/SeismicData/pyasdf/blob/master/pyasdf/inventory_utils.py) Utils.

  Station coordinates and recording start and end dates are given in a csv file looking like:

    #station;lat;lon;height;install;uninstall
    BJN1;42.348837;-2.105215;25.1;2021-269T09:28:16.4100;2022-269T11:12:31.1300
    BJN2;42.368469;-2.115131;37.0;2021-269T07:27:09.4100;2022-269T09:00:34.7700


- # eventAlert/Event_mail.job :

  Bash script called from Seiscomp *scalert* when a new event is declared. It uses *scbulletin*, *scxmldump* and *scmapcut* (https://www.seiscomp.de/) to create a bulletin and an image map to be attached to an email and a Telegram messages. Linux mailutils and telegram-send utils (https://github.com/rahiel/telegram-send) must be installed and configured.


- # seedlink/check_seedlink_problems.job :

  Bash script to look for seedlink problems in a network of seismic stations received by a Seiscomp Server. It sends an alert by email and Telegram if a configurable Time delay is overpassed by one or more stations. Another message is sent if the problem is solved in one or more stations. *slinktool* (https://github.com/EarthScope/slinktool), Linux mailutils and telegram-send utils (https://github.com/rahiel/telegram-send) must be installed and configured. It is advisable to run this script on a different computer than the Seiscomp server.

    Ex:  ./check_seedlink_problems.job CA >& ./Trash/seedlink_check_CA.log &

- # seedlink/check_seedlink_problems_station.job :

  Bash script to look for seedlink problems in single station of a seismic network received in a Seiscomp Server. It sends an alert by email and Telegram if a configurable Time delay is overpassed. Another alert is sent if the problem is solved. *slinktool* (https://github.com/EarthScope/slinktool), Linux mailutils and telegram-send utils (https://github.com/rahiel/telegram-send) must be installed and configured. It is advisable to run this script on a different computer than the Seiscomp server.

    Ex: ./check_seedlink_problems_station.job CA ICJA >& ./Trash/seedlink_check_CA_ICJA.log &

<img width="1088" height="295" alt="Sin nombre" src="https://github.com/user-attachments/assets/5d4be5cd-5644-4ee9-a71b-17965d815ff7" />

