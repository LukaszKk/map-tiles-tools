import os


class PathProvider:

    env_path = 'C:\\Users\\obliczenia\\anaconda3\\envs\\geo2\\'

    src_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = src_dir + '\\..\\logs\\'
    input_path = src_dir + '\\..\\input\\'
    output_path = src_dir + '\\..\\output\\'
    scripts_path = env_path + 'Scripts\\'

    input_data_path = input_path + 'data\\'

    input_50k = input_data_path + '50k\\'
    input_50k_incomplete = input_data_path + '50kIncomplete\\'
    input_50kTmp = input_data_path + '50kTmp\\'
    input_250k = input_data_path + '250k\\'

    input_icc = input_path + 'OS_Map_uncoated_FOGRA29_GCR_bas.icc'
    output_icc = input_path + 'sRGB_v4_ICC_preference.icc'

    group1_csv = input_data_path + "group1.csv"
    group2_csv = input_data_path + "group2.csv"
    group3_csv = input_data_path + "group3.csv"

    def __init__(self, output_path_suffix):
        self.output_path = self.output_path + output_path_suffix
        self.log_dir = self.log_dir + output_path_suffix

        self.output_data_path = self.output_path + 'data\\'
        self.output_tmp_path = self.output_path + 'tmp\\'
        self.output_tmp2_path = self.output_path + 'tmp2\\'
        self.output_tiles_path = self.output_path + 'tiles\\'

        self.output_merged_path = self.output_path + 'merged\\'
        self.merged_file = self.output_merged_path + 'merged.tif'
        self.warped_file = self.output_merged_path + 'warped.tif'
        self.translated_file = self.output_merged_path + 'translated.tif'
