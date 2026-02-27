import pytest
import pygame
from game.ball import Ball

def test_line_intersection_crossing():
    # Two lines crossing at (5, 5)
    line1_start = (0, 0)
    line1_end = (10, 10)
    line2_start = (0, 10)
    line2_end = (10, 0)

    intersection = Ball.line_intersection(line1_start, line1_end, line2_start, line2_end)

    assert intersection is not None
    assert intersection.x == pytest.approx(5)
    assert intersection.y == pytest.approx(5)

def test_line_intersection_parallel():
    # Two horizontal parallel lines
    line1_start = (0, 0)
    line1_end = (10, 0)
    line2_start = (0, 1)
    line2_end = (10, 1)

    intersection = Ball.line_intersection(line1_start, line1_end, line2_start, line2_end)

    assert intersection is None

def test_line_intersection_no_intersection_segments():
    # Lines would intersect at (5, 5) if infinite, but segment 1 stops at (4, 4)
    line1_start = (0, 0)
    line1_end = (4, 4)
    line2_start = (0, 10)
    line2_end = (10, 0)

    intersection = Ball.line_intersection(line1_start, line1_end, line2_start, line2_end)

    assert intersection is None

def test_line_intersection_endpoints():
    # Intersection at the endpoint of line 1 and start of line 2
    line1_start = (0, 0)
    line1_end = (5, 5)
    line2_start = (5, 5)
    line2_end = (10, 0)

    intersection = Ball.line_intersection(line1_start, line1_end, line2_start, line2_end)

    assert intersection is not None
    assert intersection.x == pytest.approx(5)
    assert intersection.y == pytest.approx(5)

def test_line_intersection_collinear():
    # Collinear lines (overlapping or not) result in denominator = 0 -> None
    line1_start = (0, 0)
    line1_end = (10, 10)
    line2_start = (5, 5)
    line2_end = (15, 15)

    intersection = Ball.line_intersection(line1_start, line1_end, line2_start, line2_end)

    assert intersection is None

def test_line_intersection_vertical_horizontal():
    # Vertical line and horizontal line crossing
    line1_start = (5, 0)
    line1_end = (5, 10)
    line2_start = (0, 5)
    line2_end = (10, 5)

    intersection = Ball.line_intersection(line1_start, line1_end, line2_start, line2_end)

    assert intersection is not None
    assert intersection.x == pytest.approx(5)
    assert intersection.y == pytest.approx(5)
