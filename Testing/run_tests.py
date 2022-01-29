def test_divergence():
    thing = {"NAME": "Yakutat City and Borough, Alaska", "state": "02", "county": "282", "BROWN": 55.0, "POP": 649.0,
             "Sub_Areas": [
                 {"state": "02", "county": "282", "tract": "000100", "BROWN": 55.0, "POP": 649.0, "Sub_Areas": [
                     {"state": "02", "county": "282", "tract": "000100", "block group": "1", "BROWN": 55.0,
                      "POP": 649.0,
                      "Valid": True, "Divergence": 0.0}]
                     # county_tracts = {"NAME": "St. Clair County, Alabama", "state": "01", "county": "115", "BROWN": 10551.0,
                     #                  "POP": 87989.0,
                     #                  "Sub_Areas": [{"state": "01", "county": "115", "tract": "040103", "BROWN": 1123.0, "POP": 9311.0},
                     #                                {"state": "01", "county": "115", "tract": "040104", "BROWN": 678.0, "POP": 4955.0},
                     #                                {"state": "01", "county": "115", "tract": "040105", "BROWN": 813.0, "POP": 4996.0},
                     #                                {"state": "01", "county": "115", "tract": "040106", "BROWN": 628.0, "POP": 6942.0},
                     #                                {"state": "01", "county": "115", "tract": "040204", "BROWN": 442.0, "POP": 7009.0},
                     #                                {"state": "01", "county": "115", "tract": "040205", "BROWN": 250.0, "POP": 5989.0},
                     #                                {"state": "01", "county": "115", "tract": "040401", "BROWN": 837.0, "POP": 5301.0},
                     #                                {"state": "01", "county": "115", "tract": "040402", "BROWN": 309.0, "POP": 3597.0},
                     #                                {"state": "01", "county": "115", "tract": "040501", "BROWN": 693.0, "POP": 11271.0},
                     #                                {"state": "01", "county": "115", "tract": "040300", "BROWN": 273.0, "POP": 5328.0},
                     #                                {"state": "01", "county": "115", "tract": "040201", "BROWN": 355.0, "POP": 6143.0},
                     #                                {"state": "01", "county": "115", "tract": "040502", "BROWN": 3035.0, "POP": 10775.0},
                     #                                {"state": "01", "county": "115", "tract": "040203", "BROWN": 1115.0, "POP": 6372.0}]}
                     # county_blocks = {"NAME": "St. Clair County, Alabama", "state": "01", "county": "115", "BROWN": 10551.0,
                     #                  "POP": 87989.0, "Sub_Areas": [
                     #         {"state": "01", "county": "115", "tract": "040103", "BROWN": 1123.0, "POP": 9311.0, "Sub_Areas": [
                     #             {"state": "01", "county": "115", "tract": "040103", "block group": "2", "BROWN": 618.0, "POP": 5228.0},
                     #             {"state": "01", "county": "115", "tract": "040103", "block group": "1", "BROWN": 505.0,
                     #              "POP": 4083.0}]}, {"state": "01", "county": "115", "tract": "040104", "BROWN": 678.0, "POP": 4955.0,
                     #                                 "Sub_Areas": [
                     #                                     {"state": "01", "county": "115", "tract": "040104", "block group": "2",
                     #                                      "BROWN": 351.0, "POP": 2872.0},
                     #                                     {"state": "01", "county": "115", "tract": "040104", "block group": "1",
                     #                                      "BROWN": 327.0, "POP": 2083.0}]},
                     #         {"state": "01", "county": "115", "tract": "040105", "BROWN": 813.0, "POP": 4996.0, "Sub_Areas": [
                     #             {"state": "01", "county": "115", "tract": "040105", "block group": "2", "BROWN": 222.0, "POP": 1768.0},
                     #             {"state": "01", "county": "115", "tract": "040105", "block group": "1", "BROWN": 591.0,
                     #              "POP": 3228.0}]}, {"state": "01", "county": "115", "tract": "040106", "BROWN": 628.0, "POP": 6942.0,
                     #                                 "Sub_Areas": [
                     #                                     {"state": "01", "county": "115", "tract": "040106", "block group": "1",
                     #                                      "BROWN": 487.0, "POP": 2311.0},
                     #                                     {"state": "01", "county": "115", "tract": "040106", "block group": "2",
                     #                                      "BROWN": 141.0, "POP": 3437.0},
                     #                                     {"state": "01", "county": "115", "tract": "040106", "block group": "3",
                     #                                      "BROWN": 0.0, "POP": 1194.0}]},
                     #         {"state": "01", "county": "115", "tract": "040204", "BROWN": 442.0, "POP": 7009.0, "Sub_Areas": [
                     #             {"state": "01", "county": "115", "tract": "040204", "block group": "1", "BROWN": 387.0, "POP": 4775.0},
                     #             {"state": "01", "county": "115", "tract": "040204", "block group": "2", "BROWN": 49.0, "POP": 1499.0},
                     #             {"state": "01", "county": "115", "tract": "040204", "block group": "3", "BROWN": 6.0, "POP": 735.0}]},
                     #         {"state": "01", "county": "115", "tract": "040205", "BROWN": 250.0, "POP": 5989.0, "Sub_Areas": [
                     #             {"state": "01", "county": "115", "tract": "040205", "block group": "1", "BROWN": 32.0, "POP": 1556.0},
                     #             {"state": "01", "county": "115", "tract": "040205", "block group": "3", "BROWN": 197.0, "POP": 2910.0},
                     #             {"state": "01", "county": "115", "tract": "040205", "block group": "2", "BROWN": 21.0, "POP": 1523.0}]},
                     #         {"state": "01", "county": "115", "tract": "040401", "BROWN": 837.0, "POP": 5301.0, "Sub_Areas": [
                     #             {"state": "01", "county": "115", "tract": "040401", "block group": "2", "BROWN": 510.0, "POP": 1421.0},
                     #             {"state": "01", "county": "115", "tract": "040401", "block group": "3", "BROWN": 277.0, "POP": 2512.0},
                     #             {"state": "01", "county": "115", "tract": "040401", "block group": "1", "BROWN": 50.0, "POP": 1368.0}]},
                     #         {"state": "01", "county": "115", "tract": "040402", "BROWN": 309.0, "POP": 3597.0, "Sub_Areas": [
                     #             {"state": "01", "county": "115", "tract": "040402", "block group": "2", "BROWN": 132.0, "POP": 996.0},
                     #             {"state": "01", "county": "115", "tract": "040402", "block group": "3", "BROWN": 122.0, "POP": 836.0},
                     #             {"state": "01", "county": "115", "tract": "040402", "block group": "1", "BROWN": 55.0, "POP": 1765.0}]},
                     #         {"state": "01", "county": "115", "tract": "040501", "BROWN": 693.0, "POP": 11271.0, "Sub_Areas": [
                     #             {"state": "01", "county": "115", "tract": "040501", "block group": "1", "BROWN": 37.0, "POP": 3701.0},
                     #             {"state": "01", "county": "115", "tract": "040501", "block group": "4", "BROWN": 444.0, "POP": 4165.0},
                     #             {"state": "01", "county": "115", "tract": "040501", "block group": "3", "BROWN": 173.0, "POP": 627.0},
                     #             {"state": "01", "county": "115", "tract": "040501", "block group": "2", "BROWN": 39.0, "POP": 2778.0}]},
                     #         {"state": "01", "county": "115", "tract": "040300", "BROWN": 273.0, "POP": 5328.0, "Sub_Areas": [
                     #             {"state": "01", "county": "115", "tract": "040300", "block group": "2", "BROWN": 155.0, "POP": 1124.0},
                     #             {"state": "01", "county": "115", "tract": "040300", "block group": "3", "BROWN": 18.0, "POP": 2716.0},
                     #             {"state": "01", "county": "115", "tract": "040300", "block group": "1", "BROWN": 100.0,
                     #              "POP": 1488.0}]}, {"state": "01", "county": "115", "tract": "040201", "BROWN": 355.0, "POP": 6143.0,
                     #                                 "Sub_Areas": [
                     #                                     {"state": "01", "county": "115", "tract": "040201", "block group": "1",
                     #                                      "BROWN": 352.0, "POP": 1417.0},
                     #                                     {"state": "01", "county": "115", "tract": "040201", "block group": "3",
                     #                                      "BROWN": 0.0, "POP": 1384.0},
                     #                                     {"state": "01", "county": "115", "tract": "040201", "block group": "4",
                     #                                      "BROWN": 0.0, "POP": 1740.0},
                     #                                     {"state": "01", "county": "115", "tract": "040201", "block group": "2",
                     #                                      "BROWN": 3.0, "POP": 1602.0}]},
                     #         {"state": "01", "county": "115", "tract": "040502", "BROWN": 3035.0, "POP": 10775.0, "Sub_Areas": [
                     #             {"state": "01", "county": "115", "tract": "040502", "block group": "3", "BROWN": 1074.0, "POP": 3383.0},
                     #             {"state": "01", "county": "115", "tract": "040502", "block group": "4", "BROWN": 113.0, "POP": 1893.0},
                     #             {"state": "01", "county": "115", "tract": "040502", "block group": "1", "BROWN": 1508.0, "POP": 3458.0},
                     #             {"state": "01", "county": "115", "tract": "040502", "block group": "2", "BROWN": 340.0,
                     #              "POP": 2041.0}]}, {"state": "01", "county": "115", "tract": "040203", "BROWN": 1115.0, "POP": 6372.0,
                     #                                 "Sub_Areas": [
                     #                                     {"state": "01", "county": "115", "tract": "040203", "block group": "1",
                     #                                      "BROWN": 471.0, "POP": 2881.0},
                     #                                     {"state": "01", "county": "115", "tract": "040203", "block group": "3",
                     #                                      "BROWN": 601.0, "POP": 1837.0},
                     #                                     {"state": "01", "county": "115", "tract": "040203", "block group": "2",
                     #                                      "BROWN": 43.0, "POP": 1654.0}]}]}

                     # print(calc_divergence(county_blocks))
                     # pprint.pprint(county_blocks)
                     # print(calc_iso(county_blocks))
                     # print(calc_iso(county_tracts))
                     # print(calc_divergence(county_tracts))

                     test_divergence()
