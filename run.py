import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description='Experimento de subsecuencia común más larga')
    parser.add_argument('--report-only', action='store_true', help='Regenera las gráficas con los datos guardados')
    args = parser.parse_args()

    os.environ['MPLCONFIGDIR'] = str(ROOT / '.mplconfig')
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    sys.dont_write_bytecode = True
    sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'benchmarks')]

    from benchmark_output import capture_environment, write_outputs

    if not args.report_only:
        env = os.environ.copy()
        env['PYTHONPATH'] = str(ROOT / 'src')
        subprocess.run(
            [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'],
            cwd=ROOT, env=env, check=True,
        )
        from benchmark import run
        from generate_cases import generate

        capture_environment(ROOT)
        cases = generate(ROOT)
        run(cases)

    write_outputs(ROOT)


if __name__ == '__main__':
    main()
