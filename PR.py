# -*- coding: utf-8 -*-
"""
Created on Thu May 23 20:09:51 2019

@author: jarl
"""

from sympy import symbols, Symbol, Function, solve, Eq, sympify, init_printing, Matrix, diff, summation, oo, exp, Sum, zeta


init_printing()
R, T_c, p_c, V_mc, C_a, C_b  = symbols('R T_c p_c V_mc C_a C_b ')

T, p, V_m, kappa, alfa, a, b = symbols('T p V_m, kappa alpha a b')

V, n = symbols('V n')

Z, Z_c, omega = symbols('Z Z_c omega')

kappa_c = [0]*4
for i in range(len(kappa_c)):
    kappa_c[i] = Symbol("kappa_0c"+str(i))
#kappa_c1, kappa_c2, kappa_c3, kappa_c4, omega = symbols('kappa_c1 kappa_c2 kappa_c3 kappa_c4 omega')



#V_m = Z*R*T/p

#C_a = 0.45724
#C_b = 0.07780
#R = 8.314
#kappa_c1 = 0.37464
#kappa_c2 = 1.54226
#kappa_c3 = 0.26992





#a = C_a  *R**2*T_c**2 /p_c
#b = C_b * R*T_c /p_c




kappa_PR = kappa_c[0] + kappa_c[1] *omega + kappa_c[2] * omega**2
alfa_PR = (1+ kappa*(1- (T/T_c)**(sympify(1)/2) ))**2




kappa_0_PRSV1 =kappa_c[0] + kappa_c[1] *omega + kappa_c[2] * omega**2 +  kappa_c[3] * omega**3
kappa_1, kappa_2, kappa_3 = symbols("kappa_1 kappa_2 kappa_3")
#kappa_PRSV1 =  kappa_0_PRSV1 + kappa_1*(1 + (T/T_c)**(sympify(1)/2) ) * (0.7 - T/T_c )
kappa_PRSV1 =  kappa_0_PRSV1 + kappa_1*(1 + (T/T_c)**0.5 ) * (0.7 - T/T_c )

#kappa_PRSV2 =  kappa_0_PRSV1 +  (kappa_1 + kappa_2*(kappa_3-T/T_c)*(1- (T/T_c)**(sympify(1)/2)) )  * (1 + (T/T_c)**(sympify(1)/2) ) * (0.7 - T/T_c )
kappa_PRSV2 =  kappa_0_PRSV1 +  (kappa_1 + kappa_2*(kappa_3-T/T_c)*(1- (T/T_c)**0.5) )  * (1 + (T/T_c)**0.5 ) * (0.7 - T/T_c )




Cubic_State = Eq(p,  R*T/(V_m-b) - a*alfa/(V_m**2 +2*b*V_m - b**2))

PR = Cubic_State.subs(alfa, alfa_PR.subs(kappa, kappa_PR) )
PRSV1 = Cubic_State.subs(alfa, alfa_PR.subs(kappa, kappa_PRSV1) )
PRSV2 = Cubic_State.subs(alfa, alfa_PR.subs(kappa, kappa_PRSV2))



#PR_Z_c = Matrix(  solve( PR.subs(p, p_c).subs(T, T_c).subs(V_m, Z_c*R*T_c/p_c ), Z_c) )
#PR_V_c = Matrix( solve(  PR.subs(p, p_c).subs(T, T_c), V_m  )  )

#V_m_c = PR_Z_c*R*T_c/p_c

Critical_state_conds_PR = Matrix([ PR , Eq( diff(PR.rhs, V_m), 0) , Eq( diff(PR.rhs, V_m, 2), 0) ]).subs(p, p_c).subs(T, T_c).subs(V_m, V_mc)  # .subs(V_m, Z_c*R*T_c/p_c )

solve_ab = solve(Critical_state_conds_PR[1:], [a, b] )

#PR_sol = PR.subs(a, solve_ab[0][0].evalf() ).subs(b, solve_ab[0][1].evalf() )
PR_sol = PR.subs(a, solve_ab[0][0] ).subs(b, solve_ab[0][1] )



V_m_atCrit = Matrix(solve(PR.subs(T, T_c).subs(p, p_c), V_m))
V_m_atCrit = V_m_atCrit.subs(a, solve_ab[0][0] ).subs(b, solve_ab[0][1] )

QA_Critical_Sate = Matrix(   [  PR_sol, Eq( diff(PR_sol.rhs, V_m), 0), Eq( diff(PR_sol.rhs, V_m, 2), 0) ] ).subs(T, T_c).subs(V_m, V_mc).subs(p, p_c)
V_cm_sol = solve(QA_Critical_Sate[0], V_mc)[0]


#PR_sol2 = PR_sol.subs(V_mc, V_cm_sol )
#V_m_CubicSol = solve(Cubic_State, V_m)[0].subs(alfa, alfa_PR.subs(kappa, kappa_PR) ).subs(a, solve_ab[0][0] ).subs(b, solve_ab[0][1] ).subs(V_mc, V_cm_sol )


Van_der_Waals_EOS = Eq(p, R*T/(V_m - b)  - a/V_m**2 )

Redlich_Kwong_EOS = Eq(p, R*T/(V_m -b) - a/(T**0.5 * V_m * (V_m + b)))

Soave_Redlich_Kwong_EOS = Redlich_Kwong_EOS.subs(a, a*alfa)



n, s, k, z, alpha_Bose = symbols('n s k z alpha_Bose')
#zeta = summation(1/(n**alpha_Bose), (n, 1, oo) )
Li = summation(z**k/k**(alpha_Bose+1), (k, 1, oo) )


Ideal_Bose_EOS = Eq(p*V_m, R*T* Li/zeta(alpha_Bose) * (T/T_c)**alpha_Bose)


rho_0, rho, A, B, v_D, p_CJ, R_1, R_2, e_0, M_W = symbols("rho_0 rho A B v_D p_CJ R_1 R_2 e_0 M_W")

Jones_Wilkins_Lee_EOS = Eq(p, A*( 1 - omega/R_1/V)*exp(-R_1*V)+B*(1-omega/R_2/V)*exp(-R_2*V) + omega*e_0/V )

JWL_EOS_TNT = Jones_Wilkins_Lee_EOS.subs(V, rho_0/rho).subs(rho, M_W/V_m ).subs(rho_0, 1.63E3).subs(A, 373.8E9).subs(B, 3.747E9).subs(R_1, 4.15).subs(R_2, 0.9).subs(omega, 0.35).subs(e_0, 6E9)







