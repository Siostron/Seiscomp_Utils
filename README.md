# Seiscomp_Utils
Bash and Python scrips around Seiscomp


- ## eventAlert/Event_mail.job :

  Bash script called from Seiscomp *scalert* when a new event is declared. It uses *scbulletin*, *scxmldump* and *scmapcut* (https://www.seiscomp.de/) to create a bulletin and an image map to be attached to an email and a Telegram messages. Linux *mailutils* and *telegram-send* utils (https://github.com/rahiel/telegram-send) must be installed and configured.
  
  
  <img width="867" height="908" alt="Event alert Email and Telegram" src="https://github.com/user-attachments/assets/c90126ad-4bab-4b0d-a0a4-478a16dbccd5" />


- ## seedlink/check_seedlink_problems.job :

  Bash script to look for seedlink problems in a network of seismic stations received by a Seiscomp Server. It sends an alert by email and Telegram if a configurable Time delay is overpassed by one or more stations. Another message is sent if the problem is solved in one or more stations. *slinktool* (https://github.com/EarthScope/slinktool), Linux *mailutils* and *telegram-send* utils (https://github.com/rahiel/telegram-send) must be installed and configured. It is advisable to run this script on a different computer than the Seiscomp server.

    Ex:  `` > ./check_seedlink_problems.job YH >& ./Trash/seedlink_check_YH.log &``
  

   <img width="920" height="631" alt="Seedlink Alert email and telegram" src="https://github.com/user-attachments/assets/2d034b4e-44f6-4d21-855d-5df065145c70" />

 

- ## seedlink/check_seedlink_problems_station.job :

  Bash script to look for seedlink problems in single station of a seismic network received in a Seiscomp Server. It sends an alert by email and Telegram if a configurable Time delay is overpassed. Another alert is sent if the problem is solved. *slinktool* (https://github.com/EarthScope/slinktool), Linux *mailutils* and *telegram-send* utils (https://github.com/rahiel/telegram-send) must be installed and configured. It is advisable to run this script on a different computer than the Seiscomp server.

    Ex: `` > ./check_seedlink_problems_station.job CA ICJA >& ./Trash/seedlink_check_CA_ICJA.log &``


   <img width="1069" height="859" alt="Seedlink Alert email and telegram" src="https://github.com/user-attachments/assets/3115c7d5-79e8-40ea-856f-5b8bf184c27b" />

- ## Playback scripts

  Bash and Python Opspy scripts to preapre continous mseed data to run a Real-Time playback in a Non-Prduction Seiscomp server injecting data with *msrtsimul* in historic mode (https://www.seiscomp.de/doc/base/tutorials/waveformplayback.html)
  
- ###  Playback/Descarrega_CanviaBlockSize.py

  First, we retrieve all the data to analize with a Python script usyng Obspy (https://github.com/obspy/obspy/wiki/). We download them using the fdsnws from our Production Seiscomp server. We build 2 mseeds files per day, one from 0-12h and the other 12-24h. This is to avoid problems with large files, as ObsPy can currently not directly read mini-SEED files that are larger than 2^31 bytes (2048 MiB). Data is repacked to 512 bytes.

  
- ###  Playback/scmssort.job

  Secondly, we sort the downloaded data by end time using *scmssort  -u -E* in a bash script. This way multiplexed data is flowing into the system as in real time.

  
- ###  Playback/Playback_via_script.job

  At the end we are ready to run the playback itself. With this Bash script we play all the sorted mseed with ``msrtsimul -v -s 10.0 -m historic`` command (https://www.seiscomp.de/doc/apps/msrtsimul.html#msrtsimul) at speed 10 time higher than natural flow. 10 days are processed in a day.

  Procedure:

  ```
  ./Descarrega_CanviaBlockSize.py
  ./scmssort.job
  ./Playback_via_script.job
  ```

- ## CreateInventory/Inventory_date_hour.py

  Python script to create a xml Inventory from station Response files using Obspy (https://github.com/obspy/obspy/wiki/) and Inventory (https://github.com/SeismicData/pyasdf/blob/master/pyasdf/inventory_utils.py) Utils.

  Station coordinates and recording start and end dates are given in a csv file looking like:

  ```
  #station;lat;lon;height;install;uninstall
  BJN1;42.348837;-2.105215;25.1;2021-269T09:28:16.4100;2022-269T11:12:31.1300
  BJN2;42.368469;-2.115131;37.0;2021-269T07:27:09.4100;2022-269T09:00:34.7700
  ```

