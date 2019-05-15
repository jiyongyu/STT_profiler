#!/usr/bin/env python

import os

specout_dir = "/home/jiyongy2/STT_ISCA19/STT_gem5/output/outputs/real-sim/SPEC2006/"
profile_dir = "/shared/Jiyong/SPEC2006/benchspec/CPU2006/profile/"

ignore = ['lbm', 'sphinx3']

for dr in os.listdir(specout_dir):
    if "TSO-SafeFence-Spectre-DDIFT-Lazy-TransType0" in dr:
        bcmk_name = dr.split('-')[0]
        print bcmk_name

        if bcmk_name in ignore:
            continue

        delay_count = {}
        with open(specout_dir + dr + '/condor.output', 'r') as gem5_outfile:
            for line in gem5_outfile:
                if "cycle:" in line:
                    delay_count = {}
                if "addr" in line and "delayed_cycles" in line:
                    addr = (line.split()[1])[:-1]
                    cycles = int(line.split()[-1])
                    delay_count[addr] = cycles

        total_cycles = 0
        for i, val in delay_count.items():
            if val >= 0:
                total_cycles += val

        sorted_delay_count = sorted(delay_count.items(), key=lambda x: x[1], reverse=True)

        # create profile
        profile_name = bcmk_name + '.profile'
        with open(profile_dir + profile_name, 'w') as profile:
            for val in sorted_delay_count:
                profile.write("%s, %d, %.3f%%\n" % (val[0], val[1], float(val[1])*100 / total_cycles))

        # create assembly file
        asmfile_name = bcmk_name + '.S'
        os.system('./generate_asm.sh ' + bcmk_name + ' ' + profile_dir)

        # create annotate assembly file
        annotate_asmfile_name = bcmk_name + '.S.annotate'
        with open(profile_dir + annotate_asmfile_name, 'w') as new_asmfile:
            with open(profile_dir + asmfile_name, 'r') as asmfile:
                for line in asmfile:
                    if ':' not in line:
                        new_asmfile.write(line)
                    elif line[0] != ' ' or line[8] != ':':
                        new_asmfile.write(line)
                    else:
                        pc = (line.split()[0])[:-1]
                        if pc in delay_count:
                            if float(delay_count[pc]) / total_cycles > 0.01:
                                percent = "@{:.3%}".format(float(delay_count[pc]) / total_cycles)
                                line = percent + ' ' + line[2:]
                        new_asmfile.write(line)
