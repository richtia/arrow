# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import pytest

from _pytest.mark.structures import MarkDecorator


def custom_parametrization(test_cases: list[dict]) -> MarkDecorator:
    """
    Wrapper for pytest.mark.parametrize to make parametrized test cases more
    readable. Converts a list of dictionary key-value pairs to the
    corresponding pytest.mark.parametrize syntax.

    Example:
        Input:
            [
                {
                    "test_name": "test_1",
                    "expected_results": 5
                },
                {
                    "test_name": "test_2",
                    "expected_results": 1
                },
            ]
        Output:
            @pytest.mark.parametrize(
                'test_name,expected_results',
                [('test_1', 5), ('test_2', 1)]
            )
    """

    argument_names = ",".join(test_cases[0].keys())
    argument_values = []
    for test_case in test_cases:
        test_case_list = []
        arg_names = ",".join(test_case.keys())
        if argument_names != arg_names:
            error_message = (
                f"Argument names between test cases are inconsistent.  "
                f"First arguments: {argument_names}, inconsistent " 
                f"arguments: {arg_names}"
            )
            raise ValueError(error_message)
        for value in test_case.values():
            test_case_list.append(value)
        test_case_tuple = tuple(test_case_list)

        argument_values.append(test_case_tuple)

    return pytest.mark.parametrize(argnames=argument_names,
                                   argvalues=argument_values)
