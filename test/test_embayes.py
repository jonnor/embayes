
import subprocess
import os
import os.path

import sklearn
import numpy
from sklearn import datasets
from sklearn import model_selection
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.utils.estimator_checks import check_estimator 

import embayes
import pytest

def build_classifier(estimator, name='test_bayes', temp_dir='tmp/', func=None):
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    tree_name = name
    if func is None:
      func = 'embayes_predict(&{}_model, values, length)'.format(tree_name)
    def_file = os.path.join(temp_dir, name+'.def.h')
    code_file = os.path.join(temp_dir, name+'.c')
    bin_path = os.path.join(temp_dir, name)

    # Trivial program that reads values on stdin, and returns classifications on stdout
    code = """
    #include "embayes_test.h"
    #include "{def_file}"

    static void classify(const val_t *values, int length, int row) {{
        const int32_t class = {func};
        printf("%d,%d\\n", row, class);
    }}
    int main() {{
        embayes_test_read_csv(stdin, classify);
    }}
    """.format(**locals())

    with open(def_file, 'w') as f:
        f.write(estimator.output_c(tree_name))

    with open(code_file, 'w') as f:
        f.write(code)

    args = [ 'cc', '-std=c99', code_file, '-o', bin_path, '-I./test', '-I.' ]
    subprocess.check_call(args)

    return bin_path

def run_classifier(bin_path, data):
    lines = []
    for row in data:
        lines.append(",".join(str(v) for v in row))
    stdin = '\n'.join(lines)

    args = [ bin_path ]
    out = subprocess.check_output(args, input=stdin, encoding='utf8', universal_newlines=True)

    classes = []
    for line in out.split('\n'):
        if line:
            row,class_ = line.split(',')
            class_ = int(class_)
            classes.append(class_)

    assert len(classes) == len(data)

    return classes

@pytest.mark.skip('Not fully compatible yet')
def test_sklearn_api_naivegaussian():
   check_estimator(embayes.NaiveGaussian)


def test_basic_binary_classification():
    dataset = datasets.load_breast_cancer()
    X, Y = dataset.data, dataset.target
    estimator = embayes.NaiveGaussian()
    scores = model_selection.cross_val_score(estimator, X, Y, scoring='accuracy')

    assert numpy.mean(scores) > 0.9, scores

def test_binary_classification_compiled():

    dataset = datasets.load_breast_cancer()
    X, Y = dataset.data, dataset.target
    scaler = preprocessing.StandardScaler()
    X = scaler.fit_transform(X)
    estimator = embayes.NaiveGaussian()
    estimator.fit(X, Y)

    p = build_classifier(estimator)
    predicted = run_classifier(p, X)
    accuracy = metrics.accuracy_score(Y, predicted)

    assert accuracy > 0.9 # testing on training data


