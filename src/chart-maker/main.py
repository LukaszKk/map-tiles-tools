import shutil
import os
import csv
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np


def prepareLogFile(input_dir, output_dir, separator):
    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(output_dir)

    start_line = 6
    line_break = 4

    for (dir_path, dir_names, filenames) in os.walk(input_dir):
        for file in filenames:
            with open(input_dir + file, "r") as reader:
                output_file_name = file[0:file.index(".log")] + "-" + file.split(".")[2] + ".csv"

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
        break


def loadFileData(file, output_dir, group, separator, time, cpu, ram, file_idx, single):
    if any(pre == file for pre in group):
        with open(output_dir + file, "r", newline='') as reader:
            csv_reader = csv.reader(reader, delimiter=separator)
            header = True
            for row in csv_reader:
                if header:
                    header = False
                    continue

                for (i, v) in enumerate(row):
                    if i == 0:
                        if not single:
                            time[file_idx].append(v)
                        else:
                            time.append(v)
                    elif i == 1:
                        if not single:
                            cpu[file_idx].append(float(v))
                        else:
                            cpu.append(float(v))
                    elif i == 2:
                        if not single:
                            ram[file_idx].append(float(v))
                        else:
                            ram.append(float(v))
        reader.close()
        return True

    return False


def createCharts(output_dir, separator):
    group_7_50k_files = ["logfile-1.csv", "logfile-2.csv", "logfile-3.csv"]
    group_3_50k_files = ["logfile-4.csv", "logfile-5.csv", "logfile-6.csv"]
    group_7_250k_files = ["logfile-7.csv", "logfile-8.csv", "logfile-9.csv"]
    group_3_250k_files = ["logfile-10.csv", "logfile-11.csv", "logfile-12.csv"]
    group_1_250k_files = ["logfile-13.csv"]
    group_1_50k_files = ["logfile-14.csv"]

    time_7_50k = [[], [], []]
    cpu_7_50k = [[], [], []]
    ram_7_50k = [[], [], []]

    time_3_50k = [[], [], []]
    cpu_3_50k = [[], [], []]
    ram_3_50k = [[], [], []]

    time_7_250k = [[], [], []]
    cpu_7_250k = [[], [], []]
    ram_7_250k = [[], [], []]

    time_3_250k = [[], [], []]
    cpu_3_250k = [[], [], []]
    ram_3_250k = [[], [], []]

    time_1_250k = []
    cpu_1_250k = []
    ram_1_250k = []

    time_1_50k = []
    cpu_1_50k = []
    ram_1_50k = []

    for (dir_path, dir_names, filenames) in os.walk(output_dir):
        file_idx_7_50k = 0
        file_idx_3_50k = 0
        file_idx_7_250k = 0
        file_idx_3_250k = 0
        file_idx_1_250k = 0
        file_idx_1_50k = 0
        for file in filenames:

            if loadFileData(file, output_dir, group_7_50k_files, separator, time_7_50k, cpu_7_50k, ram_7_50k,
                            file_idx_7_50k, False):
                file_idx_7_50k = file_idx_7_50k + 1

            if loadFileData(file, output_dir, group_3_50k_files, separator, time_3_50k, cpu_3_50k, ram_3_50k,
                            file_idx_3_50k, False):
                file_idx_3_50k = file_idx_3_50k + 1

            if loadFileData(file, output_dir, group_7_250k_files, separator, time_7_250k, cpu_7_250k, ram_7_250k,
                            file_idx_7_250k, False):
                file_idx_7_250k = file_idx_7_250k + 1

            if loadFileData(file, output_dir, group_3_250k_files, separator, time_3_250k, cpu_3_250k, ram_3_250k,
                            file_idx_3_250k, False):
                file_idx_3_250k = file_idx_3_250k + 1

            if loadFileData(file, output_dir, group_1_250k_files, separator, time_1_250k, cpu_1_250k, ram_1_250k,
                            file_idx_1_250k, True):
                file_idx_1_250k = file_idx_1_250k + 1

            if loadFileData(file, output_dir, group_1_50k_files, separator, time_1_50k, cpu_1_50k, ram_1_50k,
                            file_idx_1_50k, True):
                file_idx_1_50k = file_idx_1_50k + 1

    # ==================== 7 250k

    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=time_7_250k[1], y=cpu_7_250k[1],
    #                          mode='lines',
    #                          name='multiprocessing'))
    # fig.add_trace(go.Scatter(x=time_7_250k[0], y=cpu_7_250k[0],
    #                          mode='lines',
    #                          name='multithreading'))
    # fig.add_trace(go.Scatter(x=time_7_250k[2], y=cpu_7_250k[2],
    #                          mode='lines',
    #                          name='ray'))
    # fig.update_layout(
    #     title="CPU Usage: data-250k, groups-7",
    #     xaxis_title="Time",
    #     yaxis_title="CPU %",
    #     legend_title="Legend",
    #     font=dict(
    #         family="Courier New, monospace",
    #         size=18,
    #         color="RebeccaPurple"
    #     )
    # )
    #
    # fig.show()
    #
    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=time_7_250k[1], y=ram_7_250k[1],
    #                          mode='lines',
    #                          name='multiprocessing'))
    # fig.add_trace(go.Scatter(x=time_7_250k[0], y=ram_7_250k[0],
    #                          mode='lines',
    #                          name='multithreading'))
    # fig.add_trace(go.Scatter(x=time_7_250k[2], y=ram_7_250k[2],
    #                          mode='lines',
    #                          name='ray'))
    # fig.update_layout(
    #     title="RAM Usage: data-250k, groups-7",
    #     xaxis_title="Time",
    #     yaxis_title="RAM %",
    #     legend_title="Legend",
    #     font=dict(
    #         family="Courier New, monospace",
    #         size=18,
    #         color="RebeccaPurple"
    #     )
    # )
    #
    # fig.show()
    #
    # # ==================== 3 250k
    #
    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=time_3_250k[2], y=cpu_3_250k[2],
    #                          mode='lines',
    #                          name='multiprocessing'))
    # fig.add_trace(go.Scatter(x=time_3_250k[1], y=cpu_3_250k[1],
    #                          mode='lines',
    #                          name='multithreading'))
    # fig.add_trace(go.Scatter(x=time_3_250k[0], y=cpu_3_250k[0],
    #                          mode='lines',
    #                          name='ray'))
    # fig.update_layout(
    #     title="CPU Usage: data-250k, groups-3",
    #     xaxis_title="Time",
    #     yaxis_title="CPU %",
    #     legend_title="Legend",
    #     font=dict(
    #         family="Courier New, monospace",
    #         size=18,
    #         color="RebeccaPurple"
    #     )
    # )
    #
    # fig.show()
    #
    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=time_3_250k[2], y=ram_3_250k[2],
    #                          mode='lines',
    #                          name='multiprocessing'))
    # fig.add_trace(go.Scatter(x=time_3_250k[1], y=ram_3_250k[1],
    #                          mode='lines',
    #                          name='multithreading'))
    # fig.add_trace(go.Scatter(x=time_3_250k[0], y=ram_3_250k[0],
    #                          mode='lines',
    #                          name='ray'))
    # fig.update_layout(
    #     title="RAM Usage: data-250k, groups-3",
    #     xaxis_title="Time",
    #     yaxis_title="RAM %",
    #     legend_title="Legend",
    #     font=dict(
    #         family="Courier New, monospace",
    #         size=18,
    #         color="RebeccaPurple"
    #     )
    # )
    #
    # fig.show()

    # ==================== 7 50k

    time_7_50k[0] = time_7_50k[0][::20]
    cpu_7_50k[2] = cpu_7_50k[2][::20]
    cpu_7_50k[1] = cpu_7_50k[1][::20]
    cpu_7_50k[0] = cpu_7_50k[0][::20]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_7_50k[0], y=cpu_7_50k[2],
                             mode='lines',
                             name='multithreading'))
    fig.add_trace(go.Scatter(x=time_7_50k[0], y=cpu_7_50k[1],
                             mode='lines',
                             name='multiprocessing'))
    fig.add_trace(go.Scatter(x=time_7_50k[0], y=cpu_7_50k[0],
                             mode='lines',
                             name='ray'))
    fig.update_layout(
        title="CPU Usage: data-50k, groups-7",
        xaxis_title="Time",
        yaxis_title="CPU %",
        legend_title="Legend",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )

    fig.show()

    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=time_7_50k[1], y=ram_7_50k[1],
    #                          mode='lines',
    #                          name='multiprocessing'))
    # fig.add_trace(go.Scatter(x=time_7_50k[0], y=ram_7_50k[0],
    #                          mode='lines',
    #                          name='multithreading'))
    # fig.add_trace(go.Scatter(x=time_7_50k[2], y=ram_7_50k[2],
    #                          mode='lines',
    #                          name='ray'))
    # fig.update_layout(
    #     title="RAM Usage: data-50k, groups-7",
    #     xaxis_title="Time",
    #     yaxis_title="RAM %",
    #     legend_title="Legend",
    #     font=dict(
    #         family="Courier New, monospace",
    #         size=18,
    #         color="RebeccaPurple"
    #     )
    # )
    #
    # fig.show()


def main():
    input_dir = "..\\..\\logs\\"
    output_dir = "..\\..\\logs\\output\\"
    separator = "|"
    # prepareLogFile(input_dir, output_dir, separator)
    createCharts(output_dir, separator)


if __name__ == '__main__':
    main()

