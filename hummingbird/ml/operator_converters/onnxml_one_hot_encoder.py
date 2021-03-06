# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import numpy as np
from onnxconverter_common.registration import register_converter
import torch

from ._base_operator import BaseOperator
from ._one_hot_encoder_implementations import OneHotEncoderString, OneHotEncoder


def convert_onnx_one_hot_encoder(operator, device=None, extra_config={}):
    """
    Converter for `ai.onnx.ml.OneHotEncoder`

    Args:
        operator: An operator wrapping a `ai.onnx.ml.OneHotEncoder` model
        device: String defining the type of device the converted operator should be run on
        extra_config: Extra configuration used to select the best conversion strategy

    Returns:
        A PyTorch model
    """

    categories = []
    # is_strings = False
    operator = operator.raw_operator

    for attr in operator.origin.attribute:
        if attr.name == "cats_int64s":
            categories.append(np.array(attr.ints))
        elif attr.name == "cats_strings":
            raise NotImplementedError("OneHotEncoder does not yet support Strings (Issue #209)")
        #    categories.append([x.decode("UTF-8") for x in attr.strings])
        #    is_strings = True

    if categories == []:
        raise RuntimeError("Error parsing OneHotEncoder, no categories")

    # if is_strings:
    #     return OneHotEncoderString(categories, device)
    return OneHotEncoder(categories, device)


register_converter("ONNXMLOneHotEncoder", convert_onnx_one_hot_encoder)
