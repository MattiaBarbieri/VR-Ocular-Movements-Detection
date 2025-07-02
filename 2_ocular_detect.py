#!/usr/bin/python3
import math
import sys
import statistics
import numpy as np

K = 0.068055
sacc_threshold = 1/K # 1 degree


macro_sacc_count = 0; macro_sacc_ampl = []; macro_sacc_ampl_deg = []; macro_sacc_duration = []; macro_sacc_peakvel = []; macro_sacc_medvel = [];  macro_sacc_avgvel = []; macro_sacc_rawamp = []
micro_sacc_count = 0; micro_sacc_ampl = []; micro_sacc_duration = []; micro_sacc_peakvel = []; micro_sacc_medvel = []; micro_sacc_avgvel = []
purs_count = 0; purs_ampl = []; purs_ampl_deg = []; purs_duration = []; purs_peakvel = []; purs_medvel= []; purs_avgvel = []; purs_rawamp = []
fixa_count = 0; fixa_ampl = []; fixa_ampl_deg = []; fixa_duration = []; fixa_peakvel = []; fixa_medvel = []; fixa_avgvel = []; fixa_rawamp = []

fixa_duration_sum = 0

if (len(sys.argv) != 2):
    print("Usage: " + sys.argv[0] + " <remodnav_out_file>")
    exit(1)

with open(sys.argv[1]) as f:
    lines = f.readlines()
    hdr = lines[0].split('\t')
    event = hdr.index('label')
    x1 = hdr.index('start_x')
    y1 = hdr.index('start_y')
    x2 = hdr.index('end_x')
    y2 = hdr.index('end_y')
    duration = hdr.index('duration')
    peak_vel = hdr.index('peak_vel')
    med_vel = hdr.index('med_vel')
    amp = hdr.index('amp')
    avg_vel = hdr.index('avg_vel\n')

    for l in lines[1:]:
        data = l.split('\t')
        event_type = data[event]

        if event_type in ['SACC']:
            dx = float(data[x1]) - float(data[x2])
            dy = float(data[y2]) - float(data[y2])
            temp = abs(math.hypot(dx, dy))
            temp2 = temp * K
            # sacc_count += 1
            # sacc_ampl += temp
            # sacc_ampl.append(temp)

            if temp >= sacc_threshold:
                macro_sacc_count += 1
                macro_sacc_ampl.append(temp)
                macro_sacc_ampl_deg.append(temp2)
                macro_sacc_duration.append(float(data[duration]))
                macro_sacc_peakvel.append(float(data[peak_vel]))
                #macro_sacc_medvel.append(float(data[med_vel]))
                #macro_sacc_avgvel.append(float(data[avg_vel]))
                macro_sacc_rawamp.append(float(data[amp]))
            else:
                micro_sacc_count += 1
                micro_sacc_ampl.append(temp)
                micro_sacc_duration.append(float(data[duration]))
                micro_sacc_peakvel.append(float(data[peak_vel]))
                #micro_sacc_medvel.append(float(data[med_vel]))
                #micro_sacc_avgvel.append(float(data[avg_vel]))

        elif event_type in ['PURS']:

            dx = float(data[x1]) - float(data[x2])
            dy = float(data[y2]) - float(data[y2])
            temp = abs(math.hypot(dx,dy))
            temp2 = temp * K

            purs_count += 1
            purs_ampl.append(temp)
            purs_ampl_deg.append(temp2)
            purs_duration.append(float(data[duration]))
            purs_peakvel.append(float(data[peak_vel]))
            purs_medvel.append(float(data[med_vel]))
            purs_avgvel.append(float(data[avg_vel]))
            purs_rawamp.append(float(data[amp]))


        elif event_type in ['FIXA']:

            dx = float(data[x1]) - float(data[x2])
            dy = float(data[y2]) - float(data[y2])
            temp = abs(math.hypot(dx,dy))
            temp2 = temp * 0.056250

            fixa_count += 1
            fixa_ampl.append(temp)
            fixa_ampl_deg.append(temp2)
            fixa_duration.append(float(data[duration]))
            fixa_peakvel.append(float(data[peak_vel]))
            fixa_medvel.append(float(data[med_vel]))
            fixa_avgvel.append(float(data[avg_vel]))
            fixa_rawamp.append(float(data[amp]))
            fixa_duration_sum += float(data[duration])


    # MACROSACCADES RESULTS
    # Calculate mean
    # macro_sacc_ampl /= macro_sacc_count
    mean_macro_sacc_ampl = np.mean(macro_sacc_ampl)
    mean_macro_sacc_ampl_deg = (np.mean(macro_sacc_ampl_deg))
    mean_macro_sacc_duration = np.mean(macro_sacc_duration)
    mean_macro_sacc_peakvel = np.mean(macro_sacc_peakvel)
    #mean_macro_sacc_medvel = np.mean(macro_sacc_medvel)
    #mean_macro_sacc_avgvel = np.mean(macro_sacc_avgvel)
    mean_macro_sacc_rawamp = np.mean(macro_sacc_rawamp)

    # Calculate median
    median_macro_sacc_ampl = np.median(macro_sacc_ampl)
    median_macro_sacc_ampl_deg = np.median(macro_sacc_ampl_deg)
    median_macro_sacc_duration = np.median(macro_sacc_duration)
    median_macro_sacc_peakvel = np.median(macro_sacc_peakvel)
    #median_macro_sacc_medvel = np.median(macro_sacc_medvel)
    #median_macro_sacc_avgvel = np.median(macro_sacc_avgvel)
    median_macro_sacc_rawampl = np.median(macro_sacc_rawamp)

    # Calculate standard deviation
    sd_macro_sacc_ampl = statistics.stdev(macro_sacc_ampl)
    sd_macro_sacc_ampl_deg = statistics.stdev(macro_sacc_ampl_deg)
    sd_macro_sacc_duration = statistics.stdev(macro_sacc_duration)
    sd_macro_sacc_peakvel = statistics.stdev(macro_sacc_peakvel)
    #sd_macro_sacc_medvel = statistics.stdev(macro_sacc_medvel)
    #sd_macro_sacc_avgvel = statistics.stdev(macro_sacc_avgvel)
    sd_macro_sacc_rawamp = statistics.stdev(macro_sacc_rawamp)



    # FIXATION RESULTS
    # Calculate mean
    mean_fixa_duration = np.mean(fixa_duration)

    # Calculate median
    median_fixa_duration = np.median(fixa_duration)

    # Calculate standard deviation
    sd_fixa_duration = statistics.stdev(fixa_duration)



    print("Found: {:d} Macrosaccades (ampl: {:f} pixels (median: {:f}),(sd: {:f}) / {:f} degrees: (median: {:f}), (sd:{:f}), rawamp: {:f} (median: {:f}, (sd:{:f}); duration: {:f} (median: {:f}), (sd: {:f}); peak_vel: {:f} (median: {:f}), (sd: {:f}))".format
        (macro_sacc_count,
        mean_macro_sacc_ampl, median_macro_sacc_ampl, sd_macro_sacc_ampl,
        mean_macro_sacc_ampl_deg, median_macro_sacc_ampl_deg, sd_macro_sacc_ampl_deg,
        mean_macro_sacc_rawamp, median_macro_sacc_rawampl, sd_macro_sacc_rawamp,
        mean_macro_sacc_duration, median_macro_sacc_duration, sd_macro_sacc_duration,
        mean_macro_sacc_peakvel, median_macro_sacc_peakvel, sd_macro_sacc_peakvel))


    print("Found: {:d} Fixations (duration: {:f} (median: {:f}), (sd: {:f}))".format
       (fixa_count,
       mean_fixa_duration, median_fixa_duration, sd_fixa_duration))


    # ########## WRITE RESULTS ON A TXT FILE ##########
    with open("Dati.txt", "a") as f:
        # Scrivi intestazione solo se il file è vuoto
        if f.tell() == 0:
            f.write("NAME\tTASK\tCONDITION\t"
                    "Sacc_N\t"
                    "Sacc_amp_pix_mean\tSacc_amp_pix_med\tSacc_amp_pix_sd\t"
                    "Sacc_amp_deg_mean\tSacc_amp_deg_med\tSacc_amp_deg_sd\t"
                    "Sacc_raw_amp_mean\tSacc_raw_amp_med\tSacc_raw_amp_sd\t"
                    "Sacc_dur_mean\tSacc_dur_med\tSacc_dur_sd\t"
                    "Sacc_peakvel_mean\tSacc_peakvel_med\tSacc_peakvel_sd\t"
                    "Fixa_N\t"
                    "Fixa_dur_mean\tFixa_dur_med\tFixa_dur_sd\n")

        # Scrivi i dati
        f.write("LO\tS1\tNV\t"
                "{:.3f}\t"
                "{:.3f}\t{:.3f}\t{:.3f}\t"
                "{:.3f}\t{:.3f}\t{:.3f}\t"
                "{:.3f}\t{:.3f}\t{:.3f}\t"
                "{:.3f}\t{:.3f}\t{:.3f}\t"
                "{:.3f}\t{:.3f}\t{:.3f}\t"
                
                "{:.3f}\t"
                "{:.3f}\t{:.3f}\t{:.3f}\n".format(
            macro_sacc_count,
            mean_macro_sacc_ampl, median_macro_sacc_ampl, sd_macro_sacc_ampl,
            mean_macro_sacc_ampl_deg, median_macro_sacc_ampl_deg, sd_macro_sacc_ampl_deg,
            mean_macro_sacc_rawamp, median_macro_sacc_rawampl, sd_macro_sacc_rawamp,
            mean_macro_sacc_duration, median_macro_sacc_duration, sd_macro_sacc_duration,
            mean_macro_sacc_peakvel, median_macro_sacc_peakvel, sd_macro_sacc_peakvel,
            fixa_count,
            mean_fixa_duration, median_fixa_duration, sd_fixa_duration
        ))
