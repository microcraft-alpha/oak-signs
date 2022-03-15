"""Unit tests for the interface class."""

import uuid

from oak_signs.api import fields


def test_interface_identifier():
    """Check the random interface identifier."""
    obj = fields.Interface()
    assert type(obj._id()) is uuid.UUID  # type: ignore
