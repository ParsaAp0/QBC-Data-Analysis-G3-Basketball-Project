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
import plotly.express as px
import plotly.io as pio
from scipy.stats import shapiro
from scipy.stats import ttest_ind
from scipy.stats import mannwhitneyu
import plotly.graph_objects as go
from scipy.stats import levene
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy.stats import chi2_contingency

from scipy.stats import pearsonr
from scipy.stats import spearmanr
from scipy.stats import linregress
# Database engine
engine = create_engine(
    "mysql+mysqlconnector://root:77032098!@localhost/basketball_db"
)

def run_query(query):
    return pd.read_sql(query, engine)