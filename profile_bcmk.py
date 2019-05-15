#!/usr/bin/env python

benchmarks = ['bzip2', 'astar', 'calculix']
number = {}
number['astar'] = 473
number['bzip2'] = 401
number['calculix'] = 454

NUM_INSTR = '1B'

def profile(OUT_FILE, PROFILE_FILE, ASM_FILE, ANNOTATED_ASM_FILE):
    delay_count = {}
    with open(OUT_FILE, 'r') as gem5_outfile:
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
    with open(PROFILE_FILE, 'w') as profile_file:
        for val in sorted_delay_count:
            profile_file.write("%s, %d, %.3f%%\n" % (val[0], val[1], float(val[1])*100 / total_cycles))

    # create annotated assembly file
    with open(ANNOTATED_ASM_FILE, 'w') as new_asm_file:
        with open(ASM_FILE, 'r') as asm_file:
            for line in asm_file:
                if ':' not in line:
                    new_asm_file.write(line)
                elif line[0] != ' ' or line[8] != ':':
                    new_asm_file.write(line)
                else:
                    pc = (line.split()[0])[:-1]
                    if pc in delay_count:
                        if float(delay_count[pc]) / total_cycles > 0.01:
                            percent = "@{:.3%}".format(float(delay_count[pc]) / total_cycles)
                            line = percent + ' ' + line[2:]
                    new_asm_file.write(line)

for bcmk in benchmarks:
    profile("/shared/Jiyong/SPEC2006/benchspec/CPU2006/" + str(number[bcmk]) + "." + bcmk + "/run/run_base_ref_x86_64.0000/out_stt_" + NUM_INSTR,
            bcmk + ".profile",
            bcmk + ".S",
            bcmk + ".S.annotate")
