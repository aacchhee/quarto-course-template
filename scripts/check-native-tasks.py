"""Bounded installed task proof; synthetic content, no teaching decisions."""
import argparse
import hashlib
import json
import pathlib
import re
import select
import subprocess
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=pathlib.Path, required=True)
    parser.add_argument('--prepare', action='store_true')
    args = parser.parse_args()
    project = args.project.resolve()
    tasks = json.loads((ROOT / '.vscode/tasks.json').read_text())
    expected = [
        ('CTM: Review variants', 'variants-review.py', []),
        ('CTM: Check variants (resolve proposals)', 'question-variants.py', ['review']),
    ]
    for task, (label, script, suffix) in zip(tasks['tasks'], expected, strict=True):
        assert task['label'] == label and task['type'] == 'process'
        assert task['command'] == '${input:ctmPython}'
        assert task['args'] == [f'${{workspaceFolder}}/_extensions/math-exercise/{script}',
            '--project', '${workspaceFolder}', '--file', '${relativeFile}',
            '--label', '${input:ctmVariantLabel}', *suffix]
        assert task['options']['cwd'] == '${workspaceFolder}'
    assert {x['id'] for x in tasks['inputs']} == {'ctmPython', 'ctmVariantLabel'}
    source = project / 'pages' / 'native task proof.qmd'
    if args.prepare:
        source.parent.mkdir(parents=True)
        (project / '_quarto.yml').write_text('project:\n  type: website\n')
        source.write_text('''```{math-exercise}
#| label: template-task-proof
#| variables: |
#|   a = pick(1, 1)
#| field-labels: Answer
#| note: synthetic template a={#a#}
#| tests:
#|   - name: zero is wrong
#|     answers:
#|       Answer: '0'
#|     expect: wrong
Enter $a={@a@}$: _[{#a#}].
```
''')
        return
    evidence = project / 'proof-evidence'
    evidence.mkdir()
    def command(task):
        replacements = {'${workspaceFolder}': str(project), '${relativeFile}': str(source.relative_to(project)),
                        '${input:ctmVariantLabel}': 'template-task-proof'}
        result = []
        for arg in task['args']:
            for key, value in replacements.items():
                arg = arg.replace(key, value)
            result.append(arg)
        return [sys.executable, *result]
    def run(cmd):
        return subprocess.run(cmd, cwd=project, check=True, capture_output=True, text=True, timeout=90)
    generated = run(command(tasks['tasks'][1])[:-1] + ['generate25more'])
    (evidence / 'generated.json').write_text(generated.stdout)
    manifest = project / '_variants/template-task-proof.yml'
    original = manifest.read_bytes()
    history = json.loads(original)
    assert history['decisions'] == [] and history['events'] == []
    result = run(command(tasks['tasks'][1]))
    (evidence / 'resolved.json').write_text(result.stdout)
    records = json.loads(result.stdout)['records']
    assert len(records) == 1
    assert records[0]['tests']['passed'] is True
    assert records[0]['tests']['teacher']['passed'] is True
    assert records[0]['tests']['tests'][0]['passed'] is True
    assert records[0].get('n') is None
    assert manifest.read_bytes() == original
    helper = subprocess.Popen(command(tasks['tasks'][0]) + ['--no-browser'], cwd=project,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)
    try:
        deadline = time.monotonic() + 30
        url = None
        while time.monotonic() < deadline:
            if helper.poll() is not None:
                raise AssertionError(helper.stderr.read())
            ready, _, _ = select.select([helper.stdout], [], [], .2)
            if ready:
                match = re.search(r'http://127\.0\.0\.1:\d+/[^\s]+/', helper.stdout.readline())
                if match:
                    url = match.group()
                    break
        assert url, 'helper did not advertise its loopback URL'
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(url, timeout=60) as response:
            assert response.status == 200
            html = response.read()
        assert b'template-task-proof' in html and b'html' in html.lower()
        (evidence / 'helper.html').write_bytes(html)
        assert manifest.read_bytes() == original
    finally:
        helper.terminate()
        try:
            helper.wait(timeout=10)
        except subprocess.TimeoutExpired:
            helper.kill()
            helper.wait()
    (evidence / 'summary.json').write_text(json.dumps({'records': 1, 'teacherPassed': True,
        'authoredTestsPassed': 1, 'approvals': 0, 'manifestUnchanged': True,
        'manifestSHA256': hashlib.sha256(original).hexdigest(), 'helperGET': 200}, indent=2))
    print('PASS: installed process task arguments, real tests, read-only manifest and helper GET')


if __name__ == '__main__':
    main()
