# !/usr/bin/env python

import argparse
import json
import os
import sys
from datetime import datetime

DATE_FORMAT = '%l:%M%p %Z on %b %d, %Y'
HOME = os.path.expanduser("~")
PUSHIT_HOME = os.path.join(HOME, '.minion')

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='commands')

# init
init_parser = subparsers.add_parser('init', help='initialize empty bucket')
init_parser.add_argument(
    '--force', '-f', action='store_true', help='forcefully reinitialize'
)

# add
add_parser = subparsers.add_parser('add', help='add a task to bucket')
add_parser.add_argument('name', help='name of the task')
add_parser.add_argument('-d', '--desc', help='description of the task')


# list
list_parser = subparsers.add_parser('list', help='add a task to bucket')
list_parser.add_argument('status', choices=['open', 'closed'])


# close
close_parser = subparsers.add_parser('close', help='close a task in bucket')
close_parser.add_argument('name', help='name of the task')


def _load_data():
    location = os.path.join(PUSHIT_HOME, 'db.json')
    data = json.load(open(location, 'r'))
    return data


def _dump_data(data):
    location = os.path.join(PUSHIT_HOME, 'db.json')
    json.dump(data, open(location, 'w'))


def init(args):
    if not os.path.isdir(PUSHIT_HOME):
        os.mkdir(PUSHIT_HOME)
        _dump_data([])
    elif args.force:
        _dump_data([])
    else:
        print('minions already loaded')
    return


def add_task(args):
    data = _load_data()
    task_data = {
        'name': args.name,
        'desc': args.desc,
        'status': 'open',
        'open_date': datetime.now().strftime(DATE_FORMAT),
        'closed_date': None
    }
    data.append(task_data)
    _dump_data(data)
    return


def close_task(args):
    data = _load_data()
    for item in data:
        if item['name'] == args.name:
            item['status'] = 'closed'
            item['closed_date'] = datetime.now().strftime(DATE_FORMAT)
    _dump_data(data)
    return


def list_tasks(args):
    data = _load_data()
    tasks = []
    for item in data:
        if item['status'] == args.status:
            tasks.append(item)
    for item in tasks:
        print('{0} - {1} - {2} - {3}\n'.format(
            item['name'], item['desc'], item['open_date'], item['closed_date']
        ))


def handler(action, args):
    if action == 'init':
        init(args)
    if action == 'add':
        add_task(args)
    if action == 'list':
        list_tasks(args)
    if action == 'close':
        close_task(args)


if __name__ == "__main__":
    action = sys.argv[1]
    args = parser.parse_args()
    handler(action, args)
