import Transformations as Tr
import IOperations as Io


class ProcessService:

    def __init__(self, path_provider, file_names=()):
        self.path_provider = path_provider
        self.file_names = file_names
        self.warp_in_file = path_provider.merged_file

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

        print('Translating...')
        Io.deleteFile(self.path_provider.translated_file)
        Tr.gdalTranslate(input_file=self.path_provider.merged_file,
                         out_file=self.path_provider.translated_file)

        self.warp_in_file = self.path_provider.translated_file

    def __profilePrep(self, input_dir):
        Io.deleteDirectory(self.path_provider.output_tmp_path)
        Io.makeDirectories(self.path_provider.output_tmp_path)
        Io.copyFiles(src=input_dir, dest=self.path_provider.output_tmp_path,
                     file_names=self.file_names, file_name_regex="*.tif")

        print('Profiling')
        Io.deleteDirectory(self.path_provider.output_tmp2_path)
        Io.makeDirectories(self.path_provider.output_tmp2_path)
        Tr.profileToProfile(input_data=self.path_provider.output_tmp_path,
                            out_path=self.path_provider.output_tmp2_path)

        Io.copyFiles(src=input_dir, dest=self.path_provider.output_tmp2_path,
                     file_names=self.file_names, file_name_regex="*.TFW")

        print('Translating into one file...')
        Io.makeDirectories(self.path_provider.output_data_path)
        Tr.translateIntoOneFile(input_data=self.path_provider.output_tmp2_path,
                                out_path=self.path_provider.output_data_path)

        print('Cleaning temp dirs...')
        Io.deleteDirectory(self.path_provider.output_tmp_path)
        Io.deleteDirectory(self.path_provider.output_tmp2_path)

    def profileMerge(self, input_dir):
        self.__profilePrep(input_dir)

        print('Merging...')
        Io.deleteFile(self.path_provider.merged_file)
        Io.makeDirectories(self.path_provider.output_merged_path)
        Tr.gdalMerge(input_data=self.path_provider.output_data_path,
                     out_file=self.path_provider.merged_file)

        self.warp_in_file = self.path_provider.merged_file

    def profileMergeSingleRun(self, input_dir):
        self.__profilePrep(input_dir)

        Io.deleteDirectory(self.path_provider.output_data_path + '1\\')
        Io.deleteDirectory(self.path_provider.output_data_path + '2\\')
        Io.deleteDirectory(self.path_provider.output_data_path + '3\\')
        Io.deleteDirectory(self.path_provider.output_data_path + '4\\')

        Io.makeDirectories(self.path_provider.output_data_path + '1\\')
        Io.makeDirectories(self.path_provider.output_data_path + '2\\')
        Io.makeDirectories(self.path_provider.output_data_path + '3\\')
        Io.makeDirectories(self.path_provider.output_data_path + '4\\')

        reg = ('HP', 'HT', 'HU', 'HW', 'HX', 'HY', 'HZ', 'NA', 'NB', 'NC', 'ND',
               'NF', 'NG', 'NH', 'NJ', 'NK', 'NL', 'NM', 'NN', 'NO')
        Io.moveFiles(self.path_provider.output_data_path,
                     self.path_provider.output_data_path + '1\\', regex=reg)
        reg = ('NR', 'NS', 'NT', 'NU', 'NW', 'NX', 'NY', 'NZ', 'OV', 'SC', 'SD', 'SE', 'TA')
        Io.moveFiles(self.path_provider.output_data_path,
                     self.path_provider.output_data_path + '2\\', regex=reg)
        reg = ('SH', 'SJ', 'SK', 'TF', 'TG', 'SM', 'SN', 'SO', 'SP', 'TL', 'TM')
        Io.moveFiles(self.path_provider.output_data_path,
                     self.path_provider.output_data_path + '3\\', regex=reg)
        reg = ('SR', 'SS', 'ST', 'SU', 'TQ', 'TR', 'SV', 'SW', 'SX', 'SY', 'SZ', 'TV')
        Io.moveFiles(self.path_provider.output_data_path,
                     self.path_provider.output_data_path + '4\\', regex=reg)

        print('Merge 1')
        Tr.gdalMerge(input_data=self.path_provider.output_data_path + '1\\',
                     out_file=self.path_provider.output_merged_path + 'merged1.tif')
        print('Merge 2')
        Tr.gdalMerge(input_data=self.path_provider.output_data_path + '2\\',
                     out_file=self.path_provider.output_merged_path + 'merged2.tif')
        print('Merge 3')
        Tr.gdalMerge(input_data=self.path_provider.output_data_path + '3\\',
                     out_file=self.path_provider.output_merged_path + 'merged3.tif')
        print('Merge 4')
        Tr.gdalMerge(input_data=self.path_provider.output_data_path + '4\\',
                     out_file=self.path_provider.output_merged_path + 'merged4.tif')
        print('Merge all')
        Tr.gdalMerge(input_data=self.path_provider.output_merged_path,
                     out_file=self.path_provider.merged_file)

        self.warp_in_file = self.path_provider.merged_file

    def basicTile(self, zoom):
        print('Warping')
        Io.deleteFile(self.path_provider.warped_file)
        Tr.gdalWarp(in_file=self.warp_in_file, out_file=self.path_provider.warped_file)

        print('Tiling')
        Io.deleteDirectory(self.path_provider.output_tiles_path)
        Io.makeDirectories(self.path_provider.output_tiles_path)
        Tr.gdal2Tiles(in_file=self.path_provider.warped_file,
                      out_dir=self.path_provider.output_tiles_path,
                      zoom=zoom)
