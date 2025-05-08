import copy

class SLP:
    '''
    SLP of the sequence xn are lists of strings, which we call list forms, with each string of form 'x1.x2.x3....xn', where 'xi' are known as symbols. Each symbol can be 
    - simple: a variable starting with a letter that belongs to the alphabet, including the empty letter ''
        Ex.: 'a', 'A1', 'A1*',''
        
    - proper assignment: a variable that refers to a previous assignment in the SLP of form '#Integer'
        Ex.: '#3'
    
    The symbol * is reserved for negations
    Ex.: 'A3*' = A3^{-1}, '#3*' = (#3)^{-1}
    
    The symbol '.' is reserved for multiplication and power in the SLP and should not be used in symbols.
    
    Parameters
    ----------
    list_form : list
    A list of strings, where each string is either a simple assignment, a proper assignment, a product of assignments or a negative of an assignment. 
    '''
    def __init__(self, slp):
        self.list_form = slp
    
    
    '''
    Basic operations
    '''
    
    
    def __str__(self):
        '''
        Print list form,
        
        Ex.: print(SLP(['x','y','#0.#1']))
        >> 0. x
        1. y
        2. #0.#1
        
        Returns
        -------
        None
        '''
        for i,el in enumerate(self.list_form):
            if i == 0:
                print_form = '0. ' + el 
            else:
                print_form += '\n' + str(i) + '. ' + el
        return print_form
    
    
    def __len__(self):
        '''
        Get lenght of the represented word.
        
        Ex.: len(SLP(['x','y','#0.#1.x.x*'])) = 4
        
        Returns
        -------
        length : int
        Length of the SLP, defined as the toal length of the final sequence when uncompressed.
        
        The gernal case is implemented using dynamic programming (memorization), only faster than counting occurances of last sequence if SLP is compressed, otherwise get length on the
        last assignment.
        '''
        if not '#' in self.list_form[-1]: # If the SLP is not compressed.
            return len(self.list_form[-1].split('.')) if self.list_form[-1] != '' else 0
        
        else:
            past_indexes = [] # List of the number of occurances of the symbol for each assignment, counting proper assignments.
            current_index = -1 # Keeps track of current index to call error, if impossible assignment.
            
            for assmnt in self.list_form:
                current_index += 1 # Update the current index.
                count = 0 # Will store the lenght of the current assignment.
               
                for symbol_assmnt in assmnt.split('.'): # Iterate over the symbols of the assignment.  
                    if symbol_assmnt[0] == '#': # If a proper assignment, lenght of the assigned value.
                        
                        # The if statement below is important to deal with negative assigenments (i.e., of form #n*).
                        reference = int(symbol_assmnt[1:]) if symbol_assmnt[-1] != '*' else int(symbol_assmnt[1:-1])
                        
                        if reference > current_index - 1: # If a proper assignment points to a yet unassigned position, raises an error.
                            raise ValueError("Assigment in position " + str(current_index) + " makes reference to unassigned position!")
                        else:
                            count += past_indexes[reference] #Update count according to the values of proper asignments.
                    elif '' != symbol_assmnt:  # If not a proper assignement and it is a non-trivial simple assignement, the leght increases by 1.
                        count += 1 
                past_indexes.append(count)


            return past_indexes[-1]
    
    def complexity(self):
        '''
        Return the classical complexity of the SLP as the sum of lenghts of the RHS.
        
        Ex.: slp_complexity(['x','y','#0.#1']) = 4
        
        Returns
        -------
        complexity : int
        The complexity as the sum of lengths of RHSs of assignments.
        '''
        return sum([len(l.split('.')) for l in self.list_form])
    
    
    def inverse(self, inplace = False):
        '''
        Return an SLP for the inverse of the sequence presented by the SLP. Notice that it just adds a new assignment to the end of the SLP.
        
        inplace : bool
        If True, susbtitutes the initial SLP for its inverse.
        '''
        inverse_slp = copy.deepcopy(self.list_form)
        
        inverse_slp.append('#' + str(len(inverse_slp)-1) + '*')
            
        if inplace: # If inplace, update the SLP to its inevrse.
            self.list_form = inverse_slp
        return SLP(inverse_slp)
    
    
    '''
    Slightly more complicated operations
    '''
    
    def count(self, symbol):
        '''
        Count the number of absolute value occurences of a symbol in the SLP.
        
        Ex.: SLP(['x','x*','#0.#1']).get_count(x) = 2

        Parameters
        ----------
        symbol : str
        Symbol to be counted.
        
        Returns
        --------
        counts : int
        Number of occurences of a symbol (including its negative) in the SLP.
        
        The gernal case is implemented using dynamic programming (memorization), only faster than counting occurances of last sequence if SLP is compressed, otherwise count on the
        last assignment.  
        '''
        if not '#' in self.list_form[-1]: # If the SLP is not compressed.
            return self.list_form[-1].count(symbol)
        
        else:
            past_indexes = [] # List of the number of occurances of the symbol for each assignment, counting proper assignments.
            current_index = -1 # Keeps track of current index to call error, if impossible assignment.
            
            for assmnt in self.list_form:
                current_index += 1 # Update the current index.
                count = assmnt.count(symbol) # The number of occurences of the symbol in the current assignment.
                for symbol_assmnt in assmnt.split('.'): # Iterate over the symbols of the assignment. 
                    if symbol_assmnt[0] == '#': # If a proper assignment, get number of occurences in the assigned value.
                        
                        # The if statement below is important to deal with negative assigenments (i.e., of form #n*).
                        reference = int(symbol_assmnt[1:]) if symbol_assmnt[-1] != '*' else int(symbol_assmnt[1:-1])
                        
                        if reference > current_index - 1: # If a proper assignment points to a yet unassigned position, raises an error.
                            raise ValueError("Assigment in position " + str(current_index) + " makes reference to unassigned position!")
                        else:
                            count += past_indexes[reference] #Update count according to the values of proper asignments.
                past_indexes.append(count)


            return past_indexes[-1]
        
        
    def signed_count(self, symbol):
        '''
        Count the number of signed occurences of a symbol in the SLP.
        
        Ex.: SLP(['x','x*','#0.#1.x*']).get_signed_count('x') = 1, SLP(['x','x*','#0.#1.x*']).get_signed_count('x*') = 2
        
        Parameters
        ----------
        symbol : str
        Symbol to be counted.
        
        Returns
        --------
        counts : int
        Sign sentive number of occurences of the symbol in the SLP.
        
        The gernal case is implemented using dynamic programming (memorization), only faster than counting occurances of last sequence if SLP is compressed, otherwise count on the
        last assignment.   
        '''
        
        if not '#' in self.list_form[-1]: # If the SLP is not compressed.
            return self.list_form[-1].split('.').count(symbol) # Count exact occurences of the symbol in the assignment.
        
        else:
            inverse = symbol[:-1] if symbol[-1] == '*' else symbol + '*' # Defines the inverse of the symbol, that is 'x'-> 'x*' and 'x*'->'x'.
            
            past_indexes = [] # List of the number of occurances of the signed symbol for each assignment, counting proper assignments.
            past_indexes_inverses = [] # List of the number of occurances of the inverse of signed symbol for each assignment, counting proper assignments.
            current_index = -1 # Keeps track of current index to call error, if impossible assignment.
            
            for assmnt in self.list_form:
                current_index += 1 # Update the current index
                count = assmnt.split('.').count(symbol) # Count exact occurences of the symbol in the assignment.
                count_inverse = assmnt.split('.').count(inverse)
                
                for symbol_assmnt in assmnt.split('.'): # Iterate over the symbols of the assignment.    
                    if symbol_assmnt[0] == '#': # If a proper assignment, get number of occurences in the assigned value.
                        
                        # The if statement below is important to deal with negative assigenments (i.e., of form #n*).
                        reference = int(symbol_assmnt[1:]) if symbol_assmnt[-1] != '*' else int(symbol_assmnt[1:-1])
                        
                        if reference > current_index - 1: # If a proper assignment points to a yet unassigned position, raises an error.
                            raise ValueError("Assigment in position " + str(current_index) + " makes reference to unassigned position!")
                        else:
                            if symbol_assmnt[-1] != '*': # If the assignment is positive (i.e., not followed by a *), the occurences of symbol and inverse are 
                                                        # computed directly.
                                count += past_indexes[reference]
                                count_inverse += past_indexes_inverses[reference]
                            else: # If the assignement is negative (i.e., followed by a *), the occurences of symbol and its inverse exchange places.
                                count += past_indexes_inverses[reference]
                                count_inverse += past_indexes[reference]

                                
                past_indexes.append(count)
                past_indexes_inverses.append(count_inverse)
        
        return past_indexes[-1]
    
    
    def substitute(self, replaced, replacement, inplace = False):
        '''
        Substitute every occurence of a simple symbol by a sequence, which can be given as a SLP.
        
        Parameters
        ----------
        replaced : str
        Simple symbol to be replaced.
        replacement : str, SLP
        The replacement string, can be given as a SLP.
        inplace : bool, optional
        If True, updates the current SLP to be replaced.
         
        Returns
        -------
        slp : SLP
        SLP of the substitution.
        
        The gernal case is implemented using dynamic programming (memorization), only faster than counting occurances of last sequence if SLP is compressed, otherwise use string replace on the
        last assignment if replacement is a string.
        '''
        if (not '#' in self.list_form[-1]) and type(replacement) == str and (len(replacement.split('.')) == 1): # If the SLP is not compressed.
            new_slp = [assmnt for assmnt in self.list_form[:-1]]
            new_slp.append(self.list_form[-1].replace(replaced, replacement)) # Replace occurences of the symbol in the assignment.
        
        else:
            new_slp = [] # New SLP in list form
            
            # Deal with replacement being either string or SLP.
            replacement = [replacement] if type(replacement) == str else replacement.list_form
            
            replacement_size = len(replacement) # How many new assignments were added thanks to replacement.
            new_slp += replacement # Add replacement to the SLP.
            replacement_index = '#' + str(len(replacement) - 1) # The assignment position of the replacement sequence in the new SLP.

            
            for assmnt in self.list_form:
                new_assmnt = ''
                for symbol_assmnt in assmnt.split('.'):
                    if '#' in symbol_assmnt:  # If a proper asignment.    
                        # Add transformed proper assignment to SLP by padding by the size of the replacement to the assignment index. We do the if statemente to avoid problems with *.
                        new_assmnt += '#' + str(int(symbol_assmnt[1:]) + replacement_size) + '.' if symbol_assmnt[-1] != '*' else '#' + str(int(symbol_assmnt[1:-1]) + replacement_size) + '*.'
                    else: # If simple symbol, only append to new assignment
                        new_assmnt += symbol_assmnt + '.'
                    
                new_assmnt = new_assmnt.replace(replaced, replacement_index) # Replace the target symbol by its index reference
                new_slp.append(new_assmnt[:-1]) # Delete last '.' symbol.
                                
        if inplace: # If inplace == True, substitute the list form to uncompressed form.
            self.list_form = new_slp
        
        return SLP(new_slp)
    
    def get_power(self, power, inplace = False):
        '''
        If s is a sequence given by the SLP, find a SLP for s^power. The new SLP will have form 
        [s,x_1='x0.x0',x_2='x1.x1',...,x{lg(power)+1} = 'x{lg(power)}.x{lg(power)}','x0^b0.x1.^b1...x{lg(power)+1}^b{lg(power)+1}'] 
        where b0b1...b{lg(power)+1} is the binary representation of power.
        
        Parameters
        ----------
        power : int
        The power to be taken.
        inplace : bool, optional
        If True, updates the current SLP to its power.
         
        Returns
        -------
        slp : SLP
        SLP of the power.
        '''
        if not '#' in self.list_form[-1]: # If the SLP is not compressed.
            return SLP([((self.list_form[-1] +'.')*power)[:-1]]) # Count exact occurences of the symbol in the assignment.
        else:
            new_slp = copy.deepcopy(self.list_form) # Start constructing x0
            power_binary = bin(power)[2:] # Get the binary representation of the power.
            leading_digit = len(power_binary) # Length of the binary representation of the power, i.e., lg power + 1.

            # We will add to the SLP the following assigments, x0.x0, x1.x1, ..., x{leading_digit-1}.x{leading_digit-1}, where x0 is the SLP of replacement.
            # This variable power_bank saves, exactly, the indices of each xi, starting with x0 (i.e., the SLP of the replacement itself). We iterate to get the rest.
            x0 = '#' + str(len(new_slp) - 1)
            power_bank = [x0] 
            for _ in range(1, leading_digit):
                power_bank.append(x0 + '.' + x0) # Add to the SLP of the power the assignment x{i-1}.x{i-1} where i is the current iteration index.
                new_slp.append(x0 + '.' + x0) # Add to replacement the assignment x{i-1}.x{i-1}.
                x0 = '#' + str(len(new_slp) - 1) # Update the last entry of the power bank. 

            # Now add the assignement 'x0^b0.x1.^b1...x{lg(power)+1}^b{lg(power)+1}'.
            last_assignment_power = ''
            if power_binary[1:] != (len(power_binary)-1)*'0': # If power is a power of 2, we are done.
                for i,bi in enumerate(power_binary): # Iterate over the binary representation of power.
                    last_assignment_power += int(bi)*(power_bank[i] + '.')
                new_slp.append(last_assignment_power[:-1])

            if inplace:
                # If inplace == True, substitute SLP to its power.
                self.list_form = new_slp

            return SLP(new_slp)
    
    '''
    Changes of presentation
    '''    
    
    
    def get_uncompressed(self, inplace = False):
        '''
        Uncompress the SLP by substituting proper assignements for their values.
        
        Parameters
        ----------
        inplace : bool, optional
        If True, substitute the list form for its uncompressed version.
        
        Returns
        -------
        slp : SLP
        SLP for the input with no proper assignments.
        '''
        uncompressed_form = []
        
        for assmt in self.list_form:
            
            uncompressed = '' 
            for symbol_assmnt in assmt.split('.'):                
                # If assignments are valid, we iterate over the symbol to check if it is simple or an assignment. 
                    
                if symbol_assmnt[0] == '#': # If a proper assigment, substitute for the actual sequence value.
                    
                    # The if statement below is important to deal with negative assigenments (i.e., of form #n*).
                    reference = int(symbol_assmnt[1:]) if symbol_assmnt[-1] != '*' else int(symbol_assmnt[1:-1])
                    
                    if symbol_assmnt[-1] != '*': # If the proper assignment is positive, only append it to the sequence.
                        uncompressed += uncompressed_form[reference] + '.'
                    else:
                        # We append the inverse of each element of the assigned value, inverting the order of the sequence (shoes-socks theorem).
                        for symbol_uncompressed in uncompressed_form[reference].split('.')[::-1]:
                            # To avoid double negation (i.e., **), we do as a if else
                            uncompressed += symbol_uncompressed + '*.' if symbol_uncompressed[-1] != '*' else symbol_uncompressed[:-1] + '.'
                else: 
                    uncompressed += symbol_assmnt + '.'
            uncompressed = uncompressed[:-1] if uncompressed[-1] == '.' else uncompressed # Delete last occurence of a '.'.
            uncompressed_form.append(uncompressed)
        
        if inplace: # If inplace == True, substitute the list form to uncompressed form.
            self.list_form = uncompressed_form
        return SLP(uncompressed_form)
    
    def get_binary(self, inplace = False, dictionary = False):
        '''
        Transform a general SLP into binary (Chomsky normal form).
        
        Ex.: SLP(['x*','y','#0.#1.x']).get_binary() -> ['x*','y','#0.#1','x', '#2.#3']
        
        Parameters
        ----------      
        inplace : bool, optional
        If True, update self.list_form for the output.
        dictionary : bool, optional
        If True, returns the dictionary which maps every assignment and symbol of the input to the corresponding assignment of the output. Might be useful for debugging.
        
        Returns
        -------
        slp : SLP
        Binary SLP for the input.
        
        Implemented using dynamic programming (memorization).
        '''
        binary_list = []
        binary_dic = {}
        
        for k, assmt in enumerate(self.list_form):
            for i, symbol_assmnt in enumerate(assmt.split('.')): # Iterate over the symbols of each assignment to assign them, if necessary.
                
                j = 0 # What we are doing here is not the most pedagogical code, but it is the faster. The idea is that we will iterate over the symbols of the 
                # assignment and make them as new assignements if they are not yet in the assignment list. We will also make new assignments so that each proper
                # assignment has lenght 2. To make sure we iterate correctly, we use this variable j that tells us whether the last assignments added to the
                # assignment list were of lenght 2 (in which case, nothing to do) or if they were of lenght 1, in which case we modify the iteration to concatenate
                # with the len(binary_list)-j entry, instead of only len(binary_list).
                
                if not symbol_assmnt in binary_dic.keys(): # If symbol already in the dictionary keys, we only need to update the list of assignments.
                    j += 1 # Update j as we have added a new element to binary_list.
                    
                    if not '#' in symbol_assmnt:
                        binary_list.append(symbol_assmnt) # If a simple symbol, including negative, is part of an assignement, it is separated as a new assignment.
                        binary_dic[symbol_assmnt] = '#' + str(len(binary_list)-1) # Add to dictionary of binary list the new symbol.
                    
                    else: # If an assignment is proper and not yet in the dictionary, it means it is a negative of a previous proper assignment.
                        binary_list.append(binary_dic[symbol_assmnt[:-1]] + '*') # If it is a negative assignment, we simply .
                        binary_dic[symbol_assmnt] = '#' + str(len(binary_list)-1) 

                if i == 1:# In the first iteration, concatenate the first and second symbols.
                    binary_list.append(binary_dic[assmt.split('.')[0]] + '.' + binary_dic[symbol_assmnt])
                
                elif i > 1: # If assignement is of form 'x1.x2.x3.x4....' go concatenating with the assignment list ['x1.x2', '#0.x3', '#1.x4', ...].
                    binary_list.append('#' +  str(len(binary_list) -1 - j) + '.' + binary_dic[symbol_assmnt])
            
            binary_dic['#' + str(k)] = '#' + str(len(binary_list)-1) # Rewrite the current assignment of the original list as a binary assignment.
        
        if inplace: # If inplace == True, substitute the list form to binary form.
            self.list_form = binary_list
            
        
        if dictionary: # If dictionary returns binary_dic as well.
            return binary_list, binary_dic
        
        else:
            return SLP(binary_list)