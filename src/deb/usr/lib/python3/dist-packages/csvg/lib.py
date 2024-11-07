import subprocess
import sys
import z3

def get_float(
        model:z3.Model,
        variable:z3.Real,
) -> float:
    return float(model[variable].as_decimal(-1))


def svg_to_pdf(
        svg:str,
) -> str:
    command = [
        'inkscape',
        '--pipe',
        '--export-text-to-path',
        '--export-type', 'pdf',
        '--export-filename', '-',
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = process.communicate(input=svg.encode())
    return stdout
