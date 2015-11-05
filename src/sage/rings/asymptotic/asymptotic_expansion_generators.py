r"""
Common Asymptotic Expansions

.. WARNING::

    As this code is experimental, a warning is thrown when an
    asymptotic ring (or an associated structure) is created for the
    first time in a session (see
    :class:`sage.misc.superseded.experimental`).

    TESTS::

        sage: AsymptoticRing(growth_group='z^ZZ * log(z)^QQ', coefficient_ring=ZZ)
        doctest:...: FutureWarning: This class/method/function is marked as
        experimental. It, its functionality or its interface might change
        without a formal deprecation.
        See http://trac.sagemath.org/17601 for details.
        doctest:...: FutureWarning: This class/method/function is marked as
        experimental. It, its functionality or its interface might change
        without a formal deprecation.
        See http://trac.sagemath.org/17601 for details.
        Asymptotic Ring <z^ZZ * log(z)^QQ> over Integer Ring


Asymptotic expansions in SageMath can be built through the
``asymptotic_expansions`` object. It contains generators for common
asymptotic expressions. For example,
::

    sage: asymptotic_expansions.Stirling('n', precision=5)
    sqrt(2)*sqrt(pi)*e^(n*log(n))*(e^n)^(-1)*n^(1/2) +
    1/12*sqrt(2)*sqrt(pi)*e^(n*log(n))*(e^n)^(-1)*n^(-1/2) +
    1/288*sqrt(2)*sqrt(pi)*e^(n*log(n))*(e^n)^(-1)*n^(-3/2) +
    O(e^(n*log(n))*(e^n)^(-1)*n^(-5/2))

generates the first 5 summands of Stirling's approximation formula for
factorials.

To construct an asymptotic expression manually, you can use the class
:class:`~sage.rings.asymptotic.asymptotic_ring.AsymptoticRing`. See
:doc:`asymptotic ring <asymptotic_ring>` for more details and a lot of
examples.


**Asymptotic Expansions**

.. list-table::
   :class: contentstable
   :widths: 4 12
   :header-rows: 0

   * - :meth:`~AsymptoticExpansionGenerators.Stirling`
     - Stirling's approximation formula for factorials

   * - :meth:`~AsymptoticExpansionGenerators.log_Stirling`
     - the logarithm of Stirling's approximation formula for factorials

   * - :meth:`~AsymptoticExpansionGenerators.Binomial_kn_over_n`
     - an asymptotic expansion of the binomial coefficient


AUTHORS:

- Daniel Krenn (2015)


ACKNOWLEDGEMENT:

- Benjamin Hackl, Clemens Heuberger and Daniel Krenn are supported by the
  Austrian Science Fund (FWF): P 24644-N26.


Classes and Methods
===================
"""

#*****************************************************************************
# Copyright (C) 2015 Daniel Krenn <dev@danielkrenn.at>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.structure.sage_object import SageObject

class AsymptoticExpansionGenerators(SageObject):
    r"""
    A collection of constructors for several common asymptotic expansions.

    A list of all asymptotic expansions in this database is available via tab
    completion. Type "``asymptotic_expansions.``" and then hit tab to see which
    expansions are available.

    The asymptotic expansions currently in this class include:

    - :meth:`~Stirling`
    - :meth:`~log_Stirling`
    - :meth:`~Binomial_kn_over_n`
    """

    @staticmethod
    def Stirling(var, precision=None, skip_constant_factor=False):
        r"""
        Return Stirling's approximation formula for factorials.

        INPUT:

        - ``var`` -- a string for the variable name.

        - ``precision`` -- (default: ``None``) an integer. If ``None``, then
          the default precision of the asymptotic ring is used.

        - ``skip_constant_factor`` -- (default: ``False``) a
          boolean. If set, then the constant factor is left out.
          As a consequence, the coefficient ring of the output changes
          from ``Symbolic Constants Subring`` (if ``False``) to
          ``Rational Field`` (if ``True``).

        OUTPUT:

        An asymptotic expansion.

        EXAMPLES::

            sage: asymptotic_expansions.Stirling('n', precision=5)
            sqrt(2)*sqrt(pi)*e^(n*log(n))*(e^n)^(-1)*n^(1/2) +
            1/12*sqrt(2)*sqrt(pi)*e^(n*log(n))*(e^n)^(-1)*n^(-1/2) +
            1/288*sqrt(2)*sqrt(pi)*e^(n*log(n))*(e^n)^(-1)*n^(-3/2) +
            O(e^(n*log(n))*(e^n)^(-1)*n^(-5/2))
            sage: _.parent()
            Asymptotic Ring <(e^(n*log(n)))^QQ * (e^n)^QQ * n^QQ * log(n)^QQ>
            over Symbolic Constants Subring

        TESTS::

            sage: asymptotic_expansions.Stirling('n', precision=5,
            ....:                                skip_constant_factor=True)
            e^(n*log(n))*(e^n)^(-1)*n^(1/2) +
            1/12*e^(n*log(n))*(e^n)^(-1)*n^(-1/2) +
            1/288*e^(n*log(n))*(e^n)^(-1)*n^(-3/2) +
            O(e^(n*log(n))*(e^n)^(-1)*n^(-5/2))
            sage: _.parent()
            Asymptotic Ring <(e^(n*log(n)))^QQ * (e^n)^QQ * n^QQ * log(n)^QQ>
            over Rational Field
        """
        log_Stirling = AsymptoticExpansionGenerators.log_Stirling(
            var, precision=precision, skip_constant_summand=True)

        P = log_Stirling.parent().change_parameter(
            growth_group='(e^(n*log(n)))^QQ * (e^n)^QQ * n^QQ * log(n)^QQ')
        from sage.functions.log import exp
        result = exp(P(log_Stirling))

        if not skip_constant_factor:
            from sage.symbolic.ring import SR
            SCR = SR.subring(no_variables=True)
            result *= (2*SCR('pi')).sqrt()

        return result


    @staticmethod
    def log_Stirling(var, precision=None, skip_constant_summand=False):
        r"""
        Return the logarithm of Stirling's approximation formula
        for factorials.

        INPUT:

        - ``var`` -- a string for the variable name.

        - ``precision`` -- (default: ``None``) an integer. If ``None``, then
          the default precision of the asymptotic ring is used.

        - ``skip_constant_summand`` -- (default: ``False``) a
          boolean. If set, then the constant summand is left out.
          As a consequence, the coefficient ring of the output changes
          from ``Symbolic Constants Subring`` (if ``False``) to
          ``Rational Field`` (if ``True``).

        OUTPUT:

        An asymptotic expansion.

        EXAMPLES::

            sage: asymptotic_expansions.log_Stirling('n', precision=7)
            n*log(n) - n + 1/2*log(n) + 1/2*log(2*pi) + 1/12*n^(-1)
            - 1/360*n^(-3) + 1/1260*n^(-5) + O(n^(-7))

        TESTS::

            sage: asymptotic_expansions.log_Stirling('n')
            n*log(n) - n + 1/2*log(n) + 1/2*log(2*pi) + 1/12*n^(-1)
            - 1/360*n^(-3) + 1/1260*n^(-5) - 1/1680*n^(-7) + 1/1188*n^(-9)
            - 691/360360*n^(-11) + 1/156*n^(-13) - 3617/122400*n^(-15)
            + 43867/244188*n^(-17) - 174611/125400*n^(-19) + 77683/5796*n^(-21)
            - 236364091/1506960*n^(-23) + 657931/300*n^(-25)
            - 3392780147/93960*n^(-27) + 1723168255201/2492028*n^(-29)
            - 7709321041217/505920*n^(-31) + O(n^(-33))
            sage: _.parent()
            Asymptotic Ring <n^ZZ * log(n)^ZZ> over Symbolic Constants Subring

        ::

            sage: asymptotic_expansions.log_Stirling(
            ....:     'n', precision=7, skip_constant_summand=True)
            n*log(n) - n + 1/2*log(n) + 1/12*n^(-1) - 1/360*n^(-3) +
            1/1260*n^(-5) + O(n^(-7))
            sage: _.parent()
            Asymptotic Ring <n^ZZ * log(n)^ZZ> over Rational Field
        """
        if not skip_constant_summand:
            from sage.symbolic.ring import SR
            coefficient_ring = SR.subring(no_variables=True)
        else:
            from sage.rings.rational_field import QQ
            coefficient_ring = QQ

        from asymptotic_ring import AsymptoticRing
        A = AsymptoticRing(growth_group='%s^ZZ * log(%s)^ZZ' % ((var,)*2),
                           coefficient_ring=coefficient_ring)
        n = A.gen()

        if precision is None:
            precision = A.default_prec

        from sage.functions.log import log
        result = A.zero()
        if precision >= 1:
            result += n * log(n)
        if precision >= 2:
            result += -n
        if precision >= 3:
            result += log(n) / 2
        if precision >= 4 and not skip_constant_summand:
            result += log(2*coefficient_ring('pi')) / 2

        from sage.misc.misc import srange
        from sage.rings.arith import bernoulli
        for k in srange(2, 2*precision - 6, 2):
            result += bernoulli(k) / k / (k-1) / n**(k-1)

        result += (1 / n**(2*precision - 7)).O()
        return result


    @staticmethod
    def Binomial_kn_over_n(var, k, precision=None, skip_constant_factor=False,
                           algorithm=None):
        r"""
        Return the asymptotic expansion of the binomial coefficient
        `kn` choose `n`.

        INPUT:

        - ``var`` -- a string for the variable name.

        - ``k`` -- a number.

        - ``precision`` -- (default: ``None``) an integer. If ``None``, then
          the default precision of the asymptotic ring is used.

        - ``skip_constant_factor`` -- (default: ``False``) a
          boolean. If set, then the constant summand is left out.
          As a consequence, the coefficient ring of the output changes
          from ``Symbolic Constants Subring`` (if ``False``) to
          ``Rational Field`` (if ``True``).

        - ``algorithm`` -- either ``'direct'`` or ``'log'`` (default).

        OUTPUT:

        An asymptotic expansion.

        EXAMPLES::

            sage: asymptotic_expansions.Binomial_kn_over_n('n', k=2, precision=5)
            1/sqrt(pi)*(e^n)^(2*log(2))*n^(-1/2)
            - 1/8/sqrt(pi)*(e^n)^(2*log(2))*n^(-3/2)
            + 1/128/sqrt(pi)*(e^n)^(2*log(2))*n^(-5/2)
            + O((e^n)^(2*log(2))*n^(-7/2))
            sage: _.parent()
            Asymptotic Ring <(e^(n*log(n)))^(Symbolic Constants Subring)
            * (e^n)^(Symbolic Constants Subring)
            * n^(Symbolic Constants Subring)
            * log(n)^(Symbolic Constants Subring)>
            over Symbolic Constants Subring

        ::

            sage: asymptotic_expansions.Binomial_kn_over_n('n', k=3, precision=5)
            1/2*sqrt(3)/sqrt(pi)*(e^n)^(3*log(3) - 2*log(2))*n^(-1/2)
            - 7/144*sqrt(3)/sqrt(pi)*(e^n)^(3*log(3)
            - 2*log(2))*n^(-3/2) + 49/20736*sqrt(3)/sqrt(pi)*(e^n)^(3*log(3)
            - 2*log(2))*n^(-5/2)
            + O((e^n)^(3*log(3) - 2*log(2))*n^(-7/2))

        ::

            sage: asymptotic_expansions.Binomial_kn_over_n('n', k=7/5, precision=5)
            1/2*sqrt(7)/sqrt(pi)*(e^n)^(7/5*log(7/5) - 2/5*log(2/5))*n^(-1/2)
            - 13/112*sqrt(7)/sqrt(pi)*(e^n)^(7/5*log(7/5) - 2/5*log(2/5))*n^(-3/2)
            + 169/12544*sqrt(7)/sqrt(pi)*(e^n)^(7/5*log(7/5) - 2/5*log(2/5))*n^(-5/2)
            + O((e^n)^(7/5*log(7/5) - 2/5*log(2/5))*n^(-7/2))

        TESTS::

            sage: asymptotic_expansions.Binomial_kn_over_n(
            ....:     'n', k=5, precision=5, skip_constant_factor=True)
            1/2*(e^n)^(5*log(5)
            - 4*log(4))*n^(-1/2)
            - 7/160*(e^n)^(5*log(5) - 4*log(4))*n^(-3/2)
            + 49/25600*(e^n)^(5*log(5) - 4*log(4))*n^(-5/2)
            + O((e^n)^(5*log(5) - 4*log(4))*n^(-7/2))
            sage: _.parent()
            Asymptotic Ring <(e^(n*log(n)))^(Symbolic Constants Subring)
            * (e^n)^(Symbolic Constants Subring)
            * n^(Symbolic Constants Subring)
            * log(n)^(Symbolic Constants Subring)>
            over Rational Field
            sage: all(  # long time
            ....:     asymptotic_expansions.Binomial_kn_over_n('n', k=k,
            ....:         precision=5, algorithm='direct').has_same_summands(
            ....:     asymptotic_expansions.Binomial_kn_over_n('n', k=k,
            ....:     precision=5, algorithm='log'))
            ....:     for k in (2, 4))
            True
        """
        if algorithm is None:
            algorithm = 'log'  # 'log' seems to be faster, so we use it
                               # as a default.

        from sage.symbolic.ring import SR
        SCR = SR.subring(no_variables=True)
        try:
            k = SCR.coerce(k)
        except TypeError as e:
            from misc import combine_exceptions
            raise combine_exceptions(
                TypeError('Cannot use k=%s.' % (k,)), e)

        if algorithm == 'direct':
            Stirling = AsymptoticExpansionGenerators.Stirling(
                var, precision=precision, skip_constant_factor=skip_constant_factor)
            n = Stirling.parent().gen()
            result = Stirling.subs(n=k*n) / \
                       (Stirling.subs(n=(k-1)*n) * Stirling)

        if algorithm == 'log':
            log_Stirling = AsymptoticExpansionGenerators.log_Stirling(
                var, precision=precision, skip_constant_summand=True)
            n = log_Stirling.parent().gen()

            result = log_Stirling.subs(n=k*n) - \
                     log_Stirling.subs(n=(k-1)*n) - log_Stirling

            P = log_Stirling.parent().change_parameter(
                growth_group='(e^(n*log(n)))^QQ * (e^n)^QQ * n^QQ * log(n)^QQ',
                coefficient_ring=SCR)
            from sage.functions.log import exp
            result = exp(P.coerce(result))

            if not skip_constant_factor:
                result /= (2*SCR('pi')).sqrt()

            result = result.map_coefficients(
                lambda c: c.canonicalize_radical())

        else:
            raise ValueError('Unknown algorithm %s.' % (algorithm,))

        if skip_constant_factor:
            from sage.rings.rational_field import QQ
            result = result.parent().change_parameter(
                coefficient_ring=QQ)(result / SCR(k.sqrt()))
        return result

# Easy access to the asymptotic expansions generators from the command line:
asymptotic_expansions = AsymptoticExpansionGenerators()
r"""
A collection of several common asymptotic expansions.

This is an instance of :class:`AsymptoticExpansionGenerators` whose documentation
provides more details.
"""
