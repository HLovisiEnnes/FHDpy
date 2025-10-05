# FHDpy: Python package for compressed data structures of Heegaard splittings (almost v 0.1)
This package was created to serve as a proof of concept in the [arXiv preprint](https://arxiv.org/abs/2507.11406), authored by Henrique Ennes and Clément Maria. The code, however, is the full responsibility of the first author, so you can only blame him for anything that does not work.

## Background
A Heegaard splitting is a representation of a closed 3-manifold by the gluing of two handlebodies of common surface $\Sigma_g$ through an element of its mapping class group, $\phi \in \text{Mod}(\Sigma_g)$. Equivalently, a Heegaard splitting can be described by two sets of $g$ disjoint curves, say $\alpha$ and $\beta$, with $\beta = \phi(\alpha)$, whose intersection pattern conveys much of the topology of the underlying 3-manifold. We algorithmically explore this notion in the preprint, where we propose a representation of Heegaard diagrams through straight-line programs (SLPs) of the intersection sequences of the $\beta$-curves and the edges of cellular complexes of a surface.

The SLP data structure allows one to encode some 3-manifolds with exponentially less space compared to the usual triangulation representation of 3-manifolds, while still being able to efficiently manipulate and investigate their topology. This package implements some of these manipulations, which are explained in greater detail in the mentioned preprint.

### Philosophy
Although there exist Python packages for constructing and manipulating SLPs (cf. ..., to name a few), we opted to implement an SLP module by hand. There are a few reasons behind this decision.

1. We wanted to stick to a particular syntax and notation, where we consider SLPs not in binary (Chomsky normal form), allow for mixed assignments, and enable better communication with `Twister` notation (which we use to generate splittings).
2. This is also a proof of concept: SLPs are fun and among the easiest data structures one could hope for, while still having compression power comparable to the binary representation of integers.

Moreover, although all of this code would be significantly faster if implemented in different languages (and, indeed, speed is an important aspect of our argument here), we opted to have everything in Python, in the name of accessibility (and the author's better acquaintance with the programming language).

Finally, the code is *extensively* commented, and some (but not all) programming choices were made for the sake of pedagogy and not efficiency.

### About this version
For someone who has read the original preprint, it will soon become clear that, although all experiments from Section 5 used solely this package, we deviate in two major aspects from the rest of the text:

1. we do not necessarily consider triangulations of surfaces, but rather more general cellular complexes;
2. we do not use normal coordinates as inputs.

These choices make sense in the experiments described here (i.e., when the inputs are words in the mapping class group represented by some generating set), but they make some of the algorithms described in Section 4 not readily useful. In due time, however, we plan to extend this code to include those cases, although we will likely not achieve the advertised running times for all cases.

In order of priority, we want to implement in the next versions:

1. Stefankovic's randomized normalization algorithm;
2. automatic construction of marked triangulations of closed surfaces of arbitrary genus;
3. the Erickson–Nayyeri algorithm for tracing street complexes (this one will probably take even longer).

Unfortunately, we are not able to give exact deadlines for these implementations, but the author would gladly accept suggestions for further improvements.

### External packages
Besides Python's native modules, this code imports:

1. `snappy`: version 3.2+ (only needed for FHD)
2. `numpy`: version 2.1.3+

It also assumes Python 3.10+.

## Tutorial
The package is divided into two (very short) modules, one for the SLP machinery (`TutorialSLP.ipynb`) and one for the Heegaard diagrams (`TutorialFHD.ipynb`). There are two tutorial notebooks for each of these modules. Although the FHD module uses SLP, the converse is not true, and many SLP-only functions are implemented. The images and experiments described in the preprint can be found in `ExperimentsWithFHD.ipynb`.
