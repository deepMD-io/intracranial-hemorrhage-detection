#!/usr/bin/env python
# coding: utf-8

import sys
import os
import csv
import numpy as np
import pandas as pd
import pydicom
from tqdm.auto import tqdm
tqdm.pandas()


TRAIN_CSV_PATH = '../src/training.csv'
VALIDATE_CSV_PATH = '../src/validation.csv'
TEST_CSV_PATH = '../src/testing.csv'

train_data = '../../data/stage_1_train_images/'
test_data = '../../data/stage_1_test_images/'


def check_dicom(row, path=train_data):
    try:
        data = pydicom.dcmread(path+row[0])
    except ValueError:
        print('corruption on open...')
        return False
    try:
        img = np.array(data.pixel_array, dtype=float)
    except ValueError:
        print('corruption on pixel_array...')
        return False
    if img.shape != (512, 512):
        print('square peg in round hole!')
        return False
    return True

# Comment or Uncomment to process TRAINING data
df_train = pd.read_csv(TRAIN_CSV_PATH)
df_train['bad_actors'] = df_train.progress_apply(lambda x: check_dicom(x), axis=1)
df_train.to_csv('../src/train_flagged.csv', index=False)

# Comment or Uncomment to process VALIDATION data
df_validate = pd.read_csv(VALIDATE_CSV_PATH)
df_validate['bad_actors'] = df_validate.progress_apply(lambda x: check_dicom(x), axis=1)
df_validate.to_csv('../src/validate_flagged.csv', index=False)

# Comment or Uncomment to process TEST data
# df_test = pd.read_csv(TEST_CSV_PATH)
# df_test['bad_actors'] = df_test.progress_apply(lambda x: check_dicom(x),axis=1)
# df_test.to_csv('../src/test_flagged.csv', index=False)

print('All Done!')