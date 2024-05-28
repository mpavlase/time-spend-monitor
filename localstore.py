from store import StoreInterface
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import namedtuple, defaultdict
import json
import argparse


StartedProject = namedtuple('StartedProject',
                            ['timestamp', 'project'])


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime, )):
            return o.isoformat()


def datetime_decoder(dict_obj):
    for key, value in dict_obj.items():
        if isinstance(value, list):
            dict_obj[key] = [
                datetime.fromisoformat(item_str)
                for item_str in value
            ]

    return dict_obj


class LocalStore(StoreInterface):
    store: Dict[str, List[datetime]]

    def __init__(self, db_filename: Optional[str] = None):
        super().__init__()
        self.store = defaultdict(lambda: list())
        self.db_filename = db_filename

        if db_filename is not None:
            self.store.update(self._load_from_db())

    def _load_from_db(self):
        try:
            with open(self.db_filename) as fd:
                return json.load(fd, object_hook=datetime_decoder)
        except FileNotFoundError:
            return {}

    def _save_to_db(self):
        with open(self.db_filename, 'w') as fd:
            json.dump(self.store, fd, cls=DateTimeEncoder)

    def switch_to(self, project: str, at: Optional[datetime] = None):
        current_project = self.get_current_project()
        if current_project == project:
            return

        if at is None:
            at = datetime.now()

        self.store[project].append(at)
        self._save_to_db()

    def get_total_spent_per_project(self, finished_at: Optional[datetime] = None):
        cumulative_spent_times: Dict[str, int] = defaultdict(lambda: 0)
        sorted_times = self._get_sorted_by_time()

        if finished_at is None:
            finished_at = datetime.now()

        last_item = None

        for item in sorted_times:
            if last_item is None:
                last_item = item
                continue

            last_duration = (item.timestamp - last_item.timestamp).seconds
            last_project = last_item.project
            cumulative_spent_times[last_project] += last_duration
            last_item = item

        if sorted_times:
            last_duration = (finished_at - last_item.timestamp).seconds
            last_project = last_item.project
            cumulative_spent_times[last_project] += last_duration

        return cumulative_spent_times

    def get_current_project(self) -> Optional[str]:
        if len(self.store) == 0:
            return None

        def compare_fn(project_name: str):
            if project_name not in self.store:
                return datetime.min

            if len(self.store[project_name]) == 0:
                return datetime.min

            return self.store[project_name][-1]

        sorted_item = sorted(self.store.keys(), key=compare_fn, reverse=True)

        return sorted_item[0]

    def _get_sorted_by_time(self) -> List[StartedProject]:
        times: List[StartedProject] = []

        for project_name, project_times in self.store.items():
            items = (StartedProject(
                timestamp=time,
                project=project_name)
                for time in project_times)
            times.extend(items)

        times.sort(key=lambda item: item.timestamp)

        return times


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--summary', help='Show summary of time spent per project',
                        action='store_true',
                        default=True)
    parser.add_argument('db_file',
                        nargs='?',
                        default='db.json',
                        help='File with DB (default: db.json)'
                        )

    args = parser.parse_args()

    if args.summary:
        store = LocalStore(args.db_file)
        summary = store.get_total_spent_per_project()
        current_project = store.get_current_project()

        for project, seconds in summary.items():
            time = timedelta(seconds=seconds)
            current_marker = '  <--' if project == current_project else ''

            print(f'{project:20}: {time}{current_marker}')
