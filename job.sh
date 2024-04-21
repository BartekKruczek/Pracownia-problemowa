#!/bin/bash
#SBATCH --job-name=Test
#SBATCH --time=00:15:00
#SBATCH --account=plgexaile2-gpu-a100
#SBATCH --partition=plgrid-gpu-a100
#SBATCH --cpus-per-task=1
#SBATCH --mem=2GB
#SBATCH --gres=gpu

source /net/pr2/projects/plgrid/plgglemkin/isap/.venv/bin/activate
cd /net/pr2/projects/plgrid/plgglemkin/isap
python3 main.py