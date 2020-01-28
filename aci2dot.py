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

import argparse
import sys
import json
import os

simple = False
show_attributes = True
gformat = '''
  graph [
    size="8.27";
    ratio="1";
    nodesep="0.15";
    ranksep="0.5";
    #splines="false";
    rankdir=LR;
    bgcolor="transparent";
  ];
  node [
    shape=box;
    style="rounded,filled";
    fillcolor=AZURE;
    fontname=Helvetica;
  ]
  edge [
    #arrowsize=0.5;
  ]
  '''


def format_attr(policy, attr):

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


def iterd(d, i):

    for k, v in d.items():

        if isinstance(v, dict):
            attr = v.get("attributes")

            if attr:
                print('{0} [label={1};]'.format(
                    k + str(i), format_attr(k, attr)))
            else:
                print('{0} [label="{0}";]'.format(k + str(i)))

            children = v.get("children")

            if children:
                childi = 0
                for child in children:
                    if not simple:
                        childi = childi + 1

                    for childk, childv in child.items():
                        print('{0} -> {1}'.format(k +
                                                  str(i), childk + str(childi)))
                    iterd(child, childi)


def write_gformat():
    with open(".aci2dot", "wt") as text_file:
        text_file.write(gformat)


def main():

    global simple
    global show_attributes
    global gformat

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
        write_gformat()
        sys.exit('Config template written to .aci2dot')

    simple = args.nr
    show_attributes = not args.na if not args.nr else False

    try:
        data = json.load(args.policy_file)
    except json.decoder.JSONDecodeError:
        sys.exit('JSON File can not be read.')

    base_name = (os.path.splitext(args.policy_file.name)[0])

    try:
        with open(".aci2dot", 'r') as config_file:
            gformat = config_file.read()
        print("Graph config read from .aci2dot", file=sys.stderr)
    except IOError:
        pass

    if not args.stdout:
        sys.stdout = open('{0}.dot'.format(base_name), 'w')

    print('strict digraph Policy {')
    print(gformat)
    iterd(data, 0)
    print('}', flush=True)

    if args.dot:
        os.system("dot -T{0} -o{1}.{0} {1}.dot".format(args.dot, base_name))
        print("{0} exported to {1}.{0}".format(
            args.dot, base_name), file=sys.stderr)


if __name__ == '__main__':
    main()
