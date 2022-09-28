import os
import paramiko
from argparse import ArgumentParser
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

parser = ArgumentParser()
parser.add_argument("-ip", "--ip", dest="machine_ip",
                    default="172.16.0.105",
                    help="easy-nLC IP address")
parser.add_argument("-u", "--user", dest="username",
                    default="hplc",
                    help="User name for SSH connection")
parser.add_argument("-p", "--password", dest="password",
                    default="hplc",
                    help="Password for SSH connection")
parser.add_argument("-lp", "--log_path", dest="log_path",
                    default="/home/admin/batchLog",
                    help="Log path")
parser.add_argument("-o", "--out", dest="out_dir_path",
                    default=r"E:/_nLCplotsSSH",
                    help="Path for plot output")
args = parser.parse_args()

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(args.machine_ip, port=22, username=args.username, password=args.password)
sftp = ssh.open_sftp()
sftp.chdir(args.log_path)

log_events = sorted(sftp.listdir())
log_event_path = os.path.join(sftp.getcwd(), log_events[-1]).replace("\\", "/")
log_event_path_alt = os.path.join(sftp.getcwd(), log_events[-2]).replace("\\", "/")

# check if Gradient.txt exists otherwise take the sample folder before last one
sftp.chdir(log_event_path)
log_events_sub = sftp.listdir_attr()
sftp.chdir([le for le in log_events_sub if le.st_size == 4096][0].filename)
if "Gradient.txt" in sftp.listdir():
    log_file_name = log_events[-1]
else:
    sftp.chdir(log_event_path_alt)
    log_events_sub_alt = sftp.listdir_attr()
    sftp.chdir([le for le in log_events_sub_alt if le.st_size == 4096][0].filename)
    if "Gradient.txt" in sftp.listdir():
        log_file_name = log_events[-2]

df_A = pd.read_table(sftp.open("Pump A.txt"))
df_B = pd.read_table(sftp.open("Pump B.txt"))
df_G = pd.read_table(sftp.open("Gradient.txt"))

sftp.close()
ssh.close()

df_G = df_G[df_G["flow [nl/min]"].notna()]

df_A["min"] = ((pd.to_datetime(df_A["time"], format='%H:%M:%S.%f') - pd.to_datetime("00:00:00.000", format='%H:%M:%S.%f')).dt.total_seconds()/60).astype(int)
df_B["min"] = ((pd.to_datetime(df_B["time"], format='%H:%M:%S.%f') - pd.to_datetime("00:00:00.000", format='%H:%M:%S.%f')).dt.total_seconds()/60).astype(int)
df_G["min"] = ((pd.to_datetime(df_G["time"], format='%H:%M:%S.%f') - pd.to_datetime("00:00:00.000", format='%H:%M:%S.%f')).dt.total_seconds()/60).astype(int)

fig, axs = plt.subplots(nrows=3)
plt.subplots_adjust(wspace=0.5, hspace=0.5)
fig.set_figheight(8)

plt_a = sns.lineplot(data=df_A, x='time', y='pressure [bar]', ax=axs[0], ci=None)
plt_b = sns.lineplot(data=df_B, x='time', y='pressure [bar]', ax=axs[1], ci=None)
plt_g = sns.lineplot(data=df_G, x='time', y='flow [nl/min]', ax=axs[2], ci=None)

plt_a.set_title("Pump A")
plt_b.set_title("Pump B")
plt_g.set_title("Gradient")

tick_step_a = int(np.floor(len(df_A))/5)
tick_step_b = int(np.floor(len(df_B))/5)
tick_step_g = int(np.floor(len(df_G))/5)

plt_a.set_xticks(range(len(df_A))[::tick_step_a])
plt_b.set_xticks(range(len(df_B))[::tick_step_b])
plt_g.set_xticks(range(len(df_G))[::tick_step_g])

plt_a.set_xticklabels(df_A["min"].tolist()[::tick_step_a])
plt_b.set_xticklabels(df_B["min"].tolist()[::tick_step_b])
plt_g.set_xticklabels(df_G["min"].tolist()[::tick_step_g])

plt.suptitle(log_file_name, fontsize=14)

plt.savefig(os.path.join(args.out_dir_path, "{}.png".format(log_file_name)))
