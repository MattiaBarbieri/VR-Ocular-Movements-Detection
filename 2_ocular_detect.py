import math
import sys
import statistics
import numpy as np

def parse_remodnav_file(filepath):
    with open(filepath) as f:
        lines = f.readlines()
    hdr = lines[0].split('\t')
    return lines[1:], hdr

def extract_indices(hdr):
    return {
        'event': hdr.index('label'),
        'x1': hdr.index('start_x'),
        'y1': hdr.index('start_y'),
        'x2': hdr.index('end_x'),
        'y2': hdr.index('end_y'),
        'duration': hdr.index('duration'),
        'peak_vel': hdr.index('peak_vel'),
        'med_vel': hdr.index('med_vel'),
        'amp': hdr.index('amp'),
        'avg_vel': hdr.index('avg_vel\n')
    }

def process_events(lines, indices):
    K = 0.068055
    sacc_threshold = 2 / K
    fixa_threshold = 0.2

    macro_sacc_count = 0; macro_sacc_ampl = []; macro_sacc_ampl_deg = []; macro_sacc_duration = []; macro_sacc_peakvel = []; macro_sacc_medvel = []; macro_sacc_avgvel = []; macro_sacc_rawamp = []
    micro_sacc_count = 0; micro_sacc_ampl = []; micro_sacc_duration = []; micro_sacc_peakvel = []; micro_sacc_medvel = []; micro_sacc_avgvel = []
    purs_count = 0; purs_ampl = []; purs_ampl_deg = []; purs_duration = []; purs_peakvel = []; purs_medvel= []; purs_avgvel = []; purs_rawamp = []
    fixa_count = 0; fixa_ampl = []; fixa_ampl_deg = []; fixa_duration = []; fixa_peakvel = []; fixa_medvel = []; fixa_avgvel = []; fixa_rawamp = []
    fixa_duration_sum = 0

    for l in lines:
        data = l.split('\t')
        event_type = data[indices['event']]

        if event_type in ['SACC']:
            dx = float(data[indices['x1']]) - float(data[indices['x2']])
            dy = float(data[indices['y2']]) - float(data[indices['y2']])
            temp = abs(math.hypot(dx, dy))
            temp2 = temp * K

            if temp >= sacc_threshold:
                macro_sacc_count += 1
                macro_sacc_ampl.append(temp)
                macro_sacc_ampl_deg.append(temp2)
                macro_sacc_duration.append(float(data[indices['duration']]))
                macro_sacc_peakvel.append(float(data[indices['peak_vel']]))
                #macro_sacc_medvel.append(float(data[indices['med_vel']]))
                #macro_sacc_avgvel.append(float(data[indices['avg_vel']]))
                macro_sacc_rawamp.append(float(data[indices['amp']]))
            else:
                micro_sacc_count += 1
                micro_sacc_ampl.append(temp)
                micro_sacc_duration.append(float(data[indices['duration']]))
                micro_sacc_peakvel.append(float(data[indices['peak_vel']]))
                #micro_sacc_medvel.append(float(data[indices['med_vel']]))
                #micro_sacc_avgvel.append(float(data[indices['avg_vel']]))

        elif event_type in ['PURS']:
            dx = float(data[indices['x1']]) - float(data[indices['x2']])
            dy = float(data[indices['y2']]) - float(data[indices['y2']])
            temp = abs(math.hypot(dx,dy))
            temp2 = temp * K

            purs_count += 1
            purs_ampl.append(temp)
            purs_ampl_deg.append(temp2)
            purs_duration.append(float(data[indices['duration']]))
            purs_peakvel.append(float(data[indices['peak_vel']]))
            purs_medvel.append(float(data[indices['med_vel']]))
            purs_avgvel.append(float(data[indices['avg_vel']]))
            purs_rawamp.append(float(data[indices['amp']]))

        elif event_type in ['FIXA']:
            dx = float(data[indices['x1']]) - float(data[indices['x2']])
            dy = float(data[indices['y2']]) - float(data[indices['y2']])
            temp = abs(math.hypot(dx,dy))
            temp2 = temp * 0.056250
            temp3 = float(data[indices['duration']])

            if temp >= fixa_threshold:

                fixa_count += 1
                fixa_ampl.append(temp)
                fixa_ampl_deg.append(temp2)
                fixa_duration.append(float(data[indices['duration']]))
                fixa_peakvel.append(float(data[indices['peak_vel']]))
                fixa_medvel.append(float(data[indices['med_vel']]))
                fixa_avgvel.append(float(data[indices['avg_vel']]))
                fixa_rawamp.append(float(data[indices['amp']]))
                fixa_duration_sum += float(data[indices['duration']])

    return {
        'macro_sacc_count': macro_sacc_count,
        'macro_sacc_ampl': macro_sacc_ampl,
        'macro_sacc_ampl_deg': macro_sacc_ampl_deg,
        'macro_sacc_duration': macro_sacc_duration,
        'macro_sacc_peakvel': macro_sacc_peakvel,
        'macro_sacc_rawamp': macro_sacc_rawamp,
        'fixa_count': fixa_count,
        'fixa_duration': fixa_duration
    }

def compute_and_print_stats(data):
    mean_macro_sacc_ampl = np.mean(data['macro_sacc_ampl'])
    mean_macro_sacc_ampl_deg = np.mean(data['macro_sacc_ampl_deg'])
    mean_macro_sacc_duration = np.mean(data['macro_sacc_duration'])
    mean_macro_sacc_peakvel = np.mean(data['macro_sacc_peakvel'])
    mean_macro_sacc_rawamp = np.mean(data['macro_sacc_rawamp'])

    median_macro_sacc_ampl = np.median(data['macro_sacc_ampl'])
    median_macro_sacc_ampl_deg = np.median(data['macro_sacc_ampl_deg'])
    median_macro_sacc_duration = np.median(data['macro_sacc_duration'])
    median_macro_sacc_peakvel = np.median(data['macro_sacc_peakvel'])
    median_macro_sacc_rawampl = np.median(data['macro_sacc_rawamp'])

    sd_macro_sacc_ampl = statistics.stdev(data['macro_sacc_ampl'])
    sd_macro_sacc_ampl_deg = statistics.stdev(data['macro_sacc_ampl_deg'])
    sd_macro_sacc_duration = statistics.stdev(data['macro_sacc_duration'])
    sd_macro_sacc_peakvel = statistics.stdev(data['macro_sacc_peakvel'])
    sd_macro_sacc_rawamp = statistics.stdev(data['macro_sacc_rawamp'])

    mean_fixa_duration = np.mean(data['fixa_duration'])
    median_fixa_duration = np.median(data['fixa_duration'])
    sd_fixa_duration = statistics.stdev(data['fixa_duration'])

    print("Found: {:d} Macrosaccades (ampl: {:f} pixels (median: {:f}),(sd: {:f}) / {:f} degrees: (median: {:f}), (sd:{:f}), rawamp: {:f} (median: {:f}, (sd:{:f}); duration: {:f} (median: {:f}), (sd: {:f}); peak_vel: {:f} (median: {:f}), (sd: {:f}))".format(
        data['macro_sacc_count'],
        mean_macro_sacc_ampl, median_macro_sacc_ampl, sd_macro_sacc_ampl,
        mean_macro_sacc_ampl_deg, median_macro_sacc_ampl_deg, sd_macro_sacc_ampl_deg,
        mean_macro_sacc_rawamp, median_macro_sacc_rawampl, sd_macro_sacc_rawamp,
        mean_macro_sacc_duration, median_macro_sacc_duration, sd_macro_sacc_duration,
        mean_macro_sacc_peakvel, median_macro_sacc_peakvel, sd_macro_sacc_peakvel
    ))

    print("Found: {:d} Fixations (duration: {:f} (median: {:f}), (sd: {:f}))".format(
        data['fixa_count'],
        mean_fixa_duration, median_fixa_duration, sd_fixa_duration
    ))

def main():
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " <remodnav_out_file>")
        exit(1)

    lines, hdr = parse_remodnav_file(sys.argv[1])
    indices = extract_indices(hdr)
    data = process_events(lines, indices)
    compute_and_print_stats(data)

if __name__ == "__main__":
    main()
