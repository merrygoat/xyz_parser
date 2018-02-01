import xyz_parser as xyz
import pytest


class TestValueTests:
    @staticmethod
    def test_check_int():
        assert xyz.ValueTests.check_int("250") == 250
        assert xyz.ValueTests.check_int("250\t\t") == 250
        with pytest.raises(ValueError):
            xyz.ValueTests.check_int("A\t4.56\t4.32\t4.5\n")
            xyz.ValueTests.check_int("5.67")

    @staticmethod
    def test_check_float():
        assert xyz.ValueTests.check_float("250") == 250.0
        assert xyz.ValueTests.check_float("250\t\t") == 250.0
        assert xyz.ValueTests.check_float("5.67") == 5.67
        with pytest.raises(ValueError):
            xyz.ValueTests.check_float("A\t4.56\t4.32\t4.5\n")

    @staticmethod
    def test_check_coordinate_line():
        assert xyz.ValueTests.check_coordinate_line("A\t4.56\t4.32\t4.5\n") == ["A", 4.56, 4.32, 4.5]
        assert xyz.ValueTests.check_coordinate_line("A 4.56 4.32 4.5 ") == ["A", 4.56, 4.32, 4.5]
        assert xyz.ValueTests.check_coordinate_line("1 4.56 4.32 4.5 ") == ["1", 4.56, 4.32, 4.5]
        with pytest.raises(ValueError):
            xyz.ValueTests.check_coordinate_line("A 4.56 4.32 4.5 4")
            xyz.ValueTests.check_coordinate_line("A 4.B3 4.32 4.5")
            xyz.ValueTests.check_coordinate_line("A 4.03 4.5")

    @staticmethod
    def test_check_coordinate_frame():
        test_frame = xyz.ValueTests.check_coordinate_frame(
            ["A\t5.67\t5.32\t-2.43\n",
             "A\t5.67\t5.32\t-2.43\n"])
        assert test_frame.num_particles == 2
        assert test_frame.data[1][3] == -2.43
