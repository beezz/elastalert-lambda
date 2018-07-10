import os
import datetime
import shlex

from elastalert import elastalert


def handler(event, context):
    print("Starting up ElastAlert")
    args = shlex.split(event.get('ARGS', os.getenv('ARGS', '')))

    if '--end' not in args:
        args.extend([
            '--end',
            datetime.datetime.utcnow().isoformat(),
        ])

    if '--config' not in args:
        args.extend(['--config', 'config.yaml'])

    print("Using arguments: `%s`" % args)
    elastalert.main(args)


if __name__ == "__main__":
    """
    Purely for local testing
    """
    import json
    import sys
    import select
    event = {}
    if select.select([sys.stdin,], [], [], 0.0)[0]:
        event = json.loads(sys.stdin.read())
    handler(event, None)
