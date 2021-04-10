#!/bin/bash
#SBATCH -N 1
#SBATCH -p GPU-shared
#SBATCH -t 5:00:00
#SBATCH --ntasks-per-node 32

cd $SCRATCH

cp /jet/home/cpp5231/multioutput.py .

cp /jet/home/cpp5231/finalDataFrame.csv .

module load anaconda3/2020.11

python multioutput.py --output output.data

cp output.data /jet/home/cpp5231