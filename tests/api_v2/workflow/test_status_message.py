# coding: utf-8


def test_ecflow_status_message(app):
    from flask import json
    client = app.test_client()
    message = {
        'app': 'ecflow_status_collector',
        'data': {
            'owner': 'nwp_xp',
            'repo': 'nwpc_op',
            'time': '2018-09-21T15:20:59.667581',
            'status': {
                "name": "",
                "node_type": "root",
                "node_path": "/",
                "path": "/",
                "status": "aborted",
                "children": [
                    {
                        "name": "windroc_test_suite",
                        "children": [
                            {
                                "name": "initial",
                                "children": [],
                                "node_type": "task",
                                "node_path": "/windroc_test_suite/initial",
                                "path": "/windroc_test_suite/initial",
                                "status": "complete"
                            }
                        ],
                        "node_type": "suite",
                        "node_path": "/windroc_test_suite",
                        "path": "/windroc_test_suite",
                        "status": "complete"
                    },
                    {
                        "name": "grapes_meso_3km_post",
                        "node_type": "suite",
                        "node_path": "/grapes_meso_3km_post",
                        "path": "/grapes_meso_3km_post",
                        "status": "aborted",
                        "children": [
                            {
                                "name": "00",
                                "node_type": "family",
                                "node_path": "/grapes_meso_3km_post/00",
                                "path": "/grapes_meso_3km_post/00",
                                "status": "aborted",
                                "children": [
                                    {
                                        "name": "initial",
                                        "children": [],
                                        "node_type": "task",
                                        "node_path": "/grapes_meso_3km_post/00/initial",
                                        "path": "/grapes_meso_3km_post/00/initial",
                                        "status": "aborted"
                                    },
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }
    data = {
        'message': json.dumps(message)
    }

    rv = client.post("/api/v2/hpc/workflow/status", data=data)
    assert 'status' in rv.json and rv.json['status'] == 'ok'


def test_sms_status_message(app):
    from flask import json
    client = app.test_client()
    message = {
        'app': 'sms_status_collector',
        'data': {
            "owner": "nwp_xp",
            "repo": "nwpc_pd",
            "sms_name": "nwpc_op",
            "sms_user": "nwp_xp",
            "time": "2018-09-21T16:47:57.794964",
            "status": {
                "name": "nwpc_op",
                "children": [
                    {
                        "name": "ssfs_v_4_0",
                        "children": [
                            {
                                "name": "CUACE_Dust",
                                "children": [
                                    {
                                        "name": "00",
                                        "children": [
                                            {
                                                "name": "initial",
                                                "children": [],
                                                "status": "abo",
                                                "path": "/ssfs_v_4_0/CUACE_Dust/00/initial"
                                            },
                                            {
                                                "name": "pre_data",
                                                "children": [
                                                    {
                                                        "name": "obs_get",
                                                        "children": [],
                                                        "status": "com",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/00/pre_data/obs_get"
                                                    },
                                                    {
                                                        "name": "gmf_get",
                                                        "children": [],
                                                        "status": "com",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/00/pre_data/gmf_get"
                                                    },
                                                    {
                                                        "name": "terrain",
                                                        "children": [],
                                                        "status": "com",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/00/pre_data/terrain"
                                                    }
                                                ],
                                                "status": "com",
                                                "path": "/ssfs_v_4_0/CUACE_Dust/00/pre_data"
                                            },
                                            {
                                                "name": "an_3dvar",
                                                "children": [
                                                    {
                                                        "name": "analy",
                                                        "children": [],
                                                        "status": "com",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/00/an_3dvar/analy"
                                                    }
                                                ],
                                                "status": "com",
                                                "path": "/ssfs_v_4_0/CUACE_Dust/00/an_3dvar"
                                            },
                                            {
                                                "name": "pre_proc",
                                                "children": [
                                                    {
                                                        "name": "regridder",
                                                        "children": [],
                                                        "status": "com",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/00/pre_proc/regridder"
                                                    },
                                                    {
                                                        "name": "interpf",
                                                        "children": [],
                                                        "status": "com",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/00/pre_proc/interpf"
                                                    }
                                                ],
                                                "status": "com",
                                                "path": "/ssfs_v_4_0/CUACE_Dust/00/pre_proc"
                                            },
                                            {
                                                "name": "model",
                                                "children": [
                                                    {
                                                        "name": "fcst",
                                                        "children": [],
                                                        "status": "com",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/00/model/fcst"
                                                    }
                                                ],
                                                "status": "com",
                                                "path": "/ssfs_v_4_0/CUACE_Dust/00/model"
                                            },
                                            {
                                                "name": "post",
                                                "children": [
                                                    {
                                                        "name": "interpb",
                                                        "children": [],
                                                        "status": "com",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/00/post/interpb"
                                                    }
                                                ],
                                                "status": "com",
                                                "path": "/ssfs_v_4_0/CUACE_Dust/00/post"
                                            },
                                            {
                                                "name": "prods",
                                                "children": [
                                                    {
                                                        "name": "product",
                                                        "children": [],
                                                        "status": "com",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/00/prods/product"
                                                    },
                                                    {
                                                        "name": "rsmc",
                                                        "children": [
                                                            {
                                                                "name": "postp",
                                                                "children": [],
                                                                "status": "com",
                                                                "path": "/ssfs_v_4_0/CUACE_Dust/00/prods/rsmc/postp"
                                                            },
                                                            {
                                                                "name": "grib2",
                                                                "children": [],
                                                                "status": "com",
                                                                "path": "/ssfs_v_4_0/CUACE_Dust/00/prods/rsmc/grib2"
                                                            },
                                                            {
                                                                "name": "nclchart",
                                                                "children": [],
                                                                "status": "com",
                                                                "path": "/ssfs_v_4_0/CUACE_Dust/00/prods/rsmc/nclchart"
                                                            },
                                                            {
                                                                "name": "ncandplot",
                                                                "children": [],
                                                                "status": "com",
                                                                "path": "/ssfs_v_4_0/CUACE_Dust/00/prods/rsmc/ncandplot"
                                                            }
                                                        ],
                                                        "status": "com",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/00/prods/rsmc"
                                                    },
                                                    {
                                                        "name": "upload",
                                                        "children": [
                                                            {
                                                                "name": "upload_nmcdb",
                                                                "children": [],
                                                                "status": "com",
                                                                "path": "/ssfs_v_4_0/CUACE_Dust/00/prods/upload/upload_nmcdb"
                                                            },
                                                            {
                                                                "name": "upload_rsmc",
                                                                "children": [],
                                                                "status": "com",
                                                                "path": "/ssfs_v_4_0/CUACE_Dust/00/prods/upload/upload_rsmc"
                                                            },
                                                            {
                                                                "name": "upload_cmo",
                                                                "children": [],
                                                                "status": "com",
                                                                "path": "/ssfs_v_4_0/CUACE_Dust/00/prods/upload/upload_cmo"
                                                            }
                                                        ],
                                                        "status": "com",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/00/prods/upload"
                                                    }
                                                ],
                                                "status": "com",
                                                "path": "/ssfs_v_4_0/CUACE_Dust/00/prods"
                                            },
                                            {
                                                "name": "archive",
                                                "children": [
                                                    {
                                                        "name": "archiving",
                                                        "children": [],
                                                        "status": "com",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/00/archive/archiving"
                                                    }
                                                ],
                                                "status": "com",
                                                "path": "/ssfs_v_4_0/CUACE_Dust/00/archive"
                                            }
                                        ],
                                        "status": "com",
                                        "path": "/ssfs_v_4_0/CUACE_Dust/00"
                                    },
                                    {
                                        "name": "12",
                                        "children": [
                                            {
                                                "name": "initial",
                                                "children": [],
                                                "status": "que",
                                                "path": "/ssfs_v_4_0/CUACE_Dust/12/initial"
                                            },
                                            {
                                                "name": "pre_data",
                                                "children": [
                                                    {
                                                        "name": "obs_get",
                                                        "children": [],
                                                        "status": "que",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/12/pre_data/obs_get"
                                                    },
                                                    {
                                                        "name": "gmf_get",
                                                        "children": [],
                                                        "status": "que",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/12/pre_data/gmf_get"
                                                    },
                                                    {
                                                        "name": "terrain",
                                                        "children": [],
                                                        "status": "que",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/12/pre_data/terrain"
                                                    }
                                                ],
                                                "status": "que",
                                                "path": "/ssfs_v_4_0/CUACE_Dust/12/pre_data"
                                            },
                                            {
                                                "name": "an_3dvar",
                                                "children": [
                                                    {
                                                        "name": "analy",
                                                        "children": [],
                                                        "status": "que",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/12/an_3dvar/analy"
                                                    }
                                                ],
                                                "status": "que",
                                                "path": "/ssfs_v_4_0/CUACE_Dust/12/an_3dvar"
                                            },
                                            {
                                                "name": "pre_proc",
                                                "children": [
                                                    {
                                                        "name": "regridder",
                                                        "children": [],
                                                        "status": "que",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/12/pre_proc/regridder"
                                                    },
                                                    {
                                                        "name": "interpf",
                                                        "children": [],
                                                        "status": "que",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/12/pre_proc/interpf"
                                                    }
                                                ],
                                                "status": "que",
                                                "path": "/ssfs_v_4_0/CUACE_Dust/12/pre_proc"
                                            },
                                            {
                                                "name": "model",
                                                "children": [
                                                    {
                                                        "name": "fcst",
                                                        "children": [],
                                                        "status": "que",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/12/model/fcst"
                                                    }
                                                ],
                                                "status": "que",
                                                "path": "/ssfs_v_4_0/CUACE_Dust/12/model"
                                            },
                                            {
                                                "name": "post",
                                                "children": [
                                                    {
                                                        "name": "interpb",
                                                        "children": [],
                                                        "status": "que",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/12/post/interpb"
                                                    }
                                                ],
                                                "status": "que",
                                                "path": "/ssfs_v_4_0/CUACE_Dust/12/post"
                                            },
                                            {
                                                "name": "prods",
                                                "children": [
                                                    {
                                                        "name": "product",
                                                        "children": [],
                                                        "status": "que",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/12/prods/product"
                                                    },
                                                    {
                                                        "name": "rsmc",
                                                        "children": [
                                                            {
                                                                "name": "postp",
                                                                "children": [],
                                                                "status": "que",
                                                                "path": "/ssfs_v_4_0/CUACE_Dust/12/prods/rsmc/postp"
                                                            },
                                                            {
                                                                "name": "grib2",
                                                                "children": [],
                                                                "status": "que",
                                                                "path": "/ssfs_v_4_0/CUACE_Dust/12/prods/rsmc/grib2"
                                                            },
                                                            {
                                                                "name": "nclchart",
                                                                "children": [],
                                                                "status": "que",
                                                                "path": "/ssfs_v_4_0/CUACE_Dust/12/prods/rsmc/nclchart"
                                                            },
                                                            {
                                                                "name": "ncandplot",
                                                                "children": [],
                                                                "status": "que",
                                                                "path": "/ssfs_v_4_0/CUACE_Dust/12/prods/rsmc/ncandplot"
                                                            }
                                                        ],
                                                        "status": "que",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/12/prods/rsmc"
                                                    },
                                                    {
                                                        "name": "upload",
                                                        "children": [
                                                            {
                                                                "name": "upload_nmcdb",
                                                                "children": [],
                                                                "status": "que",
                                                                "path": "/ssfs_v_4_0/CUACE_Dust/12/prods/upload/upload_nmcdb"
                                                            },
                                                            {
                                                                "name": "upload_rsmc",
                                                                "children": [],
                                                                "status": "que",
                                                                "path": "/ssfs_v_4_0/CUACE_Dust/12/prods/upload/upload_rsmc"
                                                            },
                                                            {
                                                                "name": "upload_cmo",
                                                                "children": [],
                                                                "status": "que",
                                                                "path": "/ssfs_v_4_0/CUACE_Dust/12/prods/upload/upload_cmo"
                                                            }
                                                        ],
                                                        "status": "que",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/12/prods/upload"
                                                    }
                                                ],
                                                "status": "que",
                                                "path": "/ssfs_v_4_0/CUACE_Dust/12/prods"
                                            },
                                            {
                                                "name": "archive",
                                                "children": [
                                                    {
                                                        "name": "archiving",
                                                        "children": [],
                                                        "status": "que",
                                                        "path": "/ssfs_v_4_0/CUACE_Dust/12/archive/archiving"
                                                    }
                                                ],
                                                "status": "que",
                                                "path": "/ssfs_v_4_0/CUACE_Dust/12/archive"
                                            }
                                        ],
                                        "status": "que",
                                        "path": "/ssfs_v_4_0/CUACE_Dust/12"
                                    },
                                    {
                                        "name": "housekeep",
                                        "children": [
                                            {
                                                "name": "housekeeping",
                                                "children": [],
                                                "status": "que",
                                                "path": "/ssfs_v_4_0/CUACE_Dust/housekeep/housekeeping"
                                            }
                                        ],
                                        "status": "que",
                                        "path": "/ssfs_v_4_0/CUACE_Dust/housekeep"
                                    }
                                ],
                                "status": "que",
                                "path": "/ssfs_v_4_0/CUACE_Dust"
                            }
                        ],
                        "status": "abo",
                        "path": "/ssfs_v_4_0"
                    }
                ],
                "status": "abo",
                "path": "/"
            }
        }

    }
    data = {
        'message': json.dumps(message)
    }

    rv = client.post("/api/v2/hpc/workflow/status", data=data)
    assert 'status' in rv.json and rv.json['status'] == 'ok'
