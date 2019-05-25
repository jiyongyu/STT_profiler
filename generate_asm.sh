#/bin/bash

SPEC2006_DIR=/shared/Jiyong/SPEC2006
source $SPEC2006_DIR/shrc
go $1 run
cd run_base_ref_x86_64.0000
objdump -ld -C $1_base.x86_64 > $2/$1.S
