import Transformations as Tr
import IOperations as Io
from PathProvider import PathProvider

'''
Wrapper class.
Contains different generation elements.
'''
class ProcessService:

    def __init__(self, path_provider, file_names=()):
        self.path_provider = path_provider
        self.file_names = file_names

    """
    Copy and merge data.
    """
    def basicMerge(self, input_dir):
        Io.deleteDirectory(self.path_provider.output_data_path)
        Io.makeDirectories(self.path_provider.output_data_path)
        Io.copyFiles(src=input_dir, dest=self.path_provider.output_data_path,
                     file_names=self.file_names)

        print('Merging...')
        Io.deleteFile(self.path_provider.merged_file)
        Io.makeDirectories(self.path_provider.output_merged_path)
        Tr.gdalMerge(input_data=self.path_provider.output_data_path,
                     out_file=self.path_provider.merged_file, is_pct=True)

    """
    Copy and use profileToProfile.
    """
    def __profilePrep(self, input_dir):
        Io.deleteDirectory(self.path_provider.output_tmp_path)
        Io.makeDirectories(self.path_provider.output_tmp_path)
        Io.copyFiles(src=input_dir, dest=self.path_provider.output_tmp_path,
                     file_names=self.file_names, file_name_regex="*.tif")

        print('Profiling')
        Io.deleteDirectory(self.path_provider.output_data_path)
        Io.makeDirectories(self.path_provider.output_data_path)
        Tr.profileToProfile(input_data=self.path_provider.output_tmp_path,
                            out_path=self.path_provider.output_data_path)

        Io.copyFiles(src=input_dir, dest=self.path_provider.output_data_path,
                     file_names=self.file_names, file_name_regex="*.TFW")

        # print('Translating into one file...')
        # Io.makeDirectories(self.path_provider.output_data_path)
        # Tr.translateIntoOneFile(input_data=self.path_provider.output_tmp2_path,
        #                         out_path=self.path_provider.output_data_path)

        print('Cleaning temp dirs...')
        Io.deleteDirectory(self.path_provider.output_tmp_path)
        # Io.deleteDirectory(self.path_provider.output_tmp2_path)

    """
    Use profileToProfile and merge data.
    """
    def profileMerge(self, input_dir):
        self.__profilePrep(input_dir)

        print('Merging...')
        Io.deleteFile(self.path_provider.merged_file)
        Io.makeDirectories(self.path_provider.output_merged_path)
        Tr.gdalMerge(input_data=self.path_provider.output_data_path,
                     out_file=self.path_provider.merged_file)

    """
    Merge in 4 consecutive steps.
    """
    def profileMergeSingleRun(self, input_dir, use_profile, zoom):
        # self.__profilePrep(input_dir)

        Io.deleteDirectory(self.path_provider.output_tmp2_path + '0\\')
        Io.deleteDirectory(self.path_provider.output_tmp2_path + '1\\')
        Io.deleteDirectory(self.path_provider.output_tmp2_path + '2\\')
        Io.deleteDirectory(self.path_provider.output_tmp2_path + '3\\')
        Io.deleteDirectory(self.path_provider.output_tmp2_path + '4\\')

        Io.makeDirectories(self.path_provider.output_tmp2_path + '0\\')
        Io.makeDirectories(self.path_provider.output_tmp2_path + '1\\')
        Io.makeDirectories(self.path_provider.output_tmp2_path + '2\\')
        Io.makeDirectories(self.path_provider.output_tmp2_path + '3\\')
        Io.makeDirectories(self.path_provider.output_tmp2_path + '4\\')

        # Io.deleteFile(self.path_provider.merged_file)
        # Io.makeDirectories(self.path_provider.output_merged_path)

        # Io.deleteFile(self.path_provider.output_merged_path + 'merged1.tif')
        # Io.deleteFile(self.path_provider.output_merged_path + 'merged2.tif')
        # Io.deleteFile(self.path_provider.output_merged_path + 'merged3.tif')
        # Io.deleteFile(self.path_provider.output_merged_path + 'merged4.tif')

        # print('Merge 1')
        # Tr.gdalMerge(input_data=self.path_provider.output_data_path + '1\\',
        #              out_file=self.path_provider.output_merged_path + 'merged1.tif')
        # print('Merge 2')
        # Tr.gdalMerge(input_data=self.path_provider.output_data_path + '2\\',
        #              out_file=self.path_provider.output_merged_path + 'merged2.tif')
        # print('Merge 3')
        # Tr.gdalMerge(input_data=self.path_provider.output_data_path + '3\\',
        #              out_file=self.path_provider.output_merged_path + 'merged3.tif')
        # print('Merge 4')
        # Tr.gdalMerge(input_data=self.path_provider.output_data_path + '4\\',
        #              out_file=self.path_provider.output_merged_path + 'merged4.tif')
        # print('Merge all')
        # Tr.gdalMerge(input_data=self.path_provider.output_merged_path,
        #              out_file=self.path_provider.merged_file)

        Io.copyFiles(input_dir, self.path_provider.output_tmp2_path + '0\\')
        reg = ('HP', 'HT', 'HU', 'HW', 'HX', 'HY', 'HZ', 'NA', 'NB', 'NC', 'ND',
               'NF', 'NG', 'NH', 'NJ', 'NK', 'NL', 'NM', 'NN', 'NO')
        Io.moveFiles(self.path_provider.output_tmp2_path + '0\\',
                     self.path_provider.output_tmp2_path + '1\\', regex=reg)
        reg = ('NR', 'NS', 'NT', 'NU', 'NW', 'NX', 'NY', 'NZ', 'OV', 'SC', 'SD', 'SE', 'TA')
        Io.moveFiles(self.path_provider.output_tmp2_path + '0\\',
                     self.path_provider.output_tmp2_path + '2\\', regex=reg)
        reg = ('SH', 'SJ', 'SK', 'TF', 'TG', 'SM', 'SN', 'SO', 'SP', 'TL', 'TM')
        Io.moveFiles(self.path_provider.output_tmp2_path + '0\\',
                     self.path_provider.output_tmp2_path + '3\\', regex=reg)
        reg = ('SR', 'SS', 'ST', 'SU', 'TQ', 'TR', 'SV', 'SW', 'SX', 'SY', 'SZ', 'TV')
        Io.moveFiles(self.path_provider.output_tmp2_path + '0\\',
                     self.path_provider.output_tmp2_path + '4\\', regex=reg)
        Io.deleteDirectory(self.path_provider.output_tmp2_path + '0\\')

        path_provider = PathProvider("1\\")
        ps = ProcessService(path_provider)
        ps.profileMerge(self.path_provider.output_tmp2_path + '1\\')
        ps.basicTile(not use_profile, zoom)
        Io.deleteDirectory(self.path_provider.output_tmp2_path + '1\\')

        path_provider = PathProvider("2\\")
        ps = ProcessService(path_provider)
        ps.profileMerge(self.path_provider.output_tmp2_path + '2\\')
        ps.basicTile(not use_profile, zoom)
        Io.deleteDirectory(self.path_provider.output_tmp2_path + '2\\')

        path_provider = PathProvider("3\\")
        ps = ProcessService(path_provider)
        ps.profileMerge(self.path_provider.output_tmp2_path + '3\\')
        ps.basicTile(not use_profile, zoom)
        Io.deleteDirectory(self.path_provider.output_tmp2_path + '3\\')

        path_provider = PathProvider("4\\")
        ps = ProcessService(path_provider)
        ps.profileMerge(self.path_provider.output_tmp2_path + '4\\')
        ps.basicTile(not use_profile, zoom)
        Io.deleteDirectory(self.path_provider.output_tmp2_path + '4\\')

    """
    Translate, warp and generate tiles.
    """
    def basicTile(self, is_pct, zoom):
        print('Translating')
        Io.deleteFile(self.path_provider.translated_file)
        Tr.gdalTranslate(input_file=self.path_provider.merged_file,
                         out_file=self.path_provider.translated_file,
                         is_pct=is_pct)

        print('Warping')
        Io.deleteFile(self.path_provider.warped_file)
        Tr.gdalWarp(in_file=self.path_provider.translated_file,
                    out_file=self.path_provider.warped_file)

        print('Tiling')
        Io.deleteDirectory(self.path_provider.output_tiles_path)
        Io.makeDirectories(self.path_provider.output_tiles_path)
        Tr.gdal2Tiles(in_file=self.path_provider.warped_file,
                      out_dir=self.path_provider.output_tiles_path,
                      zoom=zoom)
