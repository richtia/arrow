import pytest

TPCH_QUERIES = [
    (
        """
        {
          "extensionUris": [],
          "extensions": [],
          "relations": [{
            "root": {
              "input": {
                "project": {
                  "common": {
                    "emit": {
                      "outputMapping": [16, 17]
                    }
                  },
                  "input": {
                    "read": {
                      "common": {
                        "direct": {
                        }
                      },
                      "baseSchema": {
                        "names": ["L_ORDERKEY", "L_PARTKEY", "L_SUPPKEY", "L_LINENUMBER", "L_QUANTITY", "L_EXTENDEDPRICE", "L_DISCOUNT", "L_TAX", "L_RETURNFLAG", "L_LINESTATUS", "L_SHIPDATE", "L_COMMITDATE", "L_RECEIPTDATE", "L_SHIPINSTRUCT", "L_SHIPMODE", "L_COMMENT"],
                        "struct": {
                          "types": [{
                            "i64": {
                              "typeVariationReference": 0,
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }, {
                            "i64": {
                              "typeVariationReference": 0,
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }, {
                            "i64": {
                              "typeVariationReference": 0,
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }, {
                            "i32": {
                              "typeVariationReference": 0,
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }, {
                            "decimal": {
                              "scale": 0,
                              "precision": 19,
                              "typeVariationReference": 0,
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }, {
                            "decimal": {
                              "scale": 0,
                              "precision": 19,
                              "typeVariationReference": 0,
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }, {
                            "decimal": {
                              "scale": 0,
                              "precision": 19,
                              "typeVariationReference": 0,
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }, {
                            "decimal": {
                              "scale": 0,
                              "precision": 19,
                              "typeVariationReference": 0,
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }, {
                            "fixedChar": {
                              "length": 1,
                              "typeVariationReference": 0,
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }, {
                            "fixedChar": {
                              "length": 1,
                              "typeVariationReference": 0,
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }, {
                            "date": {
                              "typeVariationReference": 0,
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }, {
                            "date": {
                              "typeVariationReference": 0,
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }, {
                            "date": {
                              "typeVariationReference": 0,
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }, {
                            "fixedChar": {
                              "length": 25,
                              "typeVariationReference": 0,
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }, {
                            "fixedChar": {
                              "length": 10,
                              "typeVariationReference": 0,
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }, {
                            "varchar": {
                              "length": 44,
                              "typeVariationReference": 0,
                              "nullability": "NULLABILITY_NULLABLE"
                            }
                          }],
                          "typeVariationReference": 0,
                          "nullability": "NULLABILITY_REQUIRED"
                        }
                      },
                     "local_files": {
                         "items": [
                         {
                             "uri_file": "file://FILENAME_PLACEHOLDER"
                         }
                         ]
                     }
                    }
                  },
                  "expressions": [{
                    "selection": {
                      "directReference": {
                        "structField": {
                          "field": 8
                        }
                      },
                      "rootReference": {
                      }
                    }
                  }, {
                    "selection": {
                      "directReference": {
                        "structField": {
                          "field": 9
                        }
                      },
                      "rootReference": {
                      }
                    }
                  }]
                }
              },
              "names": ["L_RETURNFLAG", "L_LINESTATUS"]
            }
          }],
          "expectedTypeUrls": []
        }
        """
    ),
]