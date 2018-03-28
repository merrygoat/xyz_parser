import xyz_parser

xyz_data = xyz_parser.XYZReader("test/good_configuration.xyz")
print(xyz_data.get_num_frames())
print(xyz_data.get_frame(1).data)