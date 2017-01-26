import os
import json
from datetime import datetime


DATE_FORMAT = '%l:%M%p %Z on %b %d, %Y'
HOME = os.path.expanduser("~")
MINION_HOME = os.path.join(HOME, '.minion')


class Bucket(object):

    def __init__(self, name):
        self.name = name
        self.location = os.path.join(MINION_HOME, '{0}.json'.format(self.name))

    def _load(self):
        if not os.path.isfile(self.location):
            return None
        data = json.load(open(self.location, 'r'))
        return data

    def _dump(self, data):
        json.dump(data, open(self.location, 'w'))

    def _pretty_print(self, data):
        print('status  | task | tags | start date | end date\n')
        for item in data:
            mark = 'X' if item.get('closed_date') else ' '
            tags = ','.join(item.get('tags')) if item.get('tags') else 'NA'
            print('[{0}] | {1} | {2} | {3} | {4}\n'.format(
                mark, item.get('name'), tags,
                item.get('added_date'), item.get('closed_date', 'NA')
            ))

    def create(self):
        if not os.path.isfile(self.location):
            self._dump([])
        else:
            print('"{0}" bucket already exists'.format(self.name))
        return

    def rename(self, name):
        dest = os.path.join(MINION_HOME, '{0}.json'.format(name))
        os.rename(self.location, dest)
        return

    def delete(self):
        if os.path.isfile(self.location):
            os.remove(self.location)
        else:
            print('{0} is not a valid bucket'.format(self.name))
        return

    def _check_for_unique_task(self, data, name):
        for item in data:
            if item['name'] == name:
                return True
        return False

    def add_task(self, task):
        data = self._load()
        task_name = task['name']
        if data is None:
            print('{0} is not a valid bucket'.format(self.name))
        else:
            if self._check_for_unique_task(data, task_name):
                print('"{0}" task already exists'.format(task_name))
            else:
                data.append(task)
                self._dump(data)
        return

    def edit_task(self, task):
        data = self._load()
        new_name = task['new']
        if data is None:
            print('{0} is not a valid bucket'.format(self.name))
        else:
            if self._check_for_unique_task(data, new_name):
                print('"{0}" task already exists'.format(new_name))
            else:
                for item in data:
                    if item['name'] == task['name']:
                        item['name'] = new_name if new_name else item['name']
                        if task['add_tags']:
                            item['tags'].extend(task['add_tags'])
                            item['tags'] = list(set(item['tags']))
                        if task['remove_tags']:
                            for tag in task['remove_tags']:
                                if tag in item['tags']:
                                    item['tags'].remove(tag)
                self._dump(data)
        return

    def remove_task(self, name):
        data = self._load()
        for item in data:
            if item['name'] == name:
                data.remove(item)
                break
        self._dump(data)
        return

    def close_task(self, name):
        data = self._load()
        for item in data:
            if item['name'] == name:
                item['status'] = 'closed'
                item['closed_date'] = datetime.now().strftime(DATE_FORMAT)
                break
        self._dump(data)
        return

    def _filter_by_status(self, data, status):
        tasks = []
        for item in data:
            if item['status'] == status:
                tasks.append(item)
        return tasks

    def _filter_by_tag(Self, data, tag):
        tasks = []
        for item in data:
            if tag in item.get('tags', []):
                tasks.append(item)
        return tasks

    def list_task(self, status=None, tag=None):
        data = self._load()
        if data is None:
            print('{0} is not a valid bucket'.format(self.name))
        else:
            if status:
                data = self._filter_by_status(data, status)
            if tag:
                data = self._filter_by_tag(data, tag)
            self._pretty_print(data)
        return
