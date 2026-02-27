'''
------------------------------------------------------------------------------
Author: Henrique Ennes (https://hlovisiennes.github.io/)
------------------------------------------------------------------------------
Tests for the FHD module.
------------------------------------------------------------------------------
'''
import pytest
import snappy

import FHDpy


@pytest.fixture
def fix_sphere():
    '''
    Fixes a genus 1 diagram of a sphere.
    '''
    alpha_curves_standard = {'a': FHDpy.SLP(['b*'])}
    alpha_curves_edges = {'a': ['a']}
    generators_standard = {'a': FHDpy.SLP(['b']), 'b': FHDpy.SLP(['a*'])}
    generators_edge = {'a': ['a'], 'b': ['b']}
    beta = [FHDpy.SLP(['a'])]

    return FHDpy.FHDLong(alpha_curves_standard,
                         alpha_curves_edges,
                         generators_standard,
                         generators_edge,
                         beta=beta)


@pytest.fixture
def fix_s2s1():
    '''
    Fixes a genus 1 diagram of S^2 x S^1.
    '''
    alpha_curves_standard = {'a': FHDpy.SLP(['b*'])}
    alpha_curves_edges = {'a': ['a']}
    generators_standard = {'a': FHDpy.SLP(['b']), 'b': FHDpy.SLP(['a*'])}
    generators_edge = {'a': ['a'], 'b': ['b']}
    beta = [FHDpy.SLP(['b'])]

    return FHDpy.FHDLong(alpha_curves_standard,
                         alpha_curves_edges,
                         generators_standard,
                         generators_edge,
                         beta=beta)


@pytest.fixture
def genus2_splitting():
    '''
    Fixes a genus 2 splitting of (S^2 x S^1)^2.
    '''
    alpha_curves_standard = {'a': FHDpy.SLP(['b']), 'e': FHDpy.SLP(['d*'])}
    alpha_curves_edges = {'a': ['a'], 'e': ['e']}
    generators_standard = {'a': FHDpy.SLP(['b*']),
                           'b': FHDpy.SLP(['c*', 'a', '#0.#1']),
                           'c': FHDpy.SLP(['b', 'd', '#0.#1']),
                           'd': FHDpy.SLP(['c*', 'e*', '#0.#1']),
                           'e': FHDpy.SLP(['d'])}
    generators_edge = {'a': ['a'], 'b': ['b'],
                       'c': ['c'], 'd': ['d'], 'e': ['e']}

    return FHDpy.FHDLong(alpha_curves_standard,
                         alpha_curves_edges,
                         generators_standard,
                         generators_edge)


'''
Test functions.
'''


def test_fundamental_group(fix_sphere):
    '''
    Checks if the fundmanental group of the sphere is trivial.
    '''
    assert fix_sphere.fundamental_group().relators_explicit == ['x0']


def test_gluing(fix_s2s1, genus2_splitting):
    '''
    Checks if the Dehn twist along the curve 'a' is correct.
    '''
    # Genus 1.
    gluing = 'bAbaa'

    fhd = fix_s2s1
    fhd.dehn_twist(gluing)

    fhd_genus_1 = FHDpy.FHD_genus1()
    fhd_genus_1.dehn_twist(gluing)

    surface = snappy.twister.Surface('S_1')
    manifold = surface.splitting(gluing=gluing, handles='a*A')

    assert fhd.homology() == manifold.homology()
    assert fhd.homology() == FHDpy.modular_representation(gluing)
    assert fhd.homology() == fhd_genus_1.homology()

    # Genus 2.
    gluing = 'aBcDeaabbbb'

    fhd = genus2_splitting
    fhd.dehn_twist(gluing)

    surface = snappy.twister.Surface('S_2')
    manifold = surface.splitting(gluing=gluing, handles='a*e*A*E', optimize=False)

    assert fhd.homology() == manifold.homology()
