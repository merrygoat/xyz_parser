class XYZParser:
    """Parses XYZ files to make sure they are valid and determines the number of particles and frame offsets"""
    frame_offsets = []
    frame_particles = []
    num_frames = 0
    frame_buffer = []
    line_number = 0

    def __init__(self, filename):
        self.filename = filename
        self.check_file()

    def check_file(self):
        """Checks if file is a valid XYZ file, exits if not."""
        with open(self.filename, 'r') as xyz_file:
            line = xyz_file.readline()
            while line != "":
                self.check_particle_number(line)
                self.line_number += 1
                # Skip the comment line
                xyz_file.readline()
                self.line_number += 1
                # Store the file location of the start of the frame
                self.frame_offsets.append(xyz_file.tell())
                self.get_coordinates(xyz_file)
                ValueTests.check_coordinate_frame(self.frame_buffer)
                self.num_frames += 1
                line = xyz_file.readline()

    def check_particle_number(self, line):
        """Raises exception if particle number is wrong format"""
        self.frame_particles.append(ValueTests.check_int(line))

    def get_coordinates(self, xyz_file):
        """Returns True if num_particles lines can be read from the file."""
        self.frame_buffer = []
        for i in range(self.frame_particles[-1]):
            line = xyz_file.readline()
            if line == "":
                print("Unexpected file end. Expected particle coordinates.")
                raise EOFError
            else:
                self.frame_buffer.append(line)


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
        """Passes lines of coordinates to the check_coordinate_line method"""
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


class XYZReader:
    """Methods for reading data from files."""

    def __init__(self, input_xyz_file):
        self.xyz_file = input_xyz_file
        self.xyz_info = XYZParser(input_xyz_file)

    def get_num_frames(self):
        return self.xyz_info.num_frames

    def get_frame(self, frame_number):
        if frame_number > self.xyz_info.num_frames:
            print("Unable to get frame. Requested frame > total frames")
            return 1
        else:
            frame_data = XYZFrame()
            with open(self.xyz_file) as input_file:
                input_file.seek(self.xyz_info.frame_offsets[frame_number])
                frame_data.num_particles = self.xyz_info.frame_particles[frame_number]
                for particle in range(frame_data.num_particles):
                    frame_data.data.append(input_file.readline().split())
            return frame_data
