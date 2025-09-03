#!/usr/bin/env /Users/rcap/venvs/openttd/bin/python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title manhattan
# @raycast.mode compact

# Optional parameters:
# @raycast.icon 🤖
# @raycast.argument1 { "type": "text", "placeholder": "x1 y1" }
# @raycast.argument2 { "type": "text", "placeholder": "x2 y2" }
# @raycast.packageName manhattan

# Documentation:
# @raycast.author ric

import sys

start = sys.argv[1]
end = sys.argv[2]

start = tuple(map(int, start.split(" ")))
end = tuple(map(int, end.split(" ")))

distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
print(f"Manhattan distance: {distance} tiles.")
