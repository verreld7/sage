r"""
Documentation for the matroids in the catalog

This module contains implementations for many of the functions accessible
through :mod:`matroids. <sage.matroids.matroids_catalog>` and
:mod:`matroids.named_matroids. <sage.matroids.matroids_catalog>`
(type those lines in Sage and hit ``tab`` for a list).

The docstrings include educational information about each named matroid with
the hopes that this class can be used as a reference. However, for a more
comprehensive list of properties we refer to the appendix of [Oxl2011]_.
"""
from sage.matroids.database.OxleyMatroids import U24, U25, U35, K4, Whirl3, Q6, P6, U36, R6, Fano, FanoDual, NonFano,NonFanoDual, O7, P7, AG32, AG32prime, R8, F8, Q8, L8, S8, Vamos, T8, J, P8, P8pp, Wheel4, Whirl4, K33dual, K33, AG23, TernaryDowling3, Pappus, NonPappus, K5, K5dual, R10, R12, T12, PG23
from sage.matroids.database.BrettellMatroids import RelaxedNonFano, TippedFree3spike, AG23minusDY, TQ8, P8p, KP8, Sp8, Sp8pp, LP8, WQ8, BB9, TQ9, TQ9p, M8591, PP9, BB9gDY, A9, FN9, FX9, KR9, KQ9, UG10, FF10, GP10, FZ10, UQ10, FP10, TQ10, FY10, PP10, FU10, D10, UK10, PK10, GK10, FT10, TK10, KT10, TU10, UT10, FK10, KF10, FA11, FR12, GP12, FQ12, FF12, FZ12, UQ12, FP12, FS12, UK12, UA12, AK12, FK12, KB12, AF12, NestOfTwistedCubes, XY13, N3, N3pp, UP14, VP14, FV14, OW14, FM14, FA15, N4
from sage.matroids.database.VariousMatroids import NonVamos, TicTacToe, Q10, N1, N2, BetsyRoss, Block_9_4, Block_10_5, ExtendedBinaryGolayCode, ExtendedTernaryGolayCode, AG23minus, NotP8, D16, Terrahawk, R9A, R9B, P9