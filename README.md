# nLCplotSSH
Automated generation of pump plots after each measurement for Thermo easy-nLCs (tested with easy-nLC 1000) via SSH connection.

![nLCplotSSH](https://user-images.githubusercontent.com/34959927/192791307-c507a858-ef4f-416e-b732-535f63439240.png)

## Requirements
1. Install [Python 3.8](https://www.python.org/downloads/release/python-3810/) depending on your Windows version (32/64bit)
2. Install the following Python packages
```
pip install paramiko seaborn matplotlib pandas numpy
```
## Setup
1. Clone this repo or copy `nLCplotSSH.py` (f.e. to `C:\nLCplotSSH\`)
2. Create a dedicated output folder for the plots (f.e. `D:\nLC_plots\`)
3. Open Windows `Task Scheduler` and click on `Create Basic Task...` </br>
![grafik](https://user-images.githubusercontent.com/34959927/192747529-b66a33b8-8bae-4065-8ed2-b2be9a9c5242.png)

4. Select `When a specific event is logged` </br>
![grafik](https://user-images.githubusercontent.com/34959927/192747913-685e65e6-23cd-40b2-9d0b-618c1deb8355.png)

5. Setup the logging event </br>
![grafik](https://user-images.githubusercontent.com/34959927/192748391-42bc2424-b5e8-41e3-bf46-3bc60d854922.png)

6. Select `Start a program` </br>
![grafik](https://user-images.githubusercontent.com/34959927/192748604-e3e077c4-5e4e-4e66-b4f6-e37cebe1b03d.png)

7. Browse the path to nLCplotSSH.py`` and add the arguments `-ip "IP:ADRESS:OF:NLC" -o "D:\nLC_plots"` </br>
![grafik](https://user-images.githubusercontent.com/34959927/192753822-4288023f-9951-4492-8694-d7de9038f7d4.png)

8. Check `Open the Properties dialog for this task when I click Finish` and press Finish </br>
![grafik](https://user-images.githubusercontent.com/34959927/192754422-0ebab4b7-5788-445c-a2b3-dfa255d40cfd.png)

9. In the `General` tab of the Properties dialog check `Hidden` and Select Windows 7 in `Configure for:` </br>
![grafik](https://user-images.githubusercontent.com/34959927/192755681-83136c8e-35b3-4ced-b6c0-40c4de3a2bf1.png)

10. In the `Settings` tab select `1 hour` at `Stop the task if it runs longer than:` </br>
![grafik](https://user-images.githubusercontent.com/34959927/192757188-793b37f8-1514-484e-9052-8c5d4ed18ffa.png)

11. Press `Ok`. Plots will be automatically generated after each measurement.

## Optional arguments
```
argument          default value           description
-ip / --ip        "172.16.0.105"          easy-nLC IP address
-u  / --user      "hplc"                  User name for SSH connection
-p  / --password  "hplc"                  Password for SSH connection
-lp / --log_path  "/home/admin/batchLog"  Log path in easy-nLC filesystem
-o  / --out       "E:\_nLCplotsSSH"       Path for plot output
```
