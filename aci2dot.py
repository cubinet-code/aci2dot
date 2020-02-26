#!/usr/bin/env python

# aci2dot.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from __future__ import print_function
import argparse
import sys
import json
import os
from graphviz import Digraph

simple = False
show_attributes = True
g_attr = {
    'graph': {
        # "size": '8.27',
        # "ratio": 'auto',
        "nodesep": '0.2',
        "ranksep": '0.2',
        "bgcolor": 'white',
        "splines": 'true',
        "rankdir": 'LR',
        "dpi": "300"
    },
    'node': {
        "shape": 'box',
        "style": 'rounded,filled',
        "fillcolor": 'AZURE',
        "fontname": 'Helvetica'
    },
    'edge': {
        "arrowsize": "1"
    },
}


def dot_format_attr(policy, attr):

    if not show_attributes:
        return '<<B>{0}</B>>'.format(policy)

    attr_table = '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="1" CELLPADDING="1">'
    attr_table = attr_table + \
        '<TR><TD ALIGN="LEFT" COLSPAN="2"><B>{0}</B></TD><TD></TD></TR>'.format(
            policy)
    attr_table = attr_table + '<TR><TD></TD><TD></TD></TR>'

    for k, v in attr.items():
        if k not in ['status'] and v:
            attr_table = attr_table + \
                '<TR><TD ALIGN="LEFT">{0}</TD><TD ALIGN="LEFT">: {1}</TD></TR>'.format(
                    k, (v[:20] + '..') if len(v) > 20 else v)

    attr_table = attr_table + '</TABLE>>'

    return attr_table


def dot_convert_json(dot, d, i):

    for k, v in d.items():

        if isinstance(v, dict):
            attr = v.get("attributes")

            if attr:
                dot.node(k + str(i), dot_format_attr(k, attr))

            else:
                dot.node(k + str(i), k + str(i))

            children = v.get("children")

            if children:
                for child in children:
                    if not simple:
                        i = i + 1

                    for childk, childv in child.items():
                        dot.edge(k + str(i), childk + str(i))
                    dot_convert_json(dot, child, i)


def main():

    global simple
    global show_attributes
    global g_attr

    parser = argparse.ArgumentParser(
        description='Create DOT formatted Graph from JSON formatted ACI policy export.')
    parser.add_argument('policy_file', type=argparse.FileType(
        'r'), help='JSON ACI Policy Filename')
    parser.add_argument('--nr', action='store_true',
                        help='Suppress redundant children')
    parser.add_argument('--na', action='store_true',
                        help="Don't show attributes")
    parser.add_argument('--write', action='store_true',
                        help="Write config template to .aci2dot and exit")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--stdout', action='store_true',
                       help="Write to STDOUT instead of to file")
    choices = ["svg", "png", "pdf"]
    group.add_argument('--dot', choices=choices,
                       help="Also write SVG/PNG/PDF. 'dot' needs to be installed.")

    args = parser.parse_args()

    if args.write:
        with open(".aci2dot", "wt") as text_file:
            text_file.write(json.dumps(g_attr, indent=2))
        sys.exit('Config template written to .aci2dot')

    simple = args.nr
    show_attributes = not args.na if not args.nr else False

    try:
        data = json.load(args.policy_file)
    except json.decoder.JSONDecodeError:
        sys.exit('JSON File can not be read.')

    if data.get('imdata'):
        data = data.get('imdata')[0]

    base_name = (os.path.splitext(args.policy_file.name)[0])

    try:
        with open(".aci2dot", 'r') as config_file:
            g_attr = json.loads(config_file.read())
        print("Graph config read from .aci2dot", file=sys.stderr)
    except IOError:
        pass

    dot = Digraph(comment='datetimePol', format='svg')

    dot.graph_attr.update(**g_attr['graph'])
    dot.node_attr.update(**g_attr['node'])
    dot.edge_attr.update(**g_attr['edge'])

    dot_convert_json(dot, data, 0)

    if args.stdout:
        print(dot.source)
    else:
        with open('{0}.dot'.format(base_name), "wt") as text_file:
            text_file.write(dot.source)

    if args.dot:
        dot.render(base_name, format=args.dot, cleanup=True)
        print("{0} exported to {1}.{0}".format(
            args.dot, base_name), file=sys.stderr)


if __name__ == '__main__':
    main()
