#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:22:16 2026

@author: amirreza
"""

from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Database engine
engine = create_engine(
    "mysql+mysqlconnector://root:77032098!@localhost/basketball_db"
)

def run_query(query):
    return pd.read_sql(query, engine)