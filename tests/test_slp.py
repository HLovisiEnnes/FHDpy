'''
------------------------------------------------------------------------------
Author: Henrique Ennes (https://hlovisiennes.github.io/)
------------------------------------------------------------------------------
Tests for the SLP module.
------------------------------------------------------------------------------
'''
import pytest

from FHDpy import SLP

'''
Fixes SLP.
'''


@pytest.fixture
def fix_slp():
    '''
    Builds SLP.
    '''
    slp_list_form = [
        'a',
        '#0.#0',
        '#1.#1',
        'b',
        '#2.#3',
        '#4.#3.#3.#3',
        '#5.d.d',
        'c',
        '#7*',
        '#6.#8.#8.#8.#8']

    return SLP(slp_list_form)


@pytest.fixture
def fix_uncompressed():
    '''
    Builds uncompressed version of the same SLP.
    '''

    return 'a.a.a.a.b.b.b.b.d.d.c*.c*.c*.c*'


'''
Test functions.
'''


def test_uncompression(fix_slp, fix_uncompressed):
    '''
    Tests uncompression of SLP.
    '''
    uncompressed = fix_slp.get_uncompressed(inplace=False).list_form[-1]
    assert uncompressed == fix_uncompressed


def test_len(fix_slp, fix_uncompressed):
    '''
    Tests the len attribute.
    '''
    assert len(fix_slp) == len(fix_uncompressed.split('.'))


def test_count(fix_slp, fix_uncompressed):
    '''
    Tests the count method.
    '''
    assert fix_slp.count('a') == fix_uncompressed.count('a')
    assert fix_slp.count('c') == fix_uncompressed.count('c')


def test_signed_count(fix_slp, fix_uncompressed):
    '''
    Tests the signed_count method.
    '''
    assert fix_slp.signed_count('c') == fix_uncompressed.count('c.')
    assert fix_slp.signed_count('c*') == fix_uncompressed.count('c*')


def test_inverse(fix_slp):
    '''
    Tests the inverse method.
    '''
    slp_inverse = fix_slp.inverse(inplace=False)
    slp_inverse = slp_inverse.get_uncompressed(inplace=False).list_form[-1]

    uncompresssed_inverse = 'c.c.c.c.d*.d*.b*.b*.b*.b*.a*.a*.a*.a*'

    assert slp_inverse == uncompresssed_inverse


def test_substitution(fix_slp, fix_uncompressed):
    '''
    Tests the substitution method.
    '''
    slp_substituted = fix_slp.substitute('c', 'a', inplace=False)
    slp_substituted = slp_substituted.get_uncompressed(
        inplace=False).list_form[-1]

    uncompressed_substituted = fix_uncompressed.replace('c', 'a')

    assert slp_substituted == uncompressed_substituted


def test_power(fix_slp, fix_uncompressed):
    '''
    Tests the power method.
    '''
    slp_power = fix_slp.get_power(2, inplace=False)
    slp_power = slp_power.get_uncompressed(inplace=False).list_form[-1]

    uncompressed_power = fix_uncompressed
    uncompressed_power += '.' + uncompressed_power

    assert slp_power == uncompressed_power


def test_delete(fix_slp, fix_uncompressed):
    '''
    Tests the delete method.
    '''
    slp_deleted = fix_slp.delete('c', inplace=False)
    slp_deleted = slp_deleted.get_uncompressed(inplace=False).list_form[-1]

    uncompressed_deleted = fix_uncompressed[:-12]

    assert slp_deleted == uncompressed_deleted
