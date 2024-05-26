def get_wind_farm_names_from_params():
    parameters = wind_farm_parameters()
    return [param[0] for param in parameters]


def get_wind_farm_param(windfarm_name):
    parameters = wind_farm_parameters()
    for param in parameters:
        if param[0] == windfarm_name:
            V0 = param[1]
            b = param[2]
            cut_in_speed = param[3]
            cut_out_speed = param[4]
            nameplate_power = param[5]
            return V0, b, cut_in_speed, cut_out_speed, nameplate_power
    return None


def wind_farm_parameters():
    # Define parameters for each wind farm
    w, h = 17, 99

    # Populate the parameters for each wind farm
    parameters = [[0 for x in range(w)] for y in range(h)]
    # Each list item includes: wind_farm, V0, b, cut in speed, cut out speed, nameplate power, derate factor, SWIS, start_year, hub height, region, roughness, full_name, rated_speed, ground elevation, dist. to coast, state
    parameters[0] = ['ALBANY_WF1', 9.395, 0.696, 3.5, 25, 21.6,
                     0.95, True, 2001, 65, 'R', 0.1, 'Albany', 14, 82, 0, 'WA']
    parameters[1] = ['COLLGAR_WF1', 8.05, 0.993, 3.5, 25, 206, 0.92,
                     True, 2011, 80, 'R', 0.1, 'Collgar', 14.5, 410, 290, 'WA']
    parameters[2] = ['GUNNING1', 8.383, 0.688, 4, 25, 46.5, 0.97,
                     False, 2011, 80, 'R', 0.1, 'Gunning', 11.6, 709, 100, 'NSW']
    parameters[3] = ['MTMILLAR', 9, 0.818, 2, 25, 70, 0.93, False,
                     2006, 85, 'R', 0.1, 'Mount_Millar', 14, 356, 20, 'NSW']
    parameters[4] = ['MWF_MUMBIDA_WF1', 8.41, 0.819, 3.5, 25, 55,
                     0.98, True, 2013, 80, 'R', 0.1, 'Mumbida', 13.5, 222, 14, 'WA']
    parameters[5] = ['MUSSELR1', 9.1, 0.713, 3.5, 25, 168, 0.97,
                     False, 2013, 80, 'R', 0.1, 'Musselroe', 16.5, 28, 0, 'TAS']
    parameters[6] = ['STARHLWF', 9.023, 0.817, 4.5, 25, 35, 0.87,
                     False, 2003, 68, 'R', 0.1, 'Starfish Hill', 15, 155, 0, 'SA']
    parameters[7] = ['WPWF', 9.024, 0.963, 3.5, 25, 91, 0.97, False,
                     2005, 68, 'R', 0.1, 'Wattle Point', 17.5, 10, 0, 'SA']
    parameters[8] = ['WOODLWN1', 8.965, 0.934, 3.5, 25, 48.3, 0.98,
                     False, 2011, 80, 'R', 0.1, 'Woodlawn', 14, 789, 88, 'NSW']
    parameters[9] = ['WOOLNTH1', 9.1, 0.713, 3.5, 25, 140, 0.94,
                     False, 2007, 80, 'R', 0.1, 'Woolnorth', 16.5, 34, 0, 'TAS']
    parameters[10] = ['CNUNDAWF', 8.98, 0.62, 3.5, 25, 46, 0.93,
                      False, 2005, 67, 'R', 0.1, 'Canunda', 14.5, 46, 9, 'SA']
    parameters[11] = ['CAPTL_WF', 8.965, 0.934, 3.5, 25, 140, 0.94,
                      False, 2010, 80, 'R', 0.1, 'Capital', 14, 877, 84, 'NSW']
    parameters[12] = ['GULLRWF1', 8.538, 0.789, 2.5, 25, 161, 0.98,
                      False, 2014, 80, 'R', 0.1, 'Gullen Range', 13, 920, 127, 'NSW']
    parameters[13] = ['TARALGA1', 8.05, 0.993, 3.5, 25, 106.8, 0.98,
                      False, 2015, 80, 'R', 0.1, 'Taralga', 14.5, 933, 93, 'NSW']
    parameters[14] = ['CTHLWF1', 9.100, 0.713, 3.5, 25,  154,  0.90,
                      False, 2020, 110, 'R', 0.1, 'Cattle Hill', 10.5, 878, 90, 'TAS']
    parameters[15] = ['GRANWF1', 9.100, 0.713, 3.5, 25,  112,  0.90,
                      False, 2020, 137, 'R', 0.1, 'Granville_Harbour', 11.5, 111, 2, 'TAS']
    parameters[18] = ['GULLRWF2', 7.751, 0.852, 3, 25, 110.7, 0.92,
                      False, 2014, 110, 'R', 0.1, 'Gullen Range', 12, 920, 127, 'NSW']
    parameters[19] = ['YENDWF1', 8.25, 0.914, 2.5, 22, 144.4, 0.93,
                      False, 2019, 93, 'R', 0.1, 'Yendon_(Lal_Lal_1)', 11, 498, 59, 'VIC']
    parameters[21] = ['CHALLHWF', 9.023, 0.817, 5, 25, 52, 0.92, False,
                      2003, 68, 'R', 0.1, 'Challicum_Hills', 15, 264, 101, 'VIC']
    parameters[22] = ['LKBONNY1', 9.11, 0.614, 3.5, 25, 80.5, 0.96,
                      False, 2005, 67, 'R', 0.1, 'Lake_Bonney_1', 16, 26, 8, 'SA']
    parameters[23] = ['CATHROCK', 8.98, 0.62, 3.5, 25, 66, 0.91,
                      False, 2007, 60, 'R', 0.1, 'Cathedral_Rocks', 14.5, 124, 0, 'SA']
    parameters[24] = ['HALLWF1', 8.965, 0.934, 3.5, 25, 94.5, 0.97, False,
                      2008, 80, 'R', 0.1, 'Hallett_Stage_1_Brown_Hill', 14, 730, 69, 'SA']
    parameters[25] = ['LKBONNY2', 9.1, 0.713, 3.5, 25, 159, 0.93,
                      False, 2008, 80, 'R', 0.1, 'Lake_Bonney_2', 16.5, 26, 8, 'SA']
    parameters[28] = ['HALLWF2', 8.965, 0.934, 3.5, 25, 71.4, 0.94, False,
                      2010, 80, 'R', 0.1, 'Hallett_Stage_2_Hallett_Hill', 14, 730, 69, 'SA']
    parameters[29] = ['LKBONNY3', 9.1, 0.713, 3.5, 25, 39, 0.94,
                      False, 2010, 80, 'R', 0.1, 'Lake_Bonney_3', 16.5, 26, 8, 'SA']
    parameters[30] = ['NBHWF1', 8.965, 0.934, 3.5, 25, 132.3, 0.97, False,
                      2010, 80, 'R', 0.1, 'Hallett_4_North_Brown_Hill', 14, 730, 69, 'SA']
    parameters[31] = ['WATERLWF', 9.1, 0.713, 3.5, 25, 131, 0.97,
                      False, 2011, 90, 'R', 0.1, 'Waterloo', 16.5, 565, 72, 'SA']
    parameters[32] = ['BLUFF1', 8.965, 0.934, 3.5, 25, 52.5, 0.99, False,
                      2012, 80, 'R', 0.1, 'Hallett_5_The_Bluff', 14, 730, 69, 'SA']
    parameters[33] = ['OAKLAND1', 8.965, 0.934, 3.5, 25, 67.2, 0.91,
                      False, 2012, 80, 'R', 0.1, 'Oaklands_Hill', 14, 354, 75, 'VIC']
    parameters[35] = ['GULLRWF2', 9.1, 0.713, 2, 20, 107, 0.92, False,
                      2014, 80, 'R', 0.1, 'Gullen_Range', 10.5, 920, 127, 'NSW']
    parameters[36] = ['MERCER01', 8.589, 0.702, 4, 22, 131.2, 0.93,
                      False, 2014, 80, 'R', 0.1, 'Mount_Mercer', 14.5, 342, 53, 'VIC']
    parameters[37] = ['SNOWNTH1', 8.965, 0.934, 3.5, 25, 144, 0.97, False,
                      2014, 80, 'R', 0.1, 'Snowtown_Stage_2_North', 14, 333, 28, 'SA']
    parameters[38] = ['SNOWSTH1', 8.705, 0.69, 3.5, 25, 126, 0.97,
                      False, 2014, 80, 'R', 0.1, 'Snowtown_South', 14.5, 333, 28, 'SA']
    parameters[39] = ['BALDHWF1', 8.212, 0.71, 3.5, 22, 106.6, 0.96,
                      False, 2015, 85, 'R', 0.1, 'Bald_Hills', 13, 72, 5, 'VIC']
    parameters[40] = ['ARWF1', 7.719, 0.825, 3, 25, 240, 0.82,
                      False, 2017, 85, 'R', 0.1, 'Ararat', 13, 402, 137, 'VIC']
    parameters[41] = ['HDWF1', 7.719, 0.825, 2.5, 22, 102.4, 0.97, False,
                      2017, 92.5, 'R', 0.1, 'Hornsdale_Stage_1', 13.5, 610, 47, 'SA']
    parameters[42] = ['HDWF2', 7.719, 0.825, 2.5, 22, 102.4, 0.97, False,
                      2017, 92.5, 'R', 0.1, 'Hornsdale_Stage_2', 13.5, 610, 47, 'SA']
    parameters[43] = ['HDWF3', 7.719, 0.825, 2.5, 22, 112, 0.96, False,
                      2017, 92.5, 'R', 0.1, 'Hornsdale_Stage_3', 13.5, 610, 47, 'SA']
    parameters[45] = ['CROOKWF2', 7.83, 0.77, 3, 25, 96, 0.96,
                      False, 2018, 95, 'R', 0.1, 'Crookwell_2', 12, 926, 125, 'NSW']
    parameters[46] = ['MTGELWF1', 8.383, 0.688, 3.5, 25, 66, 0.98, False,
                      2018, 87.5, 'R', 0.1, 'Mount_Gellibrand', 12, 143, 36, 'VIC']
    parameters[47] = ['SALTCRK1', 8.25, 0.914, 4.5, 25, 54, 0.96,
                      False, 2018, 87, 'R', 0.1, 'Salt_Creek', 11.5, 222, 59, 'VIC']
    parameters[48] = ['SAPHWF1', 8.25, 0.914, 4.5, 25, 270, 0.95,
                      False, 2018, 137, 'R', 0.1, 'Sapphire', 11.5, 1008, 161, 'NSW']
    parameters[49] = ['WRWF1', 7.208, 0.806, 3, 22, 172.5, 0.96, False,
                      2018, 89.5, 'R', 0.1, 'White_Rock_Stage_1', 11, 1314, 162, 'NSW']
    parameters[50] = ['YSWF1', 8.212, 0.71, 3.5, 22, 28.7, 0.98,
                      False, 2018, 80, 'R', 0.1, 'Yaloak_South', 13, 424, 41, 'VIC']
    parameters[51] = ['BADGINGARRA_WF1', 7.643, 0.946, 2.5, 25, 130,
                      0.99, True, 2019, 85, 'R', 0.1, 'Badgingarra', 13, 123, 25, 'WA']
    parameters[52] = ['BODWF1', 7.83, 0.77, 3, 25, 113.2, 0.98,
                      False, 2019, 85, 'R', 0.1, 'Bodangora', 12, 484, 217, 'NSW']
    parameters[54] = ['CROWLWF1', 8.212, 0.71, 3.5, 22, 80, 0.95,
                      False, 2019, 100, 'R', 0.1, 'Crowlands', 13, 336, 151, 'VIC']
    parameters[55] = ['MEWF1', 8.718, 0.828, 4, 25, 180.5, 0.98,
                      False, 2019, 90, 'R', 0.1, 'Mount_Emerald', 11.5, 900, 50, 'QLD']
    parameters[56] = ['WGWF1', 7.83, 0.77, 3, 25, 119.4, 0.98,
                      False, 2019, 85, 'R', 0.1, 'Willogoleche', 12, 659, 80, 'SA']
    parameters[57] = ['CHYTWF1', 8.25, 0.914, 2.5, 22, 57.6, 0.98,
                      False, 2020, 91, 'R', 0.1, 'Cherry_Tree', 11, 510, 87, 'VIC']
    parameters[58] = ['COOPGWF1', 7.83, 0.77, 3, 25, 452.9, 0.94,
                      False, 2020, 110, 'R', 0.1, 'Coopers_Gap', 12, 667, 160, 'QLD']
    parameters[59] = ['CRURWF1', 7.83, 0.77, 3, 25, 141, 0.97, False,
                      2020, 91.5, 'R', 0.1, 'Crudine_Ridge', 12, 768, 141, 'NSW']
    parameters[60] = ['DUNDWF1', 7.33, 0.823, 3, 22.5, 168, 0.97,
                      False, 2020, 114, 'R', 0.1, 'Dundonnell', 9.9, 215, 71, 'VIC']
    parameters[61] = ['DUNDWF2', 7.33, 0.823, 3, 22.5, 46.2, 0.97,
                      False, 2020, 114, 'R', 0.1, 'Dundonnell', 9.9, 215, 71, 'VIC']
    parameters[62] = ['DUNDWF3', 7.33, 0.823, 3, 22.5, 121.8, 0.98,
                      False, 2020, 114, 'R', 0.1, 'Dundonnell', 9.9, 215, 71, 'VIC']
    parameters[63] = ['LGAPWF1', 7.256, 0.95, 2.5, 21, 126, 0.96,
                      False, 2020, 110, 'R', 0.1, 'Lincoln_Gap', 11, 344, 149, 'SA']
    parameters[64] = ['MUWAWF1', 7.256, 0.95, 2.5, 26, 225.7, 0.95, False,
                      2020, 139, 'R', 0.1, 'Murra_Warra_stage_1', 11.5, 133, 205, 'VIC']
    parameters[65] = ['STWF1', 7.83, 0.77, 3, 25, 198.9, 0.95,
                      False, 2020, 110, 'R', 0.1, 'Silverton', 12, 304, 330, 'NSW']
    parameters[67] = ['COLWF01', 8.718, 0.828, 3, 25, 219, 0.94,
                      False, 2021, 91.5, 'R', 0.1, 'Collector', 12, 754, 120, 'NSW']
    parameters[72] = ['YANDIN_WF1', 7.33, 0.823, 3, 22.5, 211.68,
                      0.94, True, 2021, 105, 'R', 0.1, 'Yandin', 9.9, 181, 47, 'WA']
    parameters[76] = ['BOCORWF1', 8.41, 0.819, 3.5, 23, 113, 0.97,
                      False, 2015, 80, 'R', 0.1, 'Boco_Rock', 11, 988, 80, 'NSW']

    return (parameters)
