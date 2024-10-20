#!/bin/bash
#SBATCH --job-name=7B-AWQ
#SBATCH --time=01:00:00
#SBATCH --account=plgexaile2-gpu-a100
#SBATCH --partition=plgrid-gpu-a100
#SBATCH --cpus-per-task=8
#SBATCH --mem=40GB
#SBATCH --gres=gpu

module load GCCcore/10.3.0 tesseract/5.4.1 CUDA/12.4.0
source /net/pr2/projects/plgrid/plgglemkin/isap/Pracownia-problemowa/.venv/bin/activate
cd /net/pr2/projects/plgrid/plgglemkin/isap/Pracownia-problemowa
python3 main.py