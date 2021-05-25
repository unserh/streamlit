# Copyright 2018-2021 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""text_area unit test."""

import re
from unittest.mock import patch

from tests import testutil
import streamlit as st


class TextAreaTest(testutil.DeltaGeneratorTestCase):
    """Test ability to marshall text_area protos."""

    def test_just_label(self):
        """Test that it can be called with no value."""
        st.text_area("the label")

        c = self.get_delta_from_queue().new_element.text_area
        self.assertEqual(c.label, "the label")
        self.assertEqual(c.default, "")

    def test_value_types(self):
        """Test that it supports different types of values."""
        arg_values = ["some str", 123, None, {}, SomeObj()]
        proto_values = ["some str", "123", "None", "{}", ".*SomeObj.*"]

        for arg_value, proto_value in zip(arg_values, proto_values):
            st.text_area("the label", arg_value)

            c = self.get_delta_from_queue().new_element.text_area
            self.assertEqual(c.label, "the label")
            self.assertTrue(re.match(proto_value, c.default))

    def test_height(self):
        """Test that it can be called with height"""
        st.text_area("the label", "", 300)

        c = self.get_delta_from_queue().new_element.text_area
        self.assertEqual(c.label, "the label")
        self.assertEqual(c.default, "")
        self.assertEqual(c.height, 300)

    def test_outside_form(self):
        """Test that form id is marshalled correctly outside of a form."""

        st.text_area("foo")

        proto = self.get_delta_from_queue().new_element.color_picker
        self.assertEqual(proto.form_id, "")

    @patch("streamlit._is_running_with_streamlit", new=True)
    def test_inside_form(self):
        """Test that form id is marshalled correctly inside of a form."""

        with st.form("form"):
            st.text_area("foo")

        # 2 elements will be created: form block, widget
        self.assertEqual(len(self.get_all_deltas_from_queue()), 2)

        form_proto = self.get_delta_from_queue(0).add_block
        text_area_proto = self.get_delta_from_queue(1).new_element.text_area
        self.assertEqual(text_area_proto.form_id, form_proto.form.form_id)


class SomeObj(object):
    pass
