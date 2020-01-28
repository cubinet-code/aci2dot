aci2dot converts JSON formatted Cisco ACI policy files or snippets to a DOT graph format.

```
./aci2dot.py --help
usage: aci2dot.py [-h] [--nr] [--na] [--write]
                  [--stdout | --dot {svg,png,pdf}]
                  policy_file

Create DOT formatted Graph from JSON formatted ACI policy export.

positional arguments:
  policy_file          JSON ACI Policy Filename

optional arguments:
  -h, --help           show this help message and exit
  --nr                 Suppress redundant children
  --na                 Don't show attributes
  --write              Write config template to .aci2dot and exit
  --stdout             Write to STDOUT instead of to file
  --dot {svg,png,pdf}  Also write SVG/PNG/PDF. 'dot' needs to be installed.
```

For example:

![ACI Policy Graph](example/bgp.svg "ACI Policy Graph")

was rendered from:

```json
{
  "polUni": {
    "attributes": {
      "status": "created,modified"
    },
    "children": [{
      "fabricInst": {
        "attributes": {
          "status": "created,modified"
        },
        "children": [{
          "bgpInstPol": {
            "attributes": {
              "status": "created,modified",
              "ownerKey": "",
              "name": "default",
              "descr": "Default BGP Policy",
              "nameAlias": "",
              "ownerTag": "",
              "annotation": ""
            },
            "children": [{
              "bgpAsP": {
                "attributes": {
                  "status": "created,modified",
                  "name": "",
                  "descr": "",
                  "asn": "100",
                  "nameAlias": "",
                  "annotation": ""
                }
              }
            }, {
              "bgpExtRRP": {
                "attributes": {
                  "status": "created,modified",
                  "annotation": "",
                  "name": "",
                  "descr": "",
                  "nameAlias": ""
                }
              }
            }, {
              "bgpRRP": {
                "attributes": {
                  "status": "created,modified",
                  "annotation": "",
                  "name": "",
                  "descr": "",
                  "nameAlias": ""
                },
                "children": [{
                  "bgpRRNodePEp": {
                    "attributes": {
                      "status": "created,modified",
                      "descr": "",
                      "podId": "1",
                      "annotation": "",
                      "nameAlias": "",
                      "id": "1101"
                    }
                  }
                }, {
                  "bgpRRNodePEp": {
                    "attributes": {
                      "status": "created,modified",
                      "descr": "",
                      "podId": "1",
                      "annotation": "",
                      "nameAlias": "",
                      "id": "1102"
                    }
                  }
                }]
              }
            }]
          }
        }]
      }
    }, {
      "infraInfra": {
        "attributes": {
          "status": "created,modified"
        }
      }
    }]
  }
}
```
