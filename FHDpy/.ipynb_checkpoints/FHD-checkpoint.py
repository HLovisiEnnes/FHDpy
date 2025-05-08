import snappy
import copy
import numpy as np
import FHDpy.SLP as SLP


'''
Main class
'''

class FHDLong:
    '''
    Computes an intersection sequence presentation for the Heegaard diagram of a 3-manifold represented by a Heegaard word (i.e., an element of the mapping class group of the splitting surface). 
    
    Parameters
    ----------
    alpha_curves_standard : dict
    Dictionary with each key being an alpha curve and its associated value being an SLP of the intersection sequence of a twin of the curve.
    
    alpha_curves_edge : dict
    Dictionary with each key being an alpha curve and its associated value being the edge list of the curve.

    generators_standard : dict
    Dictionary with each key being a generator curve and its associated value being the intersection sequence of the left twin of the curve.
    
    generators_edge : dict
    Dictionary with each key being a generator curve and its associated value being an edge list representation.
    '''
    
    def __init__(self, alpha_curves_standard, alpha_curves_edges, generators_standard, generators_edge):
      
        # Deep copy is important because we will be updating these things and, if not deep copied, the assignments will be only pointers pointing to the same object, which will be updated.
        alpha_curves_standard = copy.deepcopy(alpha_curves_standard)
        self.alpha = copy.deepcopy(alpha_curves_edges.copy())
        self.generators = copy.deepcopy(generators_standard.copy())
        self.generators_edge = copy.deepcopy(generators_edge.copy())
        
        
        # Make generators from twins.
        self.maps = {}
        for edge in generators_standard.keys():
            self.maps[edge.lower()], self.maps[edge.upper()] = self.make_maps(edge, self.generators[edge])        
        
        # Add the inverse of the generators to the generator list.
        # Need to make a new dictionary because we cannot change the length of a dictionary while updating.
        inverse_edges = {}
        for curve in self.generators_edge.keys():
            # Simply add everything with upper letters
            inverse_edges[curve.upper()] = [edge.upper() for edge in self.generators_edge[curve]]
        # Add the new generators to list
        self.generators_edge.update(inverse_edges)

    
        
        # As usual, the alpha curves will be edged.
        self.twins = list(alpha_curves_standard.values())
        
         # Initial diagram is the trivial diagram of S2 x S1.
        self.beta = copy.deepcopy(self.twins)
        
    def make_maps(self, edge, slp):
        '''
        Transforms the intersection sequence of an edge represented generator curve starting at edge into a proper subsititution rule of a right and left Dehn twist about
        the generator by appending the intersected edge at the end of the SLP of the left twin.
        
        Parameters
        ----------
        edge : str
        The intersected edge.
        slp : SLP
        An SLP of the intersection sequence of one of the twins of the curve, starting the tranversing at a cell adjacent to edge. We convention to always use left twins.
        
        Returns
        -------
        map_slp : SLP
        SLP for the substitution rule of the right Dehn twist about the generator for the beta curve intersecting the generator at edge.
        inverse_map_slp : SLP
        SLP for the substitution rule of the left Dehn twist about the generator for the beta curve intersecting the generator at edge.
        '''
        # Add the edge as the last position to the SLP of the twin.
        map_slp = SLP.SLP(slp.list_form + [edge, '#' + str(len(slp.list_form)-1) + '.#' + str(len(slp.list_form))])
        inverse_slp = slp.inverse()
        inverse_map_slp = SLP.SLP(inverse_slp.list_form + [edge, '#' + str(len(inverse_slp.list_form)-1) + '.#' + str(len(inverse_slp.list_form))])
        
        return map_slp, inverse_map_slp
    
    def reset(self):
        '''
        Resests the Heegaard diagram, that is, make the beta curves parallel to the alpha curves.
  
        '''
        self.beta = copy.deepcopy(self.twins)
        return None

    def dehn_twist(self, word, compress = True):
        '''
        Updates the Heegaard diagram by applying the word, in the mapping class group of the surface, to each beta curve.
        
        Parameters
        ----------
        word : str
        Word in the mapping class group of the surface, where each letter is a generator curve in. Lower letters indicate right Dehn twists and upper letters indicate left. No marker of multiplication
        is required. Word is read from left to right (i.e., reading direction).               
        Ex.: 'aBc' represents a right Dehn twist about a, followed by a left Dehn twist about b and a right Dehn twist about c.
        compress : bool, optional
        If compress is True, first compress the word to power notation.
        
        Power notation with ^ is possible. For example, A^k means k applications of a left Dehn twist by the curve a. Only strictly positive powers are implemented, e.g., to make a^{-k} where k > 0,
        one should write A^k instead.
        '''
        if compress:
            word = get_compressed(word)
            
        split_word = list(word) # list(word) is a list where each entry is a character of word.
        
        if any(char.isdigit() for char in split_word): # Check if there are numbers in the words, in which case either there is a power or a curve that contains a number.
            clean_split_word = [] # This will be a version of the split word where each entry is either a power of a curve or a power of a curve.
            i = 0 
            while i < len(split_word):
                if split_word[i] != '^': # If not a power.
                    clean_split_word.append(split_word[i])
                    skip = 0 # Skip will tell how much of the next characters are numbers.
                
                elif split_word[i].isdigit():
                    letter_part = clean_split_word.pop() # Delete the last entry of the clean word as it will be updated to contain the digits part.
                    digit = split_word[i]
                    skip = 0
                    while split_word[i + skip].isdigit():
                        digit += split_word[i + skip] # Add next digit to the curve.
                        skip += 1
                        if (i + skip) >= len(split_word): break # If we finish the word, break.

                    clean_split_word.append(letter_part + digit) # Add curve to the list of clean words.
                
                elif split_word[i] == '^':
                    raised = clean_split_word.pop() # Delete the last entry of the clean word as it will be updated to contain the power part.
                    power = split_word[i]
                    skip = 0
                    while split_word[i + 1 + skip].isdigit():
                        power += split_word[i + 1 + skip] # Add next digit to the power.
                        skip += 1
                        if (i + 1 + skip) >= len(split_word): break # If we finish the word, break.
                    
                    clean_split_word.append(raised + power) # Add power of curve to the list of clean words.
                    
                    # Add the power to the list of maps.

                    # We use Twister convention of right Dehn twists positive and left negative.
                    sign = raised.islower()

                    # Make the power of a Dehn twist a new generator. This is not the fastest way to do this as we call get_power for each distinct power. A smater way would be to look for the
                    # highest power of each single generator in the input word, implement that, and then use it to build smaller powers. This requires changing the SLP a little, we will implement that 
                    # in a next version.
                    power_edges = []
                    for edge in self.generators_edge[raised]: # Get all edges whose of the raisd Dehn twist.
                        self.maps[edge + power] = self.make_maps(edge, self.generators[edge].get_power(int(power[1:])))[0] if sign else self.make_maps(edge.lower(), self.generators[edge.lower()].get_power(int(power[1:])))[1]
                        power_edges.append(edge + power)
                    
                    # Associated the powered edges of the curve to the powered curve.
                    self.generators_edge[raised + power] = power_edges
                    
                i += 1 + skip  # Update i until we go over the full word.
    
            
        else:
            clean_split_word = word
        # For each generator in the Heegaard word read left to right (i.e., inverse of function application).
        for curve in clean_split_word:
            # We use Twister convention of right Dehn twists positive and left negative.
            sign = curve.islower()

            # Get all edges that are in the curve.
            edges = self.generators_edge[curve]

            for edge in edges:
                # Update each beta curve by applying the mapping class.
                intersected_edge = edge.split('^')[0] # If we have a substitution of form a^k, only the a part will be found in the SLP of the intersection sequence. Therefore, we throw away what comes after
                # the ^ symbol.
                for beta in self.beta:
                    # If not a inverse twist, simply substitute each occurence of the edge by the new subsequence. If, however, an inverse twist, we replace its lowered version (i.e., the edge label itself) by
                    # the subsequence.
                    beta.substitute(intersected_edge, self.maps[edge], inplace = True) if sign else beta.substitute(intersected_edge.lower(), self.maps[edge], inplace = True)
           
        return None
    
    def homology(self, matrix = False):
        '''
        Computes the first homology group of the manifold represented by the Heegaard diagram.
        
        Parameters
        ----------
        matrix : bool
        If True, returns a presentation of the group. 
        '''
        presentation_matrix = []
        
        # Iterate over each beta curve.
        for beta in self.beta:  
            beta_relator = []
            
            # Iterate over each alpha curve.
            for alpha in self.alpha.keys():
                # For each alpha curve, adds the number of positive minus the number of negative intersections with each edge.
                 beta_relator.append(sum([beta.signed_count(edge)-beta.signed_count(edge + '*') for edge in self.alpha[alpha]]))
            
                
            # Append the relator to the presentation matrix as a new row.
            presentation_matrix.append(beta_relator)
        
        if matrix: # If matix ==  True, returns the presrntation matrix.
            return presentation_matrix, snappy.AbelianGroup(presentation_matrix)
        else:
            return snappy.AbelianGroup(presentation_matrix)
        
class FHD_genus1(SLP.SLP):
    '''
    Simpler version of FHDLong for the T2 case. It requires no parameters and returns the SLP of beta. 
    '''
    def __init__(self):
        list_form = ['b*', 'c*', '#0.#1']
        gen = {'a': SLP.SLP(['b','c','a','#0.#1', '#3.#2']), 'b': SLP.SLP(['c*', 'a*','b','#0.#1','#3.#2']), 'A': SLP.SLP(['c*','b*','a','#0.#1', '#3.#2']), 'B': SLP.SLP(['a', 'c','b','#0.#1','#3.#2'])}
        
        SLP.SLP.__init__(self, list_form)
        self.gen = gen
            
    def dehn_twist(self, generator):
        for edge in generator:
            # If not a inverse twist, simply substitute each occurence of the edge by the new subsequence. If, however, an inverse twist, we replace its lowered version (i.e., the edge label itself) by
            # the subsequence.
            self.substitute(edge, self.gen[edge], inplace = True) if edge.islower() else self.substitute(edge.lower(), self.gen[edge], inplace = True)
        return None
    
    def homology(self):
        return snappy.AbelianGroup([[self.signed_count('a')-self.signed_count('a*')]])
        

'''
Auxilary functions
'''
def get_compressed(word):
    '''
    Transforms a non-compressed word into a compressed form by perfoming cancelation of adjacent terms (e.g., 'Aa' -> '' and 'aA' -> '') and joining equal terms in powers (e.g., 'aa' -> 'a^2').
    '''
    compressed_word = ''
    last_char = ''
    i = 0
    while i < len(word):
        char = word[i]
        if char.lower() == last_char.lower(): # If the current character equals the last character or its inverse.
            skip = 1
            if skip + i >= len(word): # Avoid querying a value outsiede the length of the string.
                skip = 1
            else:
                while word[i + skip].lower() == last_char.lower():
                    skip += 1
                    if skip + i >= len(word): break
            
            
            subword = last_char + word[i: i + skip] # Subword in which only the character or its inverses occur.
            
            signed_occurences = subword.count(last_char.lower()) - subword.count(last_char.upper()) # Count the number of occurences of the positive minus negative of the symbol.
            
            if signed_occurences == 0: # If a reduction happpens, that is, we can commute a and A to form, a^kA^k, we append nothing.
                compressed_word = compressed_word.removesuffix(last_char)
                last_char = compressed_word[-1] if len(compressed_word) else ''
            elif abs(signed_occurences) == 1: # If the net occurences of the symbol in the subword is +1 or -1, we append either the symbol or its inverse, respectively.
                compressed_word = compressed_word.removesuffix(last_char) # Else, we append ^power, where power is the number of positive minus the negative occurences of the symbol.
                compressed_word += last_char.lower() if signed_occurences > 0 else last_char.upper()
            else:
                compressed_word = compressed_word.removesuffix(last_char) # Else, we append ^power, where power is the number of positive minus the negative occurences of the symbol.
                compressed_word += last_char.lower() + '^' + str(abs(signed_occurences)) if signed_occurences > 0 else last_char.upper() + '^' + str(abs(signed_occurences))

        else: # If the current character has not to do with the previous one, simply append it and make it the new last character.
            compressed_word += char
            last_char = char
            skip = 1
        i += skip
    return compressed_word

def modular_representation(word):
    '''
    Uses the usual representation of the mapping class group of the torus in Z^2 to compute the homology of the Lens' space given by a Heegaard word.
    See Benson Farb and Dan Margalit. A primer on mapping class groups. Vol. 49. Princeton university press, 2011 for details.
    
    Parameters
    ----------
    word : str
    Word in the mapping class group of the surface, where each letter is a generator curve in. Lower letters indicate right Dehn twists and upper letters indicate left. No marker of multiplication
    is required. Word is read from left to right (i.e., reading direction).

    Ex.: 'aBc' represents a right Dehn twist about a, followed by a left Dehn twist about b and a right Dehn twist about c.
    '''
    
    generators = {'A' : np.array([[1,1],[0,1]]), 'B' : np.array([[1,0],[-1,1]]),  'a' : np.array([[1,-1],[0,1]]), 'b' : np.array([[1,0],[1,1]])}
    
    vec = np.array([[1],[0]])
    vec.astype(np.int64)
    
    for curve in word:
        vec = generators[curve] @ vec
        
    return  snappy.AbelianGroup([[int(vec[1][0])]])