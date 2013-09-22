#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy import hstack, array
from nympy.linalg import solve
from sympy import Dummy, lambdify


def numeric_right_hand_side(kane, parameters):
    """Returns the right hand side function of the first order ordinary
    differential equations from a KanesMethod system which can be evaluated
    numerically.

    Parameters
    ==========
    kane : sympy.physics.mechanics.KanesMethod
        A Kane's method object in which the mass matrix and forcing terms
        have been computed.
    constants : list of sympy.Symbol
        A list of all of the constant symbols in the equations of motion.

    Returns
    =======
    right_hand_side : function
        A function which computes the derivatives of the states in the form
        `f(x, t, args)`. See the doc string for the generated function.

    Note
    ====
    This function can't handle complex EoMs with specified functions of
    time.

    """

    # TODO : Once SymPy PR #2428 gets taken care of, these dummy variables
    # will no longer be needed.
    dynamic = kane._q + kane._u
    dummy_symbols = [Dummy() for i in dynamic]
    dummy_dict = dict(zip(dynamic, dummy_symbols))
    kindiff_dict = kane.kindiffdict()

    M = kane.mass_matrix_full.subs(kindiff_dict).subs(dummy_dict)
    F = kane.forcing_full.subs(kindiff_dict).subs(dummy_dict)

    M_func = lambdify(dummy_symbols + parameters, M)
    F_func = lambdify(dummy_symbols + parameters, F)

    def right_hand_side(x, t, args):
        """Returns the derivatives of the states given the state values at
        the previous time step, the current time, and any constants.

        Parameters
        ----------
        x : array_like, shape(n,)
            The current state vector.
        t : float
            The current time.
        args : array_like, shape(m,)
            The constants.

        Returns
        -------
        dx : ndarray, shape(n,)
            The derivative of the state at the current time.

        """
        arguments = hstack((x, args))
        dx = array(solve(M_func(*arguments), F_func(*arguments))).T[0]

        return dx

    return right_hand_side
