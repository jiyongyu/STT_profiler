#/bin/bash

source /shared/Jiyong/SPEC2006/shrc
go $1 run
cd run_base_ref_x86_64.0000
objdump -ld -C $1_base.x86_64 > /shared/Jiyong/SPEC2006/benchspec/CPU2006/profile/$1.S
