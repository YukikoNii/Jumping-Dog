from .project import format_score, produce_positions, reset_height
import pygame


def test_format_score():
    assert format_score(1) == "Score: 1"
    assert format_score(10) == "Score: 10"
    assert format_score(100) == "Score: 100"


def test_produce_positions():
    assert produce_positions(12) == [0,30,60,90,120,150,180,210,240,270,300,330]
    assert produce_positions(5) == [0,82.5,165,247.5,330]


def test_reset_height():
    assert reset_height() == 1200
    assert reset_height(1) == 1700
    assert reset_height(4) == 950



