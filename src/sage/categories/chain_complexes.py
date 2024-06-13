# sage_setup: distribution = sagemath-categories
"""
Category of chain complexes
"""

#*****************************************************************************
#  Copyright (C) 2007 Robert Bradshaw
#                2009 Mike Hansen
#                2013 Volker Braun
#                2013, 2015 Travis Scrimshaw
#                2021 Michael Jung
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.categories.category_types import Category_module
from sage.categories.commutative_additive_groups import CommutativeAdditiveGroups
from sage.categories.functor import Functor
from sage.misc.abstract_method import abstract_method


#############################################################
# ChainComplex
#############################################################
class ChainComplexes(Category_module):
    """
    The category of all chain complexes over a base ring.

    EXAMPLES::

        sage: ChainComplexes(RationalField())
        Category of chain complexes over Rational Field
        sage: ChainComplexes(Integers(9))
        Category of chain complexes over Ring of integers modulo 9

     TESTS::

        sage: TestSuite(ChainComplexes(RationalField())).run()
    """

    def super_categories(self):
        """
        EXAMPLES::

            sage: ChainComplexes(Integers(9)).super_categories()
            [Category of modules over Ring of integers modulo 9]
        """
        from sage.categories.fields import Fields
        from sage.categories.modules import Modules
        from sage.categories.vector_spaces import VectorSpaces
        base_ring = self.base_ring()
        if base_ring in Fields():
            return [VectorSpaces(base_ring)]
        return [Modules(base_ring)]

    class ParentMethods:
        @abstract_method
        def homology(self, n=None):
            r"""
            Return the homology of the chain complex.

            INPUT:

            - ``n`` -- (default: ``None``) degree of the homology; if none is
              provided, the direct sum homology will be used

            EXAMPLES::

                sage: # needs sage.modules
                sage: C = ChainComplex({0: matrix(ZZ, 2, 3, [3, 0, 0, 0, 0, 0])})
                sage: C.homology(0)
                Z x Z
                sage: C.homology(1)
                Z x C3
                sage: C.homology(2)
                0

            ::

                sage: # needs sage.combinat sage.modules
                sage: A.<x,y,z> = GradedCommutativeAlgebra(QQ, degrees=(2, 2, 3))
                sage: C = A.cdg_algebra({z: x*y})
                sage: C.homology(0)
                Free module generated by {[1]} over Rational Field
                sage: C.homology(1)
                Free module generated by {} over Rational Field
                sage: C.homology(2)
                Free module generated by {[x], [y]} over Rational Field
                sage: C.homology(3)
                Free module generated by {} over Rational Field
                sage: C.homology(4)
                Free module generated by {[x^2], [y^2]} over Rational Field
            """

        @abstract_method
        def differential(self, *args, **kwargs):
            r"""
            Return the differentials (or boundary maps) of the chain complex.

            EXAMPLES::

                sage: C = ChainComplex({0: matrix(ZZ, 2, 3, [3, 0, 0, 0, 0, 0])})       # needs sage.modules
                sage: C.differential(0)                                                 # needs sage.modules
                [3 0 0]
                [0 0 0]

            ::

                sage: A.<x,y,z> = GradedCommutativeAlgebra(QQ, degrees=(2, 2, 3))       # needs sage.combinat sage.modules
                sage: C = A.cdg_algebra({z: x*y})                                       # needs sage.combinat sage.modules
                sage: C.differential()                                                  # needs sage.combinat sage.modules
                Differential of Commutative Differential Graded Algebra with
                 generators ('x', 'y', 'z') in degrees (2, 2, 3) over Rational Field
                  Defn: x --> 0
                        y --> 0
                        z --> x*y
            """

        @abstract_method(optional=True)
        def lift_from_homology(self, x):
            r"""
            Lift the homology element ``x`` to the corresponding module.

            EXAMPLES::

                sage: # needs sage.symbolic
                sage: E3 = EuclideanSpace(3)
                sage: C = E3.de_rham_complex()
                sage: one = C.homology().one()
                sage: C.lift_from_homology(one)
                Mixed differential form one on the Euclidean space E^3
            """

        def reduce_to_homology(self, x, n=None):
            r"""
            Reduce a cycle to the corresponding quotient in homology.

            INPUT:

            - ``x`` -- a cycle
            - ``n`` -- (default: ``None``) degree of the homology; if none is
              provided, the direct sum homology will be used

            EXAMPLES::

                sage: # needs sage.symbolic
                sage: E3 = EuclideanSpace(3)
                sage: C = E3.de_rham_complex()
                sage: one = C.one()
                sage: C.reduce_to_homology(one)
                [one]
            """
            try:
                # try coercion
                return self.homology(n)(x)
            except TypeError:
                # if not, this methods needs to be overwritten by parent
                raise NotImplementedError


class HomologyFunctor(Functor):
    r"""
    Homology functor.

    INPUT:

    - ``domain`` -- must be a category of chain complexes
    - ``n`` -- (default: ``None``) degree of the homology; if none is provided,
      the direct sum homology will be used

    EXAMPLES::

        sage: C = ChainComplex({0: matrix(ZZ, 2, 3, [3, 0, 0, 0, 0, 0])})               # needs sage.modules
        sage: H = HomologyFunctor(ChainComplexes(ZZ), 1)
        sage: H(C)                                                                      # needs sage.modules
        Z x C3

    ::

        sage: A.<x,y,z> = GradedCommutativeAlgebra(QQ, degrees=(2, 2, 3))               # needs sage.combinat sage.modules
        sage: C = A.cdg_algebra({z: x*y})                                               # needs sage.combinat sage.modules
        sage: H = HomologyFunctor(ChainComplexes(QQ), 2)
        sage: H(C)                                                                      # needs sage.combinat sage.modules
        Free module generated by {[x], [y]} over Rational Field

    Applying to a chain map::

        sage: # needs sage.graphs sage.modules
        sage: S = simplicial_complexes.Sphere(1); S
        Minimal triangulation of the 1-sphere
        sage: SCC = S.chain_complex()
        sage: SCC.differential()
        {0: [],
         1: [-1 -1  0]
            [ 1  0 -1]
            [ 0  1  1],
         2: []}
        sage: f = {0: zero_matrix(ZZ,3,3), 1: zero_matrix(ZZ,3,3)}
        sage: G = Hom(SCC, SCC)
        sage: x = G(f)
        sage: H = HomologyFunctor(ChainComplexes(ZZ), 1)
        sage: H(SCC)
        Z
        sage: H(x)
        Generic morphism:
          From: Z
          To:   Z
    """
    def __init__(self, domain, n=None):
        r"""
        Construct the homology functor.

        TESTS::

            sage: H = HomologyFunctor(ChainComplexes(QQ), 1); H
            Functor from Category of chain complexes over Rational Field to
             Category of commutative additive groups
        """
        if not isinstance(domain, ChainComplexes):
            raise TypeError(f'{domain} must be a category of chain complexes')
        codomain = CommutativeAdditiveGroups()
        super().__init__(domain, codomain)
        self._n = n

    def _apply_functor(self, x):
        r"""
        Apply ``self`` to a chain complex.

        TESTS::

            sage: C = ChainComplex({0: matrix(ZZ, 2, 3, [3, 0, 0, 0, 0, 0])})           # needs sage.modules
            sage: H = HomologyFunctor(ChainComplexes(ZZ), 1)
            sage: H._apply_functor(C)                                                   # needs sage.modules
            Z x C3
        """
        return x.homology(self._n)

    def _apply_functor_to_morphism(self, f):
        r"""
        Apply ``self`` to a chain map.

        TESTS::

            sage: # needs sage.symbolic
            sage: E3 = EuclideanSpace(3)
            sage: C = E3.de_rham_complex()
            sage: id = Hom(C, C).identity()
            sage: H = HomologyFunctor(ChainComplexes(SR))
            sage: id_star = H(id); id_star
            Generic endomorphism of De Rham cohomology ring on the
             Euclidean space E^3
            sage: one = H(C).one()
            sage: id_star(one)
            [one]
        """
        from sage.categories.homset import Hom
        from sage.categories.morphism import SetMorphism

        domain = f.domain()
        codomain = f.codomain()
        lift = domain.lift_from_homology
        reduce = codomain.reduce_to_homology
        apply_f_star = lambda x: reduce(f(lift(x)), self._n)
        return SetMorphism(Hom(domain.homology(self._n),
                               codomain.homology(self._n),
                               CommutativeAdditiveGroups()),
                           apply_f_star)
