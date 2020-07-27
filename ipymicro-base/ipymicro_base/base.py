#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Ian Hunt-Isaak.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget, Color
from traitlets import Unicode, Bool, CInt
from ._frontend import module_name, module_version


class baseCanvasModel(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('baseCanvasModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('baseCanvasView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Unicode('Hello World').tag(sync=True)

    
    classColor = Color('red').tag(sync=True)
    erasing = Bool(True).tag(sync=True)
    # underlying info for labels - this handles the syncing to ts
    # _labels = Bytes(default_value=None, allow_none=True, read_only=True).tag(sync=True, **labels_serialization)
    # yikes = 

    # data = DataUnion(
    #     np.zeros([10, 10, 4], dtype=np.uint8),
    #     dtype='uint8', shape_constraint=shape_constraints(None, None, 4),  # 2D RGBA
    # ).tag(sync=True, **data_union_serialization)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.on_msg(self.handle_msg)

    width = CInt(700).tag(sync=True)
    height = CInt(700).tag(sync=True)

    def set_image(self, arr):
        """
        Set the image to be segmented
        arr : numpy array
            Shape (WxHx1) or (WxHx3)
        TODO: transparency here? I removed the transparency enabling code
        on the typescript side to make things simpler with the class canvas
        """
        image_metadata, image_buffer = binary_image(arr)
        command = {
            'name': 'image',
            'metadata': image_metadata
        }
        self.send(command, (image_buffer,))

    def gogogo(self):
        command = {
            'name': 'gogogo'
        }
        self.send(command, [])

    def beep(self):
        command = {
            'name': 'beep'
        }
        self.send(command, [])
    def gimme(self):
        command = {
            'name': 'gimme'
        }
        self.send(command, [])


    def handle_msg(self, widget, content, buffers):
        # print('widget:', widget)
        # print(content)
        # self.gogogo()
        self.yikes(content['start'])


"""Binary module."""
from io import BytesIO

# from PIL import Image as PILImage

import numpy as np


# def image_bytes_to_array(im_bytes):
#     """Turn raw image bytes into a NumPy array."""
#     im_file = BytesIO(im_bytes)

#     im = PILImage.open(im_file)

#     return np.array(im)


def binary_image(ar):
    """Turn a NumPy array representing an array of pixels into a binary buffer."""
    if ar is None:
        return None
    if ar.dtype != np.uint8:
        ar = ar.astype(np.uint8)
    if ar.ndim == 1:
        ar = ar[np.newaxis, :]
    if ar.ndim == 2:
        # extend grayscale to RGBA
        add_alpha = np.full((ar.shape[0], ar.shape[1], 4), 255, dtype=np.uint8)
        add_alpha[:, :, :3] = np.repeat(ar[:, :, np.newaxis], repeats=3, axis=2)
        ar = add_alpha
    if ar.ndim != 3:
        raise ValueError("Please supply an RGBA array with shape (width, height, 4).")
    if ar.shape[2] != 4 and ar.shape[2] == 3:
        add_alpha = np.full((ar.shape[0], ar.shape[1], 4), 255, dtype=np.uint8)
        add_alpha[:, :, :3] = ar
        ar = add_alpha
    if not ar.flags["C_CONTIGUOUS"]:  # make sure it's contiguous
        ar = np.ascontiguousarray(ar, dtype=np.uint8)
    return {'shape': ar.shape, 'dtype': str(ar.dtype)}, memoryview(ar)


def array_to_binary(ar):
    """Turn a NumPy array into a binary buffer."""
    # Unsupported int64 array JavaScript side
    if ar.dtype == np.int64:
        ar = ar.astype(np.int32)

    # Unsupported float16 array JavaScript side
    if ar.dtype == np.float16:
        ar = ar.astype(np.float32)

    # make sure it's contiguous
    if not ar.flags["C_CONTIGUOUS"]:
        ar = np.ascontiguousarray(ar)

    return {'shape': ar.shape, 'dtype': str(ar.dtype)}, memoryview(ar)


def populate_args(arg, args, buffers):
    if isinstance(arg, (list, np.ndarray)):
        arg_metadata, arg_buffer = array_to_binary(np.asarray(arg))
        arg_metadata['idx'] = len(buffers)

        args.append(arg_metadata)
        buffers.append(arg_buffer)
    else:
        args.append(arg)

