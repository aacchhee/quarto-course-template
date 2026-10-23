"""Install this template's explicit reviewed native pack through its canonical installer."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=ROOT)
    args = parser.parse_args()
    project = args.project.resolve()
    if not project.is_dir():
        parser.error(f'project directory does not exist: {project}')
    refs = json.loads((ROOT / 'native-authoring-refs.json').read_text())
    expected = {'ctm-assessment', 'ctm-libs', 'ctm-checkers', 'math-exercise',
                'py-exercise', 'pyodide-interaktiv', 'jsxgraph'}
    if not isinstance(refs, dict) or set(refs) != expected or not all(isinstance(x, str) and re.fullmatch('[0-9a-f]{40}', x) for x in refs.values()):
        parser.error('native-authoring-refs.json must contain the seven exact reviewed commits')
    assessment = refs.pop('ctm-assessment')
    # A fresh temporary checkout cannot silently retain local changes or select main.
    with tempfile.TemporaryDirectory(prefix='ctm-native-authoring-') as folder:
        source = Path(folder)
        subprocess.run(['git', 'init', str(source)], check=True)
        subprocess.run(['git', '-C', str(source), 'fetch', '--depth=1',
                        'https://github.com/Erasmus-CTM/ctm-assessment.git', assessment], check=True)
        subprocess.run(['git', '-C', str(source), 'checkout', '--detach', 'FETCH_HEAD'], check=True)
        actual = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
        if actual != assessment:
            raise RuntimeError('canonical installer checkout differs from the reviewed commit')
        subprocess.run([sys.executable, str(source / 'scripts/install-project.py'),
                        '--project', str(project), '--review-refs', json.dumps(refs, sort_keys=True)], check=True)


if __name__ == '__main__':
    main()
