# !/usr/bin/env python

import argparse
import os
import sys
from datetime import datetime

import bucket as task_bucket

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='commands')


# create bucket
create_parser = subparsers.add_parser('create', help='create empty bucket')
create_parser.add_argument('name', help='name of the bucket')


# delete bucket
delete_parser = subparsers.add_parser('delete', help='delete a bucket')
delete_parser.add_argument('name', help='name of the bucket')


# rename bucket
rename_parser = subparsers.add_parser('rename', help='rename a bucket')
rename_parser.add_argument('name', help='name of the bucket')
rename_parser.add_argument('new', help='new name of the bucket')


# add task
add_parser = subparsers.add_parser('add', help='add a task to bucket')
add_parser.add_argument('bucket', help='name of the bucket')
add_parser.add_argument('name', help='name of the task')
add_parser.add_argument('-t', '--tags', nargs='+', default=[], help='tags for the task')


# close task
close_parser = subparsers.add_parser('close', help='close the task from bucket')
close_parser.add_argument('bucket', help='name of the bucket')
close_parser.add_argument('name', help='name of the task')


# list tasks
list_parser = subparsers.add_parser('list', help='list the tasks from bucket')
list_parser.add_argument('bucket', help='name of the bucket')
list_parser.add_argument('-s', '--status', choices=['new', 'closed'], help='filter by status')
list_parser.add_argument('-t', '--tag', help='filter by a tag')


# edit task
edit_parser = subparsers.add_parser('edit', help='edit a task from bucket')
edit_parser.add_argument('bucket', help='name of the bucket')
edit_parser.add_argument('name', help='name of the task')
edit_parser.add_argument('-n', '--new', help='new name of the task')
edit_parser.add_argument('-a', '--addtags', nargs='+', default=[], help='add tags to the task')
edit_parser.add_argument('-r', '--removetags', nargs='+', default=[], help='remove tags from the task')


# remove task
remove_parser = subparsers.add_parser('remove', help='remove a task from bucket')
remove_parser.add_argument('bucket', help='name of the bucket')
remove_parser.add_argument('name', help='name of the task')


def init():
    if not os.path.isdir(task_bucket.MINION_HOME):
        os.mkdir(task_bucket.MINION_HOME)
    return


def handler(action, args):
    init()  # make sure minions are loaded prior to handling any request
    if action == 'create':
        bucket = task_bucket.Bucket(args.name)
        bucket.create()
    if action == 'delete':
        bucket = task_bucket.Bucket(args.name)
        bucket.delete()
    if action == 'rename':
        bucket = task_bucket.Bucket(args.name)
        bucket.rename(args.new)
    if action == 'add':
        bucket = task_bucket.Bucket(args.bucket)
        data = {
            'name': args.name,
            'tags': args.tags,
            'status': 'new',
            'added_date': datetime.now().strftime(task_bucket.DATE_FORMAT)
        }
        bucket.add_task(data)
    if action == 'list':
        bucket = task_bucket.Bucket(args.bucket)
        status = args.status
        tag = args.tag
        bucket.list_task(status, tag)
    if action == 'close':
        bucket = task_bucket.Bucket(args.bucket)
        bucket.close_task(args.name)
    if action == 'edit':
        bucket = task_bucket.Bucket(args.bucket)
        data = {
            'name': args.name,
            'new': args.new,
            'add_tags': args.addtags,
            'remove_tags': args.removetags
        }
        bucket.edit_task(data)
    if action == 'remove':
        bucket = task_bucket.Bucket(args.bucket)
        bucket.remove_task(args.name)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        action = sys.argv[1]
        args = parser.parse_args()
        handler(action, args)
