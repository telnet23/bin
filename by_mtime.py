import os
import sys

from datetime import datetime, timezone

tz = pytz.timezone('America/New_York')
prefix = sys.argv[1]

for path in sys.argv[2:]:
    timestamp = datetime.fromtimestamp(os.path.getmtime(path))
    timestamp = timestamp.replace(tzinfo=timezone.utc)
    timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')
    filename, extension = os.path.splitext(path)
    new = os.path.join(os.path.dirname(path), prefix + ' ' + timestamp + extension)
    os.rename(path, new)
    print(path + ' -> ' + new)
