import os


class PathProvider:

    env_path = 'D:\\Software\\anaconda3\\envs\\geo2\\'

    src_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = src_dir + '\\..\\logs\\'
    input_path = src_dir + '\\..\\input\\'
    output_path = src_dir + '\\..\\output\\'
    scripts_path = env_path + 'Scripts\\'

    input_data_path = input_path + 'data\\'
    output_data_path = output_path + 'data\\'
    output_tmp_path = output_path + 'tmp\\'
    output_tmp2_path = output_path + 'tmp2\\'
    output_tiles_path = output_path + 'tiles\\'

    input_50k = input_data_path + '50k\\'
    input_50k_incomplete = input_data_path + '50kIncomplete\\'
    input_50kTmp = input_data_path + '50kTmp\\'
    input_250k = input_data_path + '250k\\'

    input_icc = input_path + 'OS_Map_uncoated_FOGRA29_GCR_bas.icc'
    output_icc = input_path + 'sRGB_v4_ICC_preference.icc'

    output_merged_path = output_path + 'merged\\'
    merged_file = output_merged_path + 'merged.tif'
    warped_file = output_merged_path + 'warped.tif'
    translated_file = output_merged_path + 'translated.tif'
