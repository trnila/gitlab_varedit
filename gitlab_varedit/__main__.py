import argparse
import os
import tempfile
from subprocess import call

import gitlab
from gitlab_varedit.parser import create, parse, diff


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('project_id')
    args = parser.parse_args()

    gl = gitlab.Gitlab.from_config()

    project = gl.projects.get(id=args.project_id)
    before = {var.key: var.value for var in project.variables.list(all=True)}

    EDITOR = os.environ.get('EDITOR', 'vim')
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(create(before).encode('utf-8'))
        tf.flush()
        call([EDITOR, tf.name])

        tf.seek(0)
        edited_message = tf.read()
        after = parse(edited_message.decode('utf-8'))
        data = diff(before, after)

        for var in data['delete']:
            project.variables.delete(var)

        for var in data['add']:
            project.variables.create({'key': var, 'value': after[var]})

        for var in data['update']:
            item = project.variables.get(var)
            item.value = after[var]
            item.save()
