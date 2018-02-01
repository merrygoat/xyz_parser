from os.path import getsize


class XYZParser:
    """Parses XYZ files to make sure they are valid and determines the number of particles and frame offsets"""
    frame_offsets = []
    frame_particles = []
    num_frames = 0
    frame_buffer = []
    line_number = 0

    def __init__(self, filename):
        self.filename = filename
        self.parse_file()

    def parse_file(self):
        """Parses an XYZ file, determining the number of frames and number of particles in each frame."""
        with open(self.filename, 'r') as xyz_file:
            line = "Temp"
            while line != "":
                self.frame_particles.append(self.check_particle_number(xyz_file.readline()))
                self.line_number += 1
                # Skip the comment line
                xyz_file.readline()
                self.line_number += 1
                # Store the file location of the start of the frame
                self.frame_offsets.append(xyz_file.tell())
                self.get_coordinates(xyz_file)
                self.num_frames += 1

    def check_particle_number(self, line):
        """Raises exception if particle number is wrong format"""
        self.frame_particles.append(ValueTests.check_int(line))

    def get_coordinates(self, xyz_file):
        """Returns True if num_particles lines can be read from the file."""
        for line_number in range(self.frame_particles[-1]):
            line = xyz_file.readline()
            if line == "":
                print("Unexpected file end. Expected particle coordinates.")
                raise EOFError
            else:
                new_frame = ValueTests.check_coordinate_frame(self.frame_buffer)
        return new_frame


class ValueTests:
    @staticmethod
    def check_int(input_string):
        try:
            return int(input_string)
        except ValueError:
            print("Check int failed.")
            raise ValueError

    @staticmethod
    def check_float(input_string):
        try:
            return float(input_string)
        except ValueError:
            print("Check float failed.")
            raise ValueError

    @staticmethod
    def check_coordinate_line(line):
        """Returns a line of an XYZ file if it is in the right format, else returns an exception"""
        split_line = line.split()
        if len(split_line) != 4:
            print("Too many or too few particles found.")
            raise ValueError
        return [split_line[0],
                ValueTests.check_float(split_line[1]),
                ValueTests.check_float(split_line[2]),
                ValueTests.check_float(split_line[3])]

    @staticmethod
    def check_coordinate_frame(frame_buffer):
        """Adds an XYZ frame to an XYZFrame object line by line"""
        new_frame = XYZFrame
        for line in frame_buffer:
            new_frame.data.append(ValueTests.check_coordinate_line(line))
            new_frame.num_particles += 1
        return new_frame


class XYZFrame:
    """A structure to store the data for a single XYZ frame"""
    data = []
    num_particles = 0

    def __init__(self):
        pass
