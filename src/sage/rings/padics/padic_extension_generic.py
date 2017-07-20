"""
p-Adic Extension Generic

A common superclass for all extensions of Qp and Zp.

AUTHORS:

- David Roe
"""
from __future__ import absolute_import

#*****************************************************************************
#       Copyright (C) 2007-2013 David Roe <roed.math@gmail.com>
#                               William Stein <wstein@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from .padic_generic import pAdicGeneric
from .padic_base_generic import pAdicBaseGeneric
from sage.rings.number_field.number_field_base import NumberField
from sage.rings.number_field.order import Order
from sage.rings.rational_field import QQ
from sage.structure.richcmp import op_EQ
from functools import reduce
from sage.categories.morphism import Morphism
from sage.categories.sets_with_partial_maps import SetsWithPartialMaps
from sage.categories.integral_domains import IntegralDomains
from sage.categories.fields import Fields
from sage.categories.homset import Hom

class pAdicExtensionGeneric(pAdicGeneric):
    def __init__(self, poly, prec, print_mode, names, element_class):
        """
        Initialization

        EXAMPLES::

            sage: R = Zp(5,5)
            sage: S.<x> = R[]
            sage: f = x^5 + 75*x^3 - 15*x^2 +125*x - 5
            sage: W.<w> = R.ext(f) #indirect doctest
        """
        #type checking done in factory
        self._given_poly = poly
        R = poly.base_ring()
        # We'll deal with the different names better later.
        # Using a tuple here is mostly needed for more general extensions
        # (ie not eisenstein or unramified)
        print_mode['unram_name'] = names[2]
        print_mode['ram_name'] = names[3]
        print_mode['var_name'] = names[0]
        names = names[0]
        pAdicGeneric.__init__(self, R, R.prime(), prec, print_mode, names, element_class)
        self._populate_coercion_lists_(element_constructor=element_class)

    def _coerce_map_from_(self, R):
        """
        Finds coercion maps from R to this ring.

        EXAMPLES::

            sage: R = Zp(5); S.<x> = ZZ[]; f = x^5 + 25*x - 5; W.<w> = R.ext(f)
            sage: L = W.fraction_field()
            sage: w + L(w) #indirect doctest
            2*w + O(w^101)
            sage: w + R(5,2)
            w + w^5 + O(w^10)
        """
        if R is self.base_ring():
            return True

    def _convert_map_from_(self, R):
        """
        Finds conversion maps from R to this ring.

        Currently, a conversion exists if the defining polynomial is the same.

        EXAMPLES::

            sage: R.<a> = Zq(125)
            sage: S = R.change(type='capped-abs', prec=40, print_mode='terse', print_pos=False)
            sage: S(a - 15)
            -15 + a + O(5^20)

        We get conversions from the exact field::

            sage: K = R.exact_field(); K
            Number Field in a with defining polynomial x^3 + 3*x + 3
            sage: R(K.gen())
            a + O(5^20)

        and its maximal order::

            sage: OK = K.maximal_order()
            sage: R(OK.gen(1))
            a + O(5^20)
        """
        cat = None
        if self._implementation == 'NTL' and R == QQ:
            # Want to use DefaultConvertMap
            return None
        if isinstance(R, pAdicExtensionGeneric) and R.defining_polynomial(exact=True) == self.defining_polynomial(exact=True):
            if R.is_field() and not self.is_field():
                cat = SetsWithPartialMaps()
            else:
                cat = R.category()
        elif isinstance(R, Order) and R.number_field().defining_polynomial() == self.defining_polynomial():
            cat = IntegralDomains()
        elif isinstance(R, NumberField) and R.defining_polynomial() == self.defining_polynomial():
            if self.is_field():
                cat = Fields()
            else:
                cat = SetsWithPartialMaps()
        if cat is not None:
            H = Hom(R, self, cat)
            return H.__make_element_class__(DefPolyConversion)(H)

    def __eq__(self, other):
        """
        Return ``True`` if ``self == other`` and ``False`` otherwise.

        We consider two `p`-adic rings or fields to be equal if they are
        equal mathematically, and also have the same precision cap and
        printing parameters.

        EXAMPLES::

            sage: R.<a> = Qq(27)
            sage: S.<a> = Qq(27,print_mode='val-unit')
            sage: R == S
            False
            sage: S.<a> = Qq(27,type='capped-rel')
            sage: R == S
            True
            sage: R is S
            True
        """
        if not isinstance(other, pAdicExtensionGeneric):
            return False

        return (self.ground_ring() == other.ground_ring() and
                self.defining_polynomial() == other.defining_polynomial() and
                self.precision_cap() == other.precision_cap() and
                self._printer.richcmp_modes(other._printer, op_EQ))

    def __ne__(self, other):
        """
        Test inequality.

        EXAMPLES::

            sage: R.<a> = Qq(27)
            sage: S.<a> = Qq(27,print_mode='val-unit')
            sage: R != S
            True
        """
        return not self.__eq__(other)

    #def absolute_discriminant(self):
    #    raise NotImplementedError

    #def discriminant(self):
    #    raise NotImplementedError

    #def is_abelian(self):
    #    raise NotImplementedError

    #def is_normal(self):
    #    raise NotImplementedError

    def degree(self):
        """
        Returns the degree of this extension.

        EXAMPLES::

            sage: R.<a> = Zq(125); R.degree()
            3
            sage: R = Zp(5); S.<x> = ZZ[]; f = x^5 - 25*x^3 + 5; W.<w> = R.ext(f)
            sage: W.degree()
            5
        """
        return self._given_poly.degree()

    def defining_polynomial(self, exact=False):
        """
        Returns the polynomial defining this extension.

        INPUT:

        - ``exact`` -- boolean (default ``False``), whether to return the underlying exact
                       defining polynomial rather than the one with coefficients in the base ring.

        EXAMPLES::

            sage: R = Zp(5,5)
            sage: S.<x> = R[]
            sage: f = x^5 + 75*x^3 - 15*x^2 + 125*x - 5
            sage: W.<w> = R.ext(f)
            sage: W.defining_polynomial()
            (1 + O(5^5))*x^5 + (O(5^6))*x^4 + (3*5^2 + O(5^6))*x^3 + (2*5 + 4*5^2 + 4*5^3 + 4*5^4 + 4*5^5 + O(5^6))*x^2 + (5^3 + O(5^6))*x + (4*5 + 4*5^2 + 4*5^3 + 4*5^4 + 4*5^5 + O(5^6))
            sage: W.defining_polynomial(exact=True)
            x^5 + 75*x^3 - 15*x^2 + 125*x - 5

        .. SEEALSO::

            :meth:`modulus`
            :meth:`exact_field`
        """
        if exact:
            return self._exact_modulus
        else:
            return self._given_poly

    def exact_field(self):
        """
        Return a number field with the same defining polynomial.

        Note that this method always returns a field, even for
        a p-adic ring.

        EXAMPLES::

            sage: R = Zp(5,5)
            sage: S.<x> = R[]
            sage: f = x^5 + 75*x^3 - 15*x^2 +125*x - 5
            sage: W.<w> = R.ext(f)
            sage: W.exact_field()
            Number Field in w with defining polynomial x^5 + 75*x^3 - 15*x^2 + 125*x - 5

        .. SEEALSO::

            :meth:`defining_polynomial`
            :meth:`modulus`
        """
        return self.base_ring().exact_field().extension(self._exact_modulus, self.variable_name())

    def modulus(self, exact=False):
        """
        Returns the polynomial defining this extension.

        INPUT:

        - ``exact`` -- boolean (default ``False``), whether to return the underlying exact
                       defining polynomial rather than the one with coefficients in the base ring.

        EXAMPLES::

            sage: R = Zp(5,5)
            sage: S.<x> = R[]
            sage: f = x^5 + 75*x^3 - 15*x^2 +125*x - 5
            sage: W.<w> = R.ext(f)
            sage: W.modulus()
            (1 + O(5^5))*x^5 + (O(5^6))*x^4 + (3*5^2 + O(5^6))*x^3 + (2*5 + 4*5^2 + 4*5^3 + 4*5^4 + 4*5^5 + O(5^6))*x^2 + (5^3 + O(5^6))*x + (4*5 + 4*5^2 + 4*5^3 + 4*5^4 + 4*5^5 + O(5^6))
            sage: W.modulus(exact=True)
            x^5 + 75*x^3 - 15*x^2 + 125*x - 5

        .. SEEALSO::

            :meth:`defining_polynomial`
            :meth:`exact_field`
        """
        return self.defining_polynomial(exact)

    def ground_ring(self):
        """
        Returns the ring of which this ring is an extension.

        EXAMPLES::

            sage: R = Zp(5,5)
            sage: S.<x> = R[]
            sage: f = x^5 + 75*x^3 - 15*x^2 +125*x - 5
            sage: W.<w> = R.ext(f)
            sage: W.ground_ring()
            5-adic Ring with capped relative precision 5
        """
        return self._given_poly.base_ring()

    def ground_ring_of_tower(self):
        """
        Returns the p-adic base ring of which this is ultimately an
        extension.

        Currently this function is identical to ground_ring(), since
        relative extensions have not yet been implemented.

        EXAMPLES::

            sage: Qq(27,30,names='a').ground_ring_of_tower()
            3-adic Field with capped relative precision 30
        """
        if isinstance(self.ground_ring(), pAdicBaseGeneric):
            return self.ground_ring()
        else:
            return self.ground_ring().ground_ring_of_tower()

    #def is_isomorphic(self, ring):
    #    raise NotImplementedError

    def polynomial_ring(self):
        """
        Returns the polynomial ring of which this is a quotient.

        EXAMPLES::

            sage: Qq(27,30,names='a').polynomial_ring()
            Univariate Polynomial Ring in x over 3-adic Field with capped relative precision 30
        """
        return self._given_poly.parent()

    #def teichmuller(self, x, prec = None):
    #    if prec is None:
    #        prec = self.precision_cap()
    #    x = self(x, prec)
    #    if x.valuation() > 0:
    #        return self(0)
    #    q = self.residue_class_field().order()
    #    u = 1 / self(1 - q, prec)
    #    delta = u * (1 - x ** (q - 1))
    #    xnew = x - x*delta*(1 - q * delta)
    #    while x != xnew:
    #        x = xnew
    #        delta = u*(1-x**(q-1))
    #        xnew = x - x*delta*(1-q*delta)
    #    return x

    def construction(self):
        """
        Returns the functorial construction of this ring, namely,
        the algebraic extension of the base ring defined by the given
        polynomial.

        Also preserves other information that makes this ring unique
        (e.g. precision, rounding, print mode).

        EXAMPLES::

            sage: R.<a> = Zq(25, 8, print_mode='val-unit')
            sage: c, R0 = R.construction(); R0
            5-adic Ring with capped relative precision 8
            sage: c(R0)
            Unramified Extension in a defined by x^2 + 4*x + 2 with capped relative precision 8 over 5-adic Ring
            sage: c(R0) == R
            True
        """
        from sage.categories.pushout import AlgebraicExtensionFunctor as AEF
        print_mode = self._printer.dict()
        return (AEF([self.defining_polynomial(exact=True)], [self.variable_name()],
                    prec=self.precision_cap(), print_mode=self._printer.dict(),
                    implementation=self._implementation),
                self.base_ring())

    def fraction_field(self, print_mode=None):
        r"""
        Returns the fraction field of this extension, which is just
        the extension of base.fraction_field() determined by the
        same polynomial.

        INPUT:

        - print_mode -- a dictionary containing print options.
          Defaults to the same options as this ring.

        OUTPUT:

        - the fraction field of self.

        EXAMPLES::

            sage: U.<a> = Zq(17^4, 6, print_mode='val-unit', print_max_terse_terms=3)
            sage: U.fraction_field()
            Unramified Extension in a defined by x^4 + 7*x^2 + 10*x + 3 with capped relative precision 6 over 17-adic Field
            sage: U.fraction_field({"pos":False}) == U.fraction_field()
            False
        """
        if self.is_field() and print_mode is None:
            return self
        if print_mode is None:
            return self.change(field=True)
        else:
            return self.change(field=True, **print_mode)

    def integer_ring(self, print_mode=None):
        r"""
        Returns the ring of integers of self, which is just the
        extension of base.integer_ring() determined by the same
        polynomial.

        INPUT:

            - print_mode -- a dictionary containing print options.
              Defaults to the same options as this ring.

        OUTPUT:

            - the ring of elements of self with nonnegative valuation.

        EXAMPLES::

            sage: U.<a> = Qq(17^4, 6, print_mode='val-unit', print_max_terse_terms=3)
            sage: U.integer_ring()
            Unramified Extension in a defined by x^4 + 7*x^2 + 10*x + 3 with capped relative precision 6 over 17-adic Ring
            sage: U.fraction_field({"pos":False}) == U.fraction_field()
            False
        """
        #Currently does not support fields with non integral defining polynomials.  This should change when the padic_general_extension framework gets worked out.
        if not self.is_field() and print_mode is None:
            return self
        if print_mode is None:
            return self.change(field=False)
        else:
            return self.change(field=False, **print_mode)

    #def hasGNB(self):
    #    raise NotImplementedError

    def random_element(self):
        """
        Returns a random element of self.

        This is done by picking a random element of the ground ring
        self.degree() times, then treating those elements as
        coefficients of a polynomial in self.gen().

        EXAMPLES::

            sage: R.<a> = Zq(125, 5); R.random_element()
            (3*a^2 + 3*a + 3) + (a^2 + 4*a + 1)*5 + (3*a^2 + 4*a + 1)*5^2 + 
            (2*a^2 + 3*a + 3)*5^3 + (4*a^2 + 3)*5^4 + O(5^5)
            sage: R = Zp(5,3); S.<x> = ZZ[]; f = x^5 + 25*x^2 - 5; W.<w> = R.ext(f)
            sage: W.random_element()
            4 + 3*w + w^2 + 4*w^3 + w^5 + 3*w^6 + w^7 + 4*w^10 + 2*w^12 + 4*w^13 + 3*w^14 + O(w^15)
        """
        return reduce(lambda x,y: x+y,
                      [self.ground_ring().random_element() * self.gen()**i for i in
                           range(self.modulus().degree())],
                      0)

    #def unit_group(self):
    #    raise NotImplementedError

    #def unit_group_gens(self):
    #    raise NotImplementedError

    #def principal_unit_group(self):
    #    raise NotImplementedError

    #def zeta(self, n = None):
    #    raise NotImplementedError

    #def zeta_order(self):
    #    raise NotImplementedError

class DefPolyConversion(Morphism):
    """
    Conversion map between p-adic rings/fields with the same defining polynomial.

    INPUT:

    - ``R`` -- a p-adic extension ring or field.
    - ``S`` -- a p-adic extension ring or field with the same defining polynomial.

    EXAMPLES::

        sage: R.<a> = Zq(125, print_mode='terse')
        sage: S = R.change(prec = 15, type='floating-point')
        sage: a - 1
        95367431640624 + a + O(5^20)
        sage: S(a - 1)
        30517578124 + a + O(5^15)

    ::

        sage: R.<a> = Zq(125, print_mode='terse')
        sage: S = R.change(prec = 15, type='floating-point')
        sage: f = S.convert_map_from(R)
        sage: TestSuite(f).run()
    """
    def _call_(self, x):
        """
        Use the polynomial associated to the element to do the conversion.

        EXAMPLES::

            sage: S.<x> = ZZ[]
            sage: W.<w> = Zp(3).extension(x^4 + 9*x^2 + 3*x - 3)
            sage: z = W.random_element()
            sage: repr(W.change(print_mode='digits')(z))
            '...20112102111011011200001212210222202220100111100200011222122121202100210120010120'
        """
        S = self.codomain()
        Sbase = S.base_ring()
        L = x.polynomial().list()
        if L and not (len(L) == 1 and L[0].is_zero()): # ZZ_pX elements 
            return S([Sbase(c) for c in L])
        else:
            # Inexact zeros need to be handled separately
            if isinstance(x.parent(), pAdicExtensionGeneric):
                return S(0, x.precision_absolute())
            else:
                return S(0)
