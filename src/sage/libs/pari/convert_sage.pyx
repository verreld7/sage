"""
Convert PARI objects to/from Flint objects

Utility function to convert PARI ``GEN``s to/from flint types (``mpz_t``,
``mpq_t``, and matrix types over them).

AUTHORS:

- Luca De Feo (2016-09-06): Separate Sage-specific components from
  generic C-interface in ``PariInstance`` (:trac:`20241`)
"""

#*****************************************************************************
#       Copyright (C) 2016 Luca De Feo <luca.defeo@polytechnique.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from __future__ import absolute_import, division, print_function

include "cysignals/signals.pxi"

from sage.libs.gmp.all cimport *
from sage.libs.flint.fmpz cimport fmpz_get_mpz, COEFF_IS_MPZ, COEFF_TO_PTR
from sage.libs.flint.fmpz_mat cimport *

from .paridecl cimport *
from .stack cimport new_gen

cdef gen new_gen_from_mpz_t(mpz_t value):
    """
    Create a new gen from a given MPIR-integer ``value``.

    EXAMPLES::

        sage: pari(42)       # indirect doctest
        42

    TESTS:

    Check that the hash of an integer does not depend on existing
    garbage on the stack (:trac:`11611`)::

        sage: foo = pari(2^(32*1024));  # Create large integer to put PARI stack in known state
        sage: a5 = pari(5);
        sage: foo = pari(0xDEADBEEF * (2^(32*1024)-1)//(2^32 - 1));  # Dirty PARI stack
        sage: b5 = pari(5);
        sage: a5.__hash__() == b5.__hash__()
        True
    """
    sig_on()
    return new_gen(_new_GEN_from_mpz_t(value))

cdef inline GEN _new_GEN_from_mpz_t(mpz_t value):
    r"""
    Create a new PARI ``t_INT`` from a ``mpz_t``.

    For internal use only; this directly uses the PARI stack.
    One should call ``sig_on()`` before and ``sig_off()`` after.
    """
    cdef unsigned long limbs = mpz_size(value)

    cdef GEN z = cgeti(limbs + 2)
    # Set sign and "effective length"
    z[1] = evalsigne(mpz_sgn(value)) + evallgefint(limbs + 2)
    mpz_export(int_LSW(z), NULL, -1, sizeof(long), 0, 0, value)

    return z

cdef inline GEN _new_GEN_from_fmpz_t(fmpz_t value):
    r"""
    Create a new PARI ``t_INT`` from a ``fmpz_t``.

    For internal use only; this directly uses the PARI stack.
    One should call ``sig_on()`` before and ``sig_off()`` after.
    """
    if COEFF_IS_MPZ(value[0]):
        return _new_GEN_from_mpz_t(COEFF_TO_PTR(value[0]))
    else:
        return stoi(value[0])

cdef gen new_gen_from_mpq_t(mpq_t value):
    """
    Create a new gen from a given MPIR-rational ``value``.

    EXAMPLES::

        sage: pari(-2/3)
        -2/3
        sage: pari(QQ(42))
        42
        sage: pari(QQ(42)).type()
        't_INT'
        sage: pari(QQ(1/42)).type()
        't_FRAC'

    TESTS:

    Check that the hash of a rational does not depend on existing
    garbage on the stack (:trac:`11854`)::

        sage: foo = pari(2^(32*1024));  # Create large integer to put PARI stack in known state
        sage: a5 = pari(5/7);
        sage: foo = pari(0xDEADBEEF * (2^(32*1024)-1)//(2^32 - 1));  # Dirty PARI stack
        sage: b5 = pari(5/7);
        sage: a5.__hash__() == b5.__hash__()
        True
    """
    sig_on()
    return new_gen(_new_GEN_from_mpq_t(value))

cdef inline GEN _new_GEN_from_mpq_t(mpq_t value):
    r"""
    Create a new PARI ``t_INT`` or ``t_FRAC`` from a ``mpq_t``.

    For internal use only; this directly uses the PARI stack.
    One should call ``sig_on()`` before and ``sig_off()`` after.
    """
    cdef GEN num = _new_GEN_from_mpz_t(mpq_numref(value))
    if mpz_cmpabs_ui(mpq_denref(value), 1) == 0:
        # Denominator is 1, return the numerator (an integer)
        return num
    cdef GEN denom = _new_GEN_from_mpz_t(mpq_denref(value))
    return mkfrac(num, denom)

cdef gen new_gen_from_padic(long ordp, long relprec,
                            mpz_t prime, mpz_t p_pow, mpz_t unit):
    cdef GEN z
    sig_on()
    z = cgetg(5, t_PADIC)
    z[1] = evalprecp(relprec) + evalvalp(ordp)
    set_gel(z, 2, _new_GEN_from_mpz_t(prime))
    set_gel(z, 3, _new_GEN_from_mpz_t(p_pow))
    set_gel(z, 4, _new_GEN_from_mpz_t(unit))
    return new_gen(z)

cdef GEN _new_GEN_from_fmpz_mat_t(fmpz_mat_t B, Py_ssize_t nr, Py_ssize_t nc):
    r"""
    Create a new PARI ``t_MAT`` with ``nr`` rows and ``nc`` columns
    from a ``mpz_t**``.

    For internal use only; this directly uses the PARI stack.
    One should call ``sig_on()`` before and ``sig_off()`` after.
    """
    cdef GEN x
    cdef GEN A = zeromatcopy(nr, nc)
    cdef Py_ssize_t i, j
    for i in range(nr):
        for j in range(nc):
            x = _new_GEN_from_fmpz_t(fmpz_mat_entry(B,i,j))
            set_gcoeff(A, i+1, j+1, x)  # A[i+1, j+1] = x (using 1-based indexing)
    return A

cdef GEN _new_GEN_from_fmpz_mat_t_rotate90(fmpz_mat_t B, Py_ssize_t nr, Py_ssize_t nc):
    r"""
    Create a new PARI ``t_MAT`` with ``nr`` rows and ``nc`` columns
    from a ``mpz_t**`` and rotate the matrix 90 degrees
    counterclockwise.  So the resulting matrix will have ``nc`` rows
    and ``nr`` columns.  This is useful for computing the Hermite
    Normal Form because Sage and PARI use different definitions.

    For internal use only; this directly uses the PARI stack.
    One should call ``sig_on()`` before and ``sig_off()`` after.
    """
    cdef GEN x
    cdef GEN A = zeromatcopy(nc, nr)
    cdef Py_ssize_t i, j
    for i in range(nr):
        for j in range(nc):
            x = _new_GEN_from_fmpz_t(fmpz_mat_entry(B,i,nc-j-1))
            set_gcoeff(A, j+1, i+1, x)  # A[j+1, i+1] = x (using 1-based indexing)
    return A

cdef gen integer_matrix(fmpz_mat_t B, Py_ssize_t nr, Py_ssize_t nc, bint permute_for_hnf):
    """
    EXAMPLES::

        sage: matrix(ZZ,2,[1..6])._pari_()   # indirect doctest
        [1, 2, 3; 4, 5, 6]
    """
    sig_on()
    cdef GEN g
    if permute_for_hnf:
        g = _new_GEN_from_fmpz_mat_t_rotate90(B, nr, nc)
    else:
        g = _new_GEN_from_fmpz_mat_t(B, nr, nc)
    return new_gen(g)

cdef GEN _new_GEN_from_mpq_t_matrix(mpq_t** B, Py_ssize_t nr, Py_ssize_t nc):
    cdef GEN x
    # Allocate zero matrix
    cdef GEN A = zeromatcopy(nr, nc)
    cdef Py_ssize_t i, j
    for i in range(nr):
        for j in range(nc):
            x = _new_GEN_from_mpq_t(B[i][j])
            set_gcoeff(A, i+1, j+1, x)  # A[i+1, j+1] = x (using 1-based indexing)
    return A

cdef gen rational_matrix(mpq_t** B, Py_ssize_t nr, Py_ssize_t nc):
    """
    EXAMPLES::

        sage: matrix(QQ,2,[1..6])._pari_()   # indirect doctest
        [1, 2, 3; 4, 5, 6]
    """
    sig_on()
    cdef GEN g = _new_GEN_from_mpq_t_matrix(B, nr, nc)
    return new_gen(g)

cdef inline void INT_to_mpz(mpz_ptr value, GEN g):
    """
    Store a PARI ``t_INT`` as an ``mpz_t``.
    """
    if typ(g) != t_INT:
        pari_err(e_TYPE, <char*>"conversion to mpz", g)

    cdef long size = lgefint(g) - 2
    mpz_import(value, size, -1, sizeof(long), 0, 0, int_LSW(g))

    if signe(g) < 0:
        mpz_neg(value, value)

cdef void INTFRAC_to_mpq(mpq_ptr value, GEN g):
    """
    Store a PARI ``t_INT`` or ``t_FRAC`` as an ``mpq_t``.
    """
    if typ(g) == t_FRAC:
        INT_to_mpz(mpq_numref(value), gel(g, 1))
        INT_to_mpz(mpq_denref(value), gel(g, 2))
    elif typ(g) == t_INT:
        INT_to_mpz(mpq_numref(value), g)
        mpz_set_ui(mpq_denref(value), 1)
    else:
        pari_err(e_TYPE, <char*>"conversion to mpq", g)
