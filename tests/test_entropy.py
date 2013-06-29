#!/usr/bin/env python2.7
import sys, os
sys.path.append('..')

import glob
import numpy
from numpy import matrix, array
from cogent import LoadSeqs, DNA
from cogent.core.alignment import DenseAlignment
from cogent.util.unit_test import TestCase, main
from cogent.align.weights.util import AlnToProfile
from mutation_motif.entropy import is_valid, get_ret, as_freq_matrix, get_entropy_terms, get_mit

class TestEntropy(TestCase):
    ref_aln = LoadSeqs('data/entropy/ref.fasta', aligned=DenseAlignment, 
                       moltype=DNA)
    ref_data = ref_aln.SeqData
    
    ctl_aln = LoadSeqs('data/entropy/control.fasta', aligned=DenseAlignment, 
                       moltype=DNA)
    ctl_data = ctl_aln.SeqData
    
    gap_aln = LoadSeqs('data/entropy/gap.fasta', aligned=DenseAlignment, 
                       moltype=DNA)
    gap_data = gap_aln.SeqData
    
    def test_validity(self):
        """returns True if all elements satisfy 0 <= e < 4
        returns False if any element does not satisfy 0 <= e < 4
        """
        self.assertTrue(is_valid(self.ref_data))
        self.assertFalse(is_valid(self.gap_data))
    
    def test_invalid_data_matrix(self):
        """raise AssertionError if data is not valid"""
        self.assertRaises(AssertionError, as_freq_matrix, self.gap_data, 
                          pseudocount=0, check_valid=True)
    
    def test_freq_matrix_pc0(self):
        """returns the correct frequency matrix when the pseudocount=0"""
        matrix = as_freq_matrix(self.ref_data, pseudocount=0, 
                                check_valid=True)
        
        expect_matrix = array([[0.2, 0.2], 
                               [0.6, 0.5], 
                               [0.1, 0.3], 
                               [0.1, 0]])
        
        numpy.testing.assert_equal(matrix, expect_matrix)
        #self.assertEqual(matrix, expect_matrix)
        
    def test_freq_matrix_pc1(self):
        """returns the correct frequency matrix when the pseudocount=1"""
        matrix = as_freq_matrix(self.ref_data, pseudocount=1, 
                                check_valid=True).round(decimals=5)
        
        expect_matrix = array([[0.21429, 0.21429], 
                               [0.5, 0.42857], 
                               [0.14286, 0.28571], 
                               [0.14286, 0.07143]])
        
        numpy.testing.assert_equal(matrix, expect_matrix)
    
    def test_get_entropy_terms_pc0(self):
        """returns the correct entropy terms when the pseudocount=0"""
        et = get_entropy_terms(self.ref_data, pseudocount=0, 
                                   check_valid=True).round(decimals=5)
        
        expect_et = array([[0.46439, 0.46439],
                           [0.44218, 0.5], 
                           [0.33219, 0.52109], 
                           [0.33219, float('nan')]])
        
        numpy.testing.assert_equal(et, expect_et)
        
    def test_get_entropy_terms_pc1(self):
        """returns the correct entropy terms when the pseudocount=1"""
        et = get_entropy_terms(self.ref_data, pseudocount=1, 
                                check_valid=True).round(decimals=5)
        
        expect_et = array([[0.47623, 0.47623], 
                           [0.5, 0.52388], 
                           [0.40105, 0.51639], 
                           [0.40105, 0.27195]])
        
        numpy.testing.assert_equal(et, expect_et)
    
    def test_get_mit_pc0(self):
        """returns the correct MI terms when the pseudocount=0"""
        mit = get_mit(self.ref_data, pseudocount=0, 
                                   check_valid=True).round(decimals=5)
        
        expect_mit = array([[0.03561, 0.03561],
                            [0.05782, 0], 
                            [0.16781, -0.02109], 
                            [0.16781, float('nan')]])
        
        numpy.testing.assert_equal(mit, expect_mit)
        
    def test_get_mit_pc1(self):
        """returns the correct MI terms when the pseudocount=1"""
        mit = get_mit(self.ref_data, pseudocount=1, 
                                check_valid=True).round(decimals=5)
        
        expect_mit = array([[0.02377, 0.02377], 
                            [0, -0.02388], 
                            [0.09895, -0.01639], 
                            [0.09895, 0.22805]])
        
        numpy.testing.assert_equal(mit, expect_mit)
    
    def test_get_ret_pc0(self):
        """returns the correct ret terms when the pseudocount=0"""
        ret = get_ret(self.ref_data, self.ctl_data, pseudocount=0, 
                      check_valid=True).round(decimals=5)
        
        expect_ret = array([[0, 0.2],
                            [0.15782, 1.16096], 
                            [0, 0.47549], 
                            [-0.1, float('nan')]])
        
        numpy.testing.assert_equal(ret, expect_ret)
        
    def test_get_ret_pc1(self):
        """returns the correct ret terms when the pseudocount=1"""
        ret = get_ret(self.ref_data, self.ctl_data, pseudocount=1, 
                      check_valid=True).round(decimals=5)
        
        expect_ret = array([[0, 0.12535], 
                            [0.11120, 0.67927], 
                            [0, 0.28571], 
                            [-0.08357, -0.21429]])
        
        numpy.testing.assert_equal(ret, expect_ret)

if __name__ == '__main__':
    main()
