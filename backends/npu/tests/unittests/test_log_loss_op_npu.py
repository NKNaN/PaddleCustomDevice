# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import unittest

import numpy as np
import paddle
from tests.eager_op_test import OpTest

paddle.enable_static()


def sigmoid_array(x):
    return 1 / (1 + np.exp(-x))


class TestLogLossOp(OpTest):
    def setUp(self):
        self.set_npu()
        self.op_type = "log_loss"
        self.place = paddle.CustomPlace("npu", 0)

        self.init_dtype()

        self.set_inputs()
        self.set_attrs()
        self.set_outputs()

    def set_inputs(self):
        samples_num = 100
        x = np.random.random((samples_num, 1)).astype(self.dtype)
        predicted = sigmoid_array(x)
        labels = np.random.randint(0, 2, (samples_num, 1)).astype(self.dtype)
        self.inputs = {"Predicted": predicted, "Labels": labels}

    def set_attrs(self):
        epsilon = 1e-7
        self.attrs = {"epsilon": epsilon}

    def set_outputs(self):
        epsilon = self.attrs["epsilon"]
        labels = self.inputs["Labels"]
        predicted = self.inputs["Predicted"]
        loss = -labels * np.log(predicted + epsilon) - (1 - labels) * np.log(
            1 - predicted + epsilon
        )
        self.outputs = {"Loss": loss}

    def set_npu(self):
        self.__class__.use_custom_device = True

    def init_dtype(self):
        self.dtype = np.float32

    def test_check_output(self):
        self.check_output_with_place(self.place)

    def test_check_grad(self):
        self.check_grad_with_place(self.place, ["Predicted"], "Loss")


if __name__ == "__main__":
    unittest.main()
