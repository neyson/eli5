# -*- coding: utf-8 -*-
from __future__ import print_function
import cgi
import os
import inspect
from pprint import pprint

from hypothesis.strategies import integers
from hypothesis.extra.numpy import arrays

from eli5.formatters import format_as_text, format_as_html


def rnd_len_arrays(dtype, min_len=0, max_len=3, elements=None):
    """ Generate numpy arrays of random length """
    lengths = integers(min_value=min_len, max_value=max_len)
    return lengths.flatmap(lambda n: arrays(dtype, n, elements=elements))


def format_as_all(res, clf):
    """ Format explanaton as text and html, print text explanation, and save html.
    """
    expl_text, expl_html = format_as_text(res), format_as_html(res)
    pprint(res)
    print(expl_text)
    _write_html(clf, expl_html, expl_text)
    return expl_text, expl_html


def strip_blanks(html):
    """ Remove whitespace and line breaks from html.
    """
    return html.replace(' ', '').replace('\n', '')


def _write_html(clf, html, text):
    """ Write to html file in .html directory. Filename is generated from calling
    function name and module, and clf class name.
    This is useful to check and debug format_as_html function.
    """
    caller = inspect.stack()[2]
    try:
        test_name, test_file = caller.function, caller.filename
    except AttributeError:
        test_name, test_file = caller[3], caller[1]
    test_file = os.path.basename(test_file).rsplit('.', 1)[0]
    filename = '{}_{}_{}.html'.format(
        test_file, test_name, clf.__class__.__name__)
    dirname = '.html'
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    path = os.path.join(dirname, filename)
    with open(path, 'wb') as f:
        f.write('Text:<pre>{text}</pre>End of text<hr/>\n{html}'
                .format(text=cgi.escape(text, quote=True), html=html)
                .encode('utf8'))
    print('html written to {}'.format(path))


def get_all_features(feature_weights):
    """ Collect a set of all features from feature weights.
    """
    features = set()
    for name, value in feature_weights:
        if isinstance(name, list):
            features.update(f['name'] for f in name)
        else:
            features.add(name)
    return features
