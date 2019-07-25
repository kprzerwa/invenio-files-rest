# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test serializer."""

from __future__ import absolute_import, print_function

from collections import namedtuple

from marshmallow import fields

from invenio_files_rest.serializer import BaseSchema, dump_wrapper, \
    json_serializer, serializer_mapping


def test_serialize_pretty(app):
    """Test pretty JSON."""
    class TestSchema(BaseSchema):
        title = fields.Str(attribute='title')

    data = {'title': 'test'}
    context = {'bucket': '11111111-1111-1111-1111-111111111111',
               'class': 'TestSchema', 'many': False}

    serializer_mapping['TestSchema'] = TestSchema

    # TODO This test should be checked if it shouldn't have
    #  BaseSchema instead of Schema
    with app.test_request_context():
        assert json_serializer(data=data, context=context).data == \
            b'{"title":"test"}'

    with app.test_request_context('/?prettyprint=1'):
        assert json_serializer(data=data, context=context).data == \
            b'{\n  "title": "test"\n}'


def test_marshmallow_compatibility():
    """Test wrapper class for marshmallow schema compatibility."""
    dict_result = {'test': 1}
    list_result = [{'test': 1}, {'test': 2}]
    old_marshal = namedtuple('MarshalResult', ['data', 'errors'])
    tuple_result = old_marshal({'test': 1}, [{'field': 5}])

    wrapped = dump_wrapper(dict_result)

    assert wrapped == dict_result
    assert wrapped.data == dict_result

    wrapped = dump_wrapper(list_result)
    assert wrapped == list_result
    assert wrapped.data == list_result

    wrapped = dump_wrapper(tuple_result)
    assert wrapped == tuple_result
    assert isinstance(wrapped, tuple)
    assert tuple_result.data == dict_result
