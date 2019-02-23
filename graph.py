import json
import sys

nodes = set()
edges = set()
for line in sys.stdin:
    source, target = line.strip().split(' -> ')
    nodes.add(source)
    nodes.add(target)
    edges.add((source, target))
out = []
for node in nodes:
    print('adding node {}'.format(node))
    out.append({'group': 'nodes',
                'data': {'id': node}})
for (source, target) in edges:
    print('adding edge {} -> {}'.format(source, target))
    out.append({'group': 'edges',
                'data': {'id': '{}-{}'.format(source, target),
                         'source': source,
                         'target': target}})
json.dump(out, fp=sys.stdout)
