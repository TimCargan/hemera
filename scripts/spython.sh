#!/bin/bash

# run [--slurm opts] pythonfile [args]
# Extract any slurm options if there are any

OP1=$1
SOPTS=""

if [[ $OP1 == "-"* ]]; then
  SOPTS=$OP1
  shift 1
  echo "sbatch with opts - $SOPTS"
fi

COMMAND=$1
echo $COMMAND
shift 1

CMD_FILE=`basename $COMMAND .py`


OUTPUT_FILE="$CMD_FILE-%J.out"

RES=$(sbatch --parsable --output "$OUTPUT_FILE" --job-name "$CMD_FILE" $SOPTS ~/bin/rsbatch.sh "$COMMAND" "$@")

echo "Will read from file: $CMD_FILE-$RES.out"
sleep 10
tail -f "$CMD_FILE-$RES.out"