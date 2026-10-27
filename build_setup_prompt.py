#!/usr/bin/env python3
"""Refresh the appendices in setup_prompt.md from the files they copy.

setup_prompt.md is what people paste into Claude, so it carries full copies of
the templates, the playbook, bake.py, and dashboard.html. Edit those files, then
run this to bring the copies back in sync:

    python3 build_setup_prompt.py           # rewrite setup_prompt.md
    python3 build_setup_prompt.py --check   # exit 1 if setup_prompt.md is out of date
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
PROMPT = HERE / 'setup_prompt.md'
FENCE = '````'  # four backticks, so the ``` blocks inside the files stay intact
LANG = {'.md': 'markdown', '.py': 'python', '.html': 'html'}
APPENDIX = re.compile(r'(<!-- appendix: (?P<name>[\w.-]+) -->\n)(.*?)(<!-- /appendix -->)', re.DOTALL)


def fenced(name):
    path = HERE / name
    if not path.exists():
        sys.exit(f'error: setup_prompt.md names {name}, which does not exist.')
    text = path.read_text(encoding='utf-8').rstrip()
    if any(line.startswith(FENCE) for line in text.splitlines()):
        sys.exit(f'error: {name} has a line starting with {FENCE}, which would end its appendix early.')
    return f'{FENCE}{LANG.get(path.suffix, "")}\n{text}\n{FENCE}\n'


def main():
    source = PROMPT.read_text(encoding='utf-8')
    names = []

    def fill(m):
        names.append(m.group('name'))
        return m.group(1) + fenced(m.group('name')) + m.group(4)

    built = APPENDIX.sub(fill, source)
    if not names:
        sys.exit('error: no <!-- appendix: file --> markers found in setup_prompt.md.')

    if '--check' in sys.argv[1:]:
        if built != source:
            sys.exit('setup_prompt.md is out of date. Run: python3 build_setup_prompt.py')
        print(f'setup_prompt.md is current ({len(names)} appendices).')
        return

    # newline='\n' keeps LF endings on Windows, so the prompt doesn't churn in git.
    with open(PROMPT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(built)
    print(f'Rebuilt {len(names)} appendices: {", ".join(names)}')


if __name__ == '__main__':
    main()
