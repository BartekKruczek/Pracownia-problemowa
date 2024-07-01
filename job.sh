#!/bin/bash
#SBATCH --job-name=Test
#SBATCH --time=24:00:00
#SBATCH --account=plgexaile2-gpu-a100
#SBATCH --partition=plgrid-gpu-a100
#SBATCH --cpus-per-task=4
#SBATCH --mem=10GB
#SBATCH --gres=gpu

module load GCCcore/10.3.0 tesseract/5.4.1
source /net/pr2/projects/plgrid/plgglemkin/isap/Pracownia-problemowa/.venv/bin/activate
cd /net/pr2/projects/plgrid/plgglemkin/isap/Pracownia-problemowa
python3 main.py