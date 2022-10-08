---
author: Shailesh Kumar
title: CR-Sparse v0.3.2
date: 2022-10-08
tags:
    - CR-Sparse
    - Python
    - JAX
category: Libraries
---

This release has been a month in the making.
The official release notes are
[here](https://github.com/carnotresearch/cr-sparse/releases/tag/v0.3.2).

A [Thinking in JAX](https://cr-sparse.readthedocs.io/en/latest/tutorials/jax.html) tutorial has been introduced in this release
for newbies to get a better hang of JAX based numerical
computing.

The main sparse recovery algorithm introduced in this
release is SPGL1 (Spectral Projected Gradient L1).
Testing the algorithm under different conditions
was an interesting experience. It finally gave
me a strong motivation to port Sparco problems
into CR-Sparse. Sparco is a large collection
of sparse recovery test problems written in MATLAB.
I had earlier avoided porting Sparco as I couldn't
understand its design clearly. But with an year
of linear operators based development behind me,
I guess, I was ready to port Sparco into CR-Sparse.

Introducing each test problem helped
me clarify different aspects
of the design of SPGL1 algorithm.
Several of these test problems require
some of the standard signals developed
by Donoho et al. for Wavelab. I included
them in `cr.nimble.dsp` module.
See the docs [here](https://cr-nimble.readthedocs.io/en/latest/source/dsp.html#synthetic-signals).
These synthetic test signals include:
heavi_sine, bumps, blocks, etc..
I tested these test problems with SPGL1
as well as some greedy algorithms like
Subspace Pursuit (SP) and Compressive Sampling
Matching Pursuit (CoSaMP).
Ended up fixing some bugs related to handling
of complex vectors in SP and CoSaMP as well.
[Test Problems Documentation](https://cr-sparse.readthedocs.io/en/latest/source/problems.html).


The `heavi-sine:fourier:heavi-side` problem
consists of a real signal modeled using
a Fourier-HeaviSide dictionary.
[Demo](https://cr-sparse.readthedocs.io/en/latest/gallery/0001.html).
Naturally, the
representation is a complex vector. Thus,
SPGL1 has to support handling of complex
representations with real signals.

`blocks:haar` is a test problem with real
signal modeled in an orthonormal basis.
[Demo](https://cr-sparse.readthedocs.io/en/latest/gallery/0002.html).
It is interesting to note that SP converges in a single iteration,
CoSaMP takes two iterations,
while SPGL1 takes 9 iterations to converge.


`complex:sinusoid-spikes:dirac-fourier`
is a complex signal containing a mixture of sinusoids
and spikes with real valued representation in
a Dirac Fourier dictionary.
[Demo](https://cr-sparse.readthedocs.io/en/latest/gallery/0004.html).
SP and CoSaMP converge very fast.
SPGL1 takes a while but converges correctly.

`signed-spikes:dirac:gaussian` is a relatively easy
problem in which sparse signed spikes are sampled
using a Gaussian sensing matrix.
[Demo](https://cr-sparse.readthedocs.io/en/latest/gallery/0007.html).
A correctly implemented sparse recovery algorithm should
handle this problem very easily.

`gaussian-spikes:dirac:gaussian` consists of
Gaussian measurements on Gaussian spikes
with identity basis.

The most exciting and challenging problem so far was
the source separation problem.
[Demo](https://cr-sparse.readthedocs.io/en/latest/gallery/0401.html).
In this example we consider the problem of separating two sources which have been mixed together. One is the sound of a guitar, and another is the sound of piano.
There were some interesting challenges in solving this problem.

* The sparsifying basis required an overlapped Windowed DCT operator.
  I implemented `cr.sparse.lop.windowed_op` to wrap any operator
  into an overlapped windowed operator.
* The data consists of audio from two sources. So it has to be
  represented as m x 2 matrix (one column for each source).
  This is a departure from the
  normal case of data (representation, signal, measurements)
  being vectors.
* The mixing matrix operates on each row of data. When the mixing
  matrix is implemented as a compressive sensing operator, it
  has to process input data on axis=1 (row by row).
* SPGL1 has to allow for both signal and represented be expressed
  in the form of arrays (2d array in this case). Thus any 
  inner product, norm computation should keep it in mind.

After handling these peculiarities, I was able to successfully
conduct the source separation using SPGL1.


This release also includes a revamp of Matching Pursuit (MP)
implementation. I had tried writing MP early in the beginning
of CR-Sparse. However my knowledge of JAX was quite rusty then.
Now that I have better understanding of JAX, I could rewrite
MP properly this time.

I have been trying to implement different algorithms discussed
in Michael Elad's book "Sparse and Redundant Representations".
Generation of Grassmannian frames from a starting random dictionary
is now supported.
[Demo](https://cr-sparse.readthedocs.io/en/latest/gallery/grass.html).
Another algorithm I implemented based on the book was
FOcal Underdetermined System Solver (FOCUSS).
[Demo](https://cr-sparse.readthedocs.io/en/latest/gallery/0300_cvx/focuss_1.html).


