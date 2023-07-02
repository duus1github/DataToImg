#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:duways
@file:utils.py
@date:2023/4/10 20:01
@desc:''
"""
import os
from tkinter import filedialog

import numpy as np


def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d} g)".format(pct, absolute)
