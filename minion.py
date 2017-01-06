# !/usr/bin/env python

import argparse
import json
import os
import sys
from datetime import datetime

DATE_FORMAT = '%l:%M%p %Z on %b %d, %Y'
HOME = os.path.expanduser("~")
MINION_HOME = os.path.join(HOME, '.minion')

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='commands')


# init
init_parser = subparsers.add_parser('init', help='initialize minions')


# create bucket
create_parser = subparsers.add_parser('create', help='create empty bucket')
create_parser.add_argument('name', help='name of the bucket')


# delete bucket
delete_parser = subparsers.add_parser('delete', help='delete a bucket')
delete_parser.add_argument('name', help='name of the bucket')


# add task
add_parser = subparsers.add_parser('add', help='add a task to bucket')
add_parser.add_argument('bucket', help='name of the bucket')
add_parser.add_argument('name', help='name of the task')
add_parser.add_argument('-d', '--desc', help='description of the task')


# list tasks
list_parser = subparsers.add_parser('list', help='list the tasks from bucket')
list_parser.add_argument('bucket', help='name of the bucket')
list_parser.add_argument('-s', '--status', choices=['open', 'closed'])


# close task
close_parser = subparsers.add_parser('close', help='close a task in bucket')
close_parser.add_argument('bucket', help='name of the bucket')
close_parser.add_argument('name', help='name of the task')


def _load_data(bucket):
    location = os.path.join(MINION_HOME, '{0}.json'.format(bucket))
    if os.path.isfile(location):
        data = json.load(open(location, 'r'))
        return data
    return None


def _dump_data(data, bucket):
    location = os.path.join(MINION_HOME, '{0}.json'.format(bucket))
    json.dump(data, open(location, 'w'))


def _pretty_print(data):
    print('status | task | description | start date | end date\n')
    for item in data:
        mark = 'X' if item.get('closed_date') else ''
        print('[ {0} ] | {1} | {2} | {3} | {4}\n'.format(
            mark, item.get('name'), item.get('desc'),
            item.get('open_date'), item.get('closed_date', 'NA')
        ))


def init():
    if not os.path.isdir(MINION_HOME):
        os.mkdir(MINION_HOME)
    else:
        print('minions already loaded')
    return


def create_bucket(args):
    if not os.path.isdir(MINION_HOME):
        print('run init first')
    else:
        _dump_data([], args.name)
    return


def delete_bucket(args):
    if not os.path.isdir(MINION_HOME):
        print('run init first')
    else:
        location = os.path.join(MINION_HOME, '{0}.json'.format(args.name))
        os.remove(location)
    return


def add_task(args):
    data = _load_data(args.bucket)
    if data is None:
        print('create bucket first')
    else:
        task_data = {
            'name': args.name,
            'desc': args.desc,
            'status': 'open',
            'open_date': datetime.now().strftime(DATE_FORMAT)
        }
        data.append(task_data)
        _dump_data(data, args.bucket)
    return


def close_task(args):
    data = _load_data(args.bucket)
    if data is None:
        print('create bucket first')
    else:
        for item in data:
            if item['name'] == args.name:
                item['status'] = 'closed'
                item['closed_date'] = datetime.now().strftime(DATE_FORMAT)
        _dump_data(data, args.bucket)
    return


def list_tasks(args):
    data = _load_data(args.bucket)
    if data is None:
        print('create bucket first')
    else:
        if args.status:
            tasks = []
            for item in data:
                if item['status'] == args.status:
                    tasks.append(item)
            _pretty_print(tasks)
        else:
            _pretty_print(data)


def handler(action, args):
    if action == 'init':
        init()
    if action == 'create':
        create_bucket(args)
    if action == 'delete':
        delete_bucket(args)
    if action == 'add':
        add_task(args)
    if action == 'list':
        list_tasks(args)
    if action == 'close':
        close_task(args)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        action = sys.argv[1]
        args = parser.parse_args()
        handler(action, args)
