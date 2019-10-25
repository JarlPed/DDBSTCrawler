# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 00:11:44 2019

@author: jarl
"""

from sympy import Eq, Symbol, symbols, solve, nsolve, diff, exp, init_printing


init_printing()

kappa, k_B, T, h, DeltaG_react, R = symbols('kappa k_B T hbar DeltaG_react R')


k = kappa*k_B*T/h*exp(-DeltaG_react/R/T)




