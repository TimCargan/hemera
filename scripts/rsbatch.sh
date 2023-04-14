#!/bin/bash
#SBATCH

# Log to squeue - custom to my slurm cluster see Arron Jacksons github for info
source /usr2/share/gpu.sbatch

COMMAND=$1
echo $COMMAND

CMD_FILE=`basename $COMMAND .py`
echo $CMD_FILE

TS=$(date +"%Y%m%dT%H%M")
OUT_BASE_DIR=${TS}-${CMD_FILE}
hostname


# Shift command over
shift 1
python "$COMMAND" "$@"

#wait

# Send notification
IFTTT_KEY=$(< %%% path/to/ifttt.key %%%)
msg_format='{"value1":"Exper Done!", "value2": "%s is done!"}'
msg="$(printf "$msg_format" $SLURM_JOB_NAME)"
echo $msg
curl -X POST -H "Content-Type: application/json" -d "${msg}" https://maker.ifttt.com/trigger/exper_done/with/key/$IFTTT_KEY

echo "All done"