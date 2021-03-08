import shutil
import os


def main():
    input_dir = "..\\..\\logs\\"
    output_dir = "..\\..\\logs\\output\\"

    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir)

    separator = "|"
    start_line = 6
    line_break = 4

    for (dir_path, dir_names, filenames) in os.walk(input_dir):
        file_counter = 1

        for file in filenames:
            with open(input_dir + file, "r") as reader:
                output_file_name = file[0:file.index(".log")] + "-" + str(file_counter) + ".csv"

                with open(output_dir + output_file_name, "w") as writer:
                    line_break_counter = 1
                    i_line = 1

                    writer.write("Time" + separator + "CPU" + separator + "RAM\n")

                    for line in reader:
                        if i_line == start_line + (line_break * line_break_counter):
                            line_break_counter = line_break_counter + 1
                            writer.write("\n")
                        elif i_line == start_line + (line_break * line_break_counter) - 3:
                            to_write = line[line.index("Time running: ") + len("Time running: "):].rstrip()
                            writer.write(to_write)
                            writer.write(separator)
                        elif i_line == start_line + (line_break * line_break_counter) - 2:
                            to_write = line[line.index("CPU: ") + len("CPU: "):len(line) - 2].rstrip()
                            writer.write(to_write)
                            writer.write(separator)
                        elif i_line == start_line + (line_break * line_break_counter) - 1:
                            to_write = line[line.index("RAM: ") + len("RAM: "):len(line) - 2].rstrip()
                            writer.write(to_write)

                        i_line = i_line + 1

                    writer.close()
                reader.close()
            file_counter = file_counter + 1
        break


if __name__ == '__main__':
    main()

