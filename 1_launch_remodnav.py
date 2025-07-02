import sys
from math import ceil
from data_processing import DataProcessing
import subprocess
import os

def calc_sample_rate(times):
    dtime=0
    prev_time = times[0]
    for this_time in times[1:]:
        dtime += float(this_time) - float(prev_time)
        prev_time = this_time
    dtime /= len(times) - 1
    return 1.0 / dtime

def write_remodnav_file(indata, outfile):
    with open(outfile + "l", 'w') as fl:
        with open(outfile + "r", 'w') as fr:
            lx, ly, rx, ry = indata
            for i in range(len(lx)):
                fl.write("{:f}\t{:f}\n".format(lx[i], ly[i]))
                fr.write("{:f}\t{:f}\n".format(rx[i], ry[i]))

def calc_min_savgol(sample_rate):
    decimals = 5
    sl = 5.0 / sample_rate
    factor = 10 ** decimals
    return ceil(sl * factor) / factor

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage " + sys.argv[0] + " <infile> <outfile_prefix>")
    else:
        conv = DataProcessing(sys.argv[1])
        data = conv.gaze_conversion()
        Kpix_deg = 0.068055
        write_remodnav_file(data[0], sys.argv[2])  # chiamo la tupla dei pixels
        sample_rate = calc_sample_rate(data[2])
        print("average sample rate: {:f}".format(sample_rate))
        savgol = calc_min_savgol(sample_rate)
        print("mininum savgol len: ~{:f}".format(savgol))
        print("remodnav --savgol-length {:f} ".format(savgol) +
              sys.argv[2] + "l outfile_l {:f} {:f}".format(Kpix_deg, sample_rate))
        print("remodnav --savgol-length {:f} ".format(savgol) +
              sys.argv[2] + "r outfile_r {:f} {:f}".format(Kpix_deg, sample_rate))

        # Aggiunta: apertura automatica del prompt dei comandi
        project_dir = r"C:\Users\mbarbieri\PycharmProjects\RealterAnalysis"
        activate_script = os.path.join(project_dir, "venv", "Scripts", "activate.bat")
        cmd_left = f"remodnav --savgol-length {savgol:.6f} {sys.argv[2]}l outfile_l {Kpix_deg:.6f} {sample_rate:.6f}"
        cmd_right = f"remodnav --savgol-length {savgol:.6f} {sys.argv[2]}r outfile_r {Kpix_deg:.6f} {sample_rate:.6f}"
        full_command = f'cmd.exe /k "cd /d {project_dir} && call {activate_script} && {cmd_left} && {cmd_right}"'
        subprocess.Popen(full_command, shell=True)


# #DA USARE SE L'INPUT SONO GRADI
# if __name__ == '__main__':
#     if len(sys.argv) != 3:
#         print("Usage " + sys.argv[0] + " <infile> <outfile_prefix>")
#     else:
#         conv = DataProcessing(sys.argv[1])
#         data = conv.ImaokaConv()
#         write_remodnav_file(data[:-1], sys.argv[2])  # scrive i dati in gradi
#         sample_rate = calc_sample_rate(data[-1])
#         print("average sample rate: {:f}".format(sample_rate))
#         savgol = calc_min_savgol(sample_rate)
#         print("mininum savgol len: ~{:f}".format(savgol))
#         print("you may run e.g: remodnav --savgol-length {:f} ".format(savgol) +
#               sys.argv[2] + "<l/r> outfile {:f} {:f}".format(1.0, sample_rate))