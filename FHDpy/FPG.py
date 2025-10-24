from __future__ import annotations  # For dosctrings.



class FinitePresentation:
    '''
    Defines a finite presentation of a group, given by generators g_1,...,g_m
        and relators r_1,...,r_n. 
    Both generators and relators are assumed to be lists of strings, where
        the relators are given using FHDpy.SLP uncompressed notation
        (i.e., multiplication is denoted by `.` and inversion by `*`).
    Relators are supposed to represent the relations r_i = e, where e is the
        group's identity.

    Arguments:
        generators (list[str]): The group presentation generators.
        reltors (list[str]): The group presentation relators, assumed given
            using FHDpy.SLP uncompressed notation (i.e., multiplication is 
            denoted by `.` and inversion by `*`)

    '''
    def __init__(
            self, 
            generators_explicit : list[str], 
            relators_explicit : list[str]
            ) -> None:

        self.generators, self.relators = self.get_tietze_word(generators_explicit, relators_explicit)
        self.generators_explicit, self.relators_explicit = self.get_explicit()
        self.defficiency = len(self.relators) - self.generators 
        

        return None
    
    def get_tietze_word(
            self, 
            generators_explicit : list[str] | None = None, 
            relators_explicit: list[str] | None = None
            ) -> tuple[int, list[list[int]]]:
        '''
        Transform an explict presentation into Tietze numerical word presentation.
        Starts counting at 1.

        Arguments:
            generators_explicit(list[str] | None): List of generators given in string format. If None, 
                uses self.generators_explicit. Defaults to None.
            relators_explicit(list[str] | None): List of relators given in string format, where
                the relators are given using FHDpy.SLP uncompressed notation
                (i.e., multiplication is denoted by `.` and inversion by `*`).
                If None, uses self.relators_explicit. Defaults to None.
        Returns:
            int: Number of generators.
            list[list[int]]: List of relators in Tietze numerical form.
        
        Example:
            >>> get_tietze_word(['a','b','c'],['a*.b', 'c.c', 'b.a*.b*'])
            (3, [[-1, 2], [3, 3], [2, -1, -2]])

        '''
        # In case of no inputs, get the class' explicit.
        if generators_explicit == None:
            generators_explicit = self.generators_explicit
        if relators_explicit == None:
            relators_explicit = self.relators_explicit

        number_generators = len(generators_explicit)
        # This dictionary is a hash between the explicit string representation
        # of generators and the implicit Tietze word integer representation.
        # We do i + 1 because we want to start counting from 1, as the sign
        # will be important.
        tietze_hash = {gen: i + 1 for i,gen in enumerate(generators_explicit)}
        
        # Now we go substituting each generator in the relators for its integer 
        # representation.
        relators_list = []
        for rel in relators_explicit:
            rel_list = []
            
            for assmnt in rel.split('.'):
                sign = 1
                # If a negative assignment.
                if assmnt[-1] == '*':
                    sign = -1
                    # For the hash function, the negative power is not given.
                    assmnt = assmnt[:-1]
                rel_list.append(sign*tietze_hash[assmnt])
            
            relators_list.append(rel_list)
        return (number_generators, relators_list)
    
    def get_explicit(self) -> tuple[list[str], list[str]]:
        '''
        Gets an explicit representation of the group's presentations.

        Returns:
            list[str]: The explicit generators; they will all have form xi.
            list[str]: The explicit relators.
        '''
        geneators = ['x' + str(i) for i in range(self.generators)]
        relators = []
        for rel in self.relators:
            # Although this is a list, we call it string because we will use
            # a `join` at the end of the iteration.
            rel_str = ['x' + str(abs(i) - 1) + '*' if i < 0
                       else 'x' + str(i - 1)
                       for i in rel]
            relators.append('.'.join(rel_str))
        return geneators, relators
    
    def __str__(self):
        '''
        Print generators and relators explicitly.
        '''
        print_gen = 'Generators:\n' + ', '.join(self.generators_explicit)
        print_rel = '\n\nRelators:\n' + ', '.join(self.relators_explicit)
        return print_gen + print_rel