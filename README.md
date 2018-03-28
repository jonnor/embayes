
# embayes
Bayesian machine learning classifiers for embedded systems.
Train in Python, deploy on microcontroller.

Want decision trees instead? Go to [emtrees](https://github.com/jonnor/emtrees)

## Key features

Embedded-friendly Classifier

* Portable C99 code
* No stdlib required
* No dynamic allocations
* Integer/fixed-point math only
* Single header file include
* Fast, sub-millisecond classification

Convenient Training

* API-compatible with [scikit-learn](http://scikit-learn.org)
* Implemented in Python 3
* C classifier accessible in Python using pybind11

[MIT licensed](./LICENSE.md)

## Status
**Minimally useful**

* Gaussian Naive Bayes classifier implemented
* Tested running on ESP8266 and Linux.
* On ESP8266, 2 classes and 30 features classify in under 0.5ms.
Thanks mostly to a [Simplified probability calculation](./doc/Probability Density Function.ipynb).


## Installing

Install from PyPI

    pip install embayes --user

## Usage

See [examples/cancer.py](./examples/cancer.py) and [embayes.ino](./embayes.ino)

## TODO

0.2

* Make estimator a wrapper around `sklearn.naivebayes.GaussianNB`
* Make estimator work in sklearn pipeline
* Make `pdf` approximation configurable as parameter

1.0

* Support generating inline C code, not needing model coefficients in RAM
* Support de/serializing coefficients at runtime
* Support training on microcontroller
