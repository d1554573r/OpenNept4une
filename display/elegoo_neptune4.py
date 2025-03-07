from mapping import *

class Neptune4Mapper(Mapper):
    page_mapping = {
        PAGE_MAIN: "1",
        PAGE_FILES: "2",
        PAGE_PREPARE_MOVE: "8",
        PAGE_PREPARE_TEMP: "95",
        PAGE_PREPARE_EXTRUDER: "9",

        PAGE_SETTINGS: "11",
        PAGE_SETTINGS_LANGUAGE: "12",
        PAGE_SETTINGS_TEMPERATURE: "32",
        PAGE_SETTINGS_TEMPERATURE_SET: "33",
        PAGE_SETTINGS_ABOUT: "35",
        PAGE_SETTINGS_ADVANCED: "42",

        PAGE_LEVELING: "14",

        PAGE_CONFIRM_PRINT: "18",
        PAGE_PRINTING: "19",
        PAGE_PRINTING_PAUSE: "25",
        PAGE_PRINTING_STOP: "26",
        PAGE_PRINTING_EMERGENCY_STOP: "106",
        PAGE_PRINTING_COMPLETE: "24",
        PAGE_PRINTING_FILAMENT: "28",
        PAGE_PRINTING_SPEED: "135",
        PAGE_PRINTING_ADJUST: "127",

        PAGE_OVERLAY_LOADING: "130",
        PAGE_LIGHTS: "84"
    }
    def __init__(self) -> None:
        super().__init__()
        self.data_mapping = {
            "extruder": {
                "temperature": [MappingLeaf([build_accessor(self.map_page(PAGE_MAIN), "nozzletemp"),
                                             build_accessor(self.map_page(PAGE_PREPARE_TEMP), "nozzletemp"),
                                             build_accessor(self.map_page(PAGE_PREPARE_EXTRUDER), "nozzletemp"),
                                             build_accessor(self.map_page(PAGE_PRINTING), "nozzletemp"),
                                             build_accessor(self.map_page(PAGE_PRINTING_FILAMENT), "nozzletemp")], formatter=format_temp)],
                "target": [MappingLeaf([build_accessor(self.map_page(PAGE_PREPARE_TEMP), 17)], formatter=lambda x: f"{x:.0f}")],

            },
            "heater_bed": {
                "temperature": [MappingLeaf([build_accessor(self.map_page(PAGE_MAIN), "bedtemp"),
                                             build_accessor(self.map_page(PAGE_PREPARE_TEMP), "bedtemp"),
                                             build_accessor(self.map_page(PAGE_PREPARE_EXTRUDER), "bedtemp"),
                                             build_accessor(self.map_page(PAGE_PRINTING), "bedtemp"),
                                             build_accessor(self.map_page(PAGE_PRINTING_FILAMENT), "bedtemp")], formatter=format_temp)],
                "target": [MappingLeaf([build_accessor(self.map_page(PAGE_PREPARE_TEMP), 18)], formatter=lambda x: f"{x:.0f}")],
            },
            "motion_report": {
                "live_position": {
                    0: [MappingLeaf([build_accessor(self.map_page(PAGE_MAIN), "x_pos")]),
                        MappingLeaf([build_accessor(self.map_page(PAGE_PRINTING), "x_pos")], formatter=lambda x: f"X[{x:3.2f}]")],
                    1: [MappingLeaf([build_accessor(self.map_page(PAGE_MAIN), "y_pos")]),
                        MappingLeaf([build_accessor(self.map_page(PAGE_PRINTING), "y_pos")], formatter=lambda y: f"Y[{y:3.2f}]")],
                    2: [MappingLeaf([build_accessor(self.map_page(PAGE_MAIN), "z_pos"), build_accessor(self.map_page(PAGE_PRINTING), "zvalue")])],
                },
                "live_velocity": [MappingLeaf([build_accessor(self.map_page(PAGE_PRINTING), "pressure_val")], formatter=lambda x: f"{x:3.2f}mm/s")],
            },
            "print_stats": {
                "print_duration": [MappingLeaf([build_accessor(self.map_page(PAGE_PRINTING), "6")], formatter=format_time)],
                "filename": [MappingLeaf([build_accessor(self.map_page(PAGE_PRINTING), "t0")], formatter=lambda x: x.replace(".gcode", ""))],
            },
            "gcode_move": {
                "extrude_factor": [MappingLeaf([build_accessor(self.map_page(PAGE_PRINTING), "flow_speed")], formatter=format_percent)],
                "speed_factor": [MappingLeaf([build_accessor(self.map_page(PAGE_PRINTING), "printspeed")], formatter=format_percent)],
                "homing_origin": {
                    2: [MappingLeaf([build_accessor(self.map_page(PAGE_PRINTING_ADJUST), "15")], formatter=lambda x: f"{x:.3f}")],
                }
            },
            "fan": {
                "speed": [MappingLeaf([build_accessor(self.map_page(PAGE_PRINTING), "fanspeed")], formatter=format_percent), MappingLeaf([build_accessor(self.map_page(PAGE_SETTINGS), "12")], field_type="pic", formatter=lambda x: "77" if int(x) == 1 else "76")]
            },
            "display_status": {
                "progress": [MappingLeaf([build_accessor(self.map_page(PAGE_PRINTING), "printvalue")], formatter=lambda x: f"{x * 100:2.1f}"), MappingLeaf([build_accessor(self.map_page(PAGE_PRINTING), "printprocess")], field_type="val", formatter=lambda x: f"{x * 100:.0f}")]
            },
            "output_pin Part_Light": {"value": [MappingLeaf([build_accessor(self.map_page(PAGE_LIGHTS), "led1")], field_type="pic", formatter=lambda x: "77" if int(x) == 1 else "76")]},
            "output_pin Frame_Light": {"value": [MappingLeaf([build_accessor(self.map_page(PAGE_LIGHTS), "led2")], field_type="pic", formatter= lambda x: "77" if int(x) == 1 else "76")]},
            "filament_switch_sensor fila": {"enabled": [MappingLeaf([build_accessor(self.map_page(PAGE_SETTINGS), "11"),
                                                                     build_accessor(self.map_page(PAGE_PRINTING_ADJUST), "16")], field_type="pic", formatter= lambda x: "77" if int(x) == 1 else "76")]}
        }

class Neptune4ProMapper(Neptune4Mapper):

    def __init__(self) -> None:
        self.page_mapping[PAGE_PREPARE_TEMP] = "6"
        self.page_mapping[PAGE_PRINTING_FILAMENT] = "27"
        super().__init__()
        self.data_mapping["extruder"]["target"] = [MappingLeaf([build_accessor(self.map_page(PAGE_PREPARE_TEMP), "nozzletemp_t"),
                                        build_accessor(self.map_page(PAGE_PRINTING_FILAMENT), "nozzletemp_t")], formatter=format_temp),
                                        MappingLeaf([build_accessor(self.map_page(PAGE_PREPARE_TEMP), 17)], formatter=lambda x: f"{x:.0f}")]
        self.data_mapping["heater_bed"]["target"] = [MappingLeaf([build_accessor(self.map_page(PAGE_PREPARE_TEMP), "bedtemp_t"),
                                        build_accessor(self.map_page(PAGE_PRINTING_FILAMENT), "bedtemp_t")], formatter=format_temp),
                                        MappingLeaf([build_accessor(self.map_page(PAGE_PREPARE_TEMP), 18)], formatter=lambda x: f"{x:.0f}")]
        self.data_mapping["heater_generic heater_bed_outer"] = {
                "temperature": [MappingLeaf([build_accessor(self.map_page(PAGE_MAIN), "out_bedtemp"),
                                             build_accessor(self.map_page(PAGE_PREPARE_TEMP), "out_bedtemp"),
                                             build_accessor(self.map_page(PAGE_PRINTING_FILAMENT), "out_bedtemp")], formatter=format_temp)],
                "target": [MappingLeaf([build_accessor(self.map_page(PAGE_PREPARE_TEMP), "out_bedtemp_t"),
                                        build_accessor(self.map_page(PAGE_PRINTING_FILAMENT), "out_bedtemp_t")], formatter=format_temp),
                                        MappingLeaf([build_accessor(self.map_page(PAGE_PREPARE_TEMP), 28)], formatter=lambda x: f"{x:.0f}")]
            }

class Neptune4PlusMapper(Neptune4Mapper):

    def __init__(self) -> None:
        super().__init__()

class Neptune4MaxMapper(Neptune4Mapper):

    def __init__(self) -> None:
        super().__init__()