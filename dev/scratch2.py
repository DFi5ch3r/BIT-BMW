def CoG_TranslationTable():
    """
    Creates a translation table for CoG data.

    Returns:
        dict: A dictionary where keys are strings in CoG data and values are lists of corresponding strings in measurement data.
    """
    trans_tab = {
        "Batterie (Blei)": ["Batterie"],
        "Blinker / FIBL": ["Blinker_h_l", "Blinker_h_r", "Blinker_hi_li", "Blinker_hi_re", "Blinker_v_l", "Blinker_v_r", "Blinker_vo_li", "Blinker_vo_re", "Blinker_LH_o_A", "Blinker_RH_o_A", "Blinker_hi_li", "Blinker_hi_re", "Blinker_vo_li", "Blinker_vo_re"],
        "Federung Hinten": ["FB_H_o", "FB_H_u", "FB_hi_ob_Ant", "FB_hi_un_Ant", "Federb_hi_Ant_o", "Federb_hi_Ant_u", "Federb_hi_Ausgl"],
        "Frontträger": ["FrontTr_l_u", "FrontTr_r_u", "Frontr_Ant_o", "Frontr_Ant_o", "Frontr_Ant_u", "Fronttr_Antw_ob", "Fronttr_Antw_u"],
        "HECU": ["Hecu", "Hecu Anb", "Hecu2", "Hecu_A", "Hecu_Anb", "Hecu_StG_Deck_re", "Hecu", "Hecu Anb", "Hecu_A", "Hecu_Anb", "Hecu_u_Anb"],
        "Heckleute": ["Heckl_Anb", "Heckl_Ant", "Heckl_oben"],
        "HRM": ["HeckR_re_vo_ob", "HeckRa_RAP_L", "HeckRa_RAP_R", "HeckRa_RAP_l", "HeckRa_RAP_r", "HeckRa_l_m_o", "HeckRa_l_m_u", "HeckRa_l_o_A", "HeckRa_l_u_A", "HeckRa_r_m_o", "HeckRa_r_m_u", "HeckRa_r_o_A", "HeckRa_r_u_A", "Heckr_RAP_li", "Heckr_RAP_re", "Heckr_li_hi", "Heckr_re_hi", "HeckRa_RAP_l", "HeckRa_RAP_r", "HeckRa_l_o_A", "HeckRa_r_o_A", "Heckr_RAP_li", "Heckr_RAP_re", "Heckr_li_mi_o", "Heckr_li_mi_ob", "Heckr_re_hi", "Heckr_re_mit_ob", "Heckr_re_mit_u", "Heckr_re_vo_ob", "Heckr_re_vo_u", "Heckr_li_vo_o", "Heckr_li_vo_ob", "Heckr_li_vo_u", "Heckr_re_mi_o", "Heckr_re_mi_ob", "Heckr_re_vo_o", "Heckr_re_vo_ob", "Heckr_re_vo_u"],
        "I-Kombi": ["I-Kombi", "I-Kombi_ob"],
        "Kennzeichenträger": ["KennzTr_l_o_A", "KennzTr_r_o_A", "KennzTräger"],
        "Kennzeichnenleuchte": ["KennzL_m", "KennzLeuchte", "KennzLeuchte_Anb", "KennzLeuchte"],
        "Keylessride": ["KeylRide_Anb_GP", "KeylRide_Anb_Tr", "KeylRide_Anb_li", "KeylRide_Anb_re", "KeylRide_GrPl_li", "KeylRide_GrPl_re", "KeylRide_ob_hi", "KeylRide_ob_vo", "Keyl_Anb_rs_li", "Keyl_Ant_o_hi", "Keyl_Ant_o_vo", "Keyl_GrPl_li", "Keyl_GrPl_re", "Keyl_Halter_li_o", "Keyl_Halter_li_u", "Keyl_Ride_Anb", "Keyl_Ride_Ant", "Keyl_Ride_Ant_Gr", "Keyl_Ride_Ant_ob"],
        "Kofferträger": ["Koffer_Anb_li", "Koffer_Anb_re"],
        "Lenkerarmaturen": ["LKR-Arma_L", "LKR-Arma_R", "LKR_Arma_l", "LKR_Arma_r", "Lenker_Arma_li", "Lenker_Arma_re"],
        "Lenkergrundplatte": ["LKRGrPl_m", "LenkerGrPl", "LenkerGrPl_2", "LenkerGrPl_mi", "Lenker_Gr_Pl", "LenkerGrPl", "Lenkergrdpl"],
        "Motor": ["Motor", "Motor2"],
        "SAF-Slave": ["SAF"],
        "Scheinwerfer": ["SW_Ant_li", "SW_Ant_re", "SW_l", "SW_r", "SW_Anb_li", "SW_Anb_li_o", "SW_Anb_li_u", "SW_Anb_re", "SW_Anb_re_o", "SW_Anb_re_u", "SW_Antw_li", "SW_Antw_re", "SW_Geh_Ant_li", "SW_Geh_Ant_re", "SW_LED_Steuerg", "Scheinw_Anb_li", "Scheinw_Anb_re", "Scheinw_Geh_hi", "Scheinw_Geh_ob"],
        "Seitenstützenschalter": ["SSS"],
        "Sensorbox": ["Sensorbox", "Sensorbox_Anb", "Sensorbox_Ant", "Sensorbox_Integr", "Sensorbox_innen", "Sensorbox_l_A", "Sensorbox_r_A", "Sensorbox_Anb_al", "Sensorbox_Ant", "Sensorbox_Ant_ne", "Sensorbox_Integr", "Sensorbox_Steck", "Sensorbox_innen", "Sensorbox_li_Anb", "Sensorbox_r_A", "Sensorbox_re_Anb", "SB_Aufn_Fahrer_h", "SB_Aufn_Fahrer_v", "SB_Aufn_Sozius_h", "SB_Aufn_Sozius_v", "Sensorbox_Anb", "Sensorbox_Ant", "Sensorbox_Antw"],
        "Steuerkopf": ["Steuerkopf", "Steuerkopf ob", "Steuerkopf_o", "Steuerkopf_ob", "Steuerkopf_u", "Steuerkopf_un", "Steuerkopf_unt"],
        "SwiLa Links und Rechts": ["SchwiLa_L", "SchwiLa_R", "SchwiLa_l", "SchwiLa_r", "SchwingenL_li", "SchwingenL_re", "Schwingenlager_r", "SchwiLa_l", "SchwiLa_r", "Schwingenl_li", "Schwingenl_re", "Schwingenl_li", "Schwingenl_re"],
        "Seitenstützenschalter": ["Seitenst_Schalt"],
        "Tank": ["Tank_h_A", "Tankdeckel", "Tank_Anb_hi", "Tank_Anb_vo_li", "Tank_Anb_vo_re", "Tank_Anbind_hi", "Tank_Anb_vo_li", "Tank_Anb_vo_re", "Tank_Anbind_hi", "Tankdeckel"],
        "Zundlenkschloss": ["ZLS", "ZLS_A", "ZLS_r_A", "ZLS Anb", "ZLS_Anb", "ZLS_Ant_GrPl", "ZLS_Ant_Seite"]
    }
    return trans_tab