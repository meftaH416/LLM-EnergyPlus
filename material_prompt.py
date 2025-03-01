import re
import json

idf_text = """
Material,
    F06 EIFS finish,         !- Name
    Smooth,                  !- Roughness
    0.0095,                  !- Thickness {m}
    0.72,                    !- Conductivity {W/m-K}
    1856,                    !- Density {kg/m3}
    840;                     !- Specific Heat {J/kg-K}

  Material,
    F07 25mm stucco,         !- Name
    Smooth,                  !- Roughness
    0.0254,                  !- Thickness {m}
    0.72,                    !- Conductivity {W/m-K}
    1856,                    !- Density {kg/m3}
    840;                     !- Specific Heat {J/kg-K}

  Material,
    F08 Metal surface,       !- Name
    Smooth,                  !- Roughness
    0.0008,                  !- Thickness {m}
    45.28,                   !- Conductivity {W/m-K}
    7824,                    !- Density {kg/m3}
    500;                     !- Specific Heat {J/kg-K}

  Material,
    F09 Opaque spandrel glass,  !- Name
    Smooth,                  !- Roughness
    0.0064,                  !- Thickness {m}
    0.99,                    !- Conductivity {W/m-K}
    2528,                    !- Density {kg/m3}
    880;                     !- Specific Heat {J/kg-K}

  Material,
    F10 25mm stone,          !- Name
    MediumRough,             !- Roughness
    0.0254,                  !- Thickness {m}
    3.17,                    !- Conductivity {W/m-K}
    2560,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    F11 Wood siding,         !- Name
    MediumSmooth,            !- Roughness
    0.0127,                  !- Thickness {m}
    0.09,                    !- Conductivity {W/m-K}
    592,                     !- Density {kg/m3}
    1170;                    !- Specific Heat {J/kg-K}

  Material,
    F12 Asphalt shingles,    !- Name
    VeryRough,               !- Roughness
    0.0032,                  !- Thickness {m}
    0.04,                    !- Conductivity {W/m-K}
    1120,                    !- Density {kg/m3}
    1260;                    !- Specific Heat {J/kg-K}

  Material,
    F13 Built-up roofing,    !- Name
    Rough,                   !- Roughness
    0.0095,                  !- Thickness {m}
    0.16,                    !- Conductivity {W/m-K}
    1120,                    !- Density {kg/m3}
    1460;                    !- Specific Heat {J/kg-K}

  Material,
    F14 Slate or tile,       !- Name
    VeryRough,               !- Roughness
    0.0127,                  !- Thickness {m}
    1.59,                    !- Conductivity {W/m-K}
    1920,                    !- Density {kg/m3}
    1260;                    !- Specific Heat {J/kg-K}

  Material,
    F15 Wood shingles,       !- Name
    VeryRough,               !- Roughness
    0.0064,                  !- Thickness {m}
    0.04,                    !- Conductivity {W/m-K}
    592,                     !- Density {kg/m3}
    1300;                    !- Specific Heat {J/kg-K}

  Material,
    F16 Acoustic tile,       !- Name
    MediumSmooth,            !- Roughness
    0.0191,                  !- Thickness {m}
    0.06,                    !- Conductivity {W/m-K}
    368,                     !- Density {kg/m3}
    590;                     !- Specific Heat {J/kg-K}

  Material,
    F17 Carpet,              !- Name
    MediumRough,             !- Roughness
    0.0127,                  !- Thickness {m}
    0.06,                    !- Conductivity {W/m-K}
    288,                     !- Density {kg/m3}
    1380;                    !- Specific Heat {J/kg-K}

  Material,
    F18 Terrazzo,            !- Name
    Rough,                   !- Roughness
    0.0254,                  !- Thickness {m}
    1.8,                     !- Conductivity {W/m-K}
    2560,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    G01 16mm gypsum board,   !- Name
    MediumSmooth,            !- Roughness
    0.0159,                  !- Thickness {m}
    0.16,                    !- Conductivity {W/m-K}
    800,                     !- Density {kg/m3}
    1090;                    !- Specific Heat {J/kg-K}

  Material,
    G01a 19mm gypsum board,  !- Name
    MediumSmooth,            !- Roughness
    0.019,                   !- Thickness {m}
    0.16,                    !- Conductivity {W/m-K}
    800,                     !- Density {kg/m3}
    1090;                    !- Specific Heat {J/kg-K}

  Material,
    G02 16mm plywood,        !- Name
    Smooth,                  !- Roughness
    0.0159,                  !- Thickness {m}
    0.12,                    !- Conductivity {W/m-K}
    544,                     !- Density {kg/m3}
    1210;                    !- Specific Heat {J/kg-K}

  Material,
    G03 13mm fiberboard sheathing,  !- Name
    Smooth,                  !- Roughness
    0.0127,                  !- Thickness {m}
    0.07,                    !- Conductivity {W/m-K}
    400,                     !- Density {kg/m3}
    1300;                    !- Specific Heat {J/kg-K}

  Material,
    G04 13mm wood,           !- Name
    MediumSmooth,            !- Roughness
    0.0127,                  !- Thickness {m}
    0.15,                    !- Conductivity {W/m-K}
    608,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    G05 25mm wood,           !- Name
    MediumSmooth,            !- Roughness
    0.0254,                  !- Thickness {m}
    0.15,                    !- Conductivity {W/m-K}
    608,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    G06 50mm wood,           !- Name
    MediumSmooth,            !- Roughness
    0.0508,                  !- Thickness {m}
    0.15,                    !- Conductivity {W/m-K}
    608,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    G07 100mm wood,          !- Name
    MediumSmooth,            !- Roughness
    0.1016,                  !- Thickness {m}
    0.15,                    !- Conductivity {W/m-K}
    608,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    I01 25mm insulation board,  !- Name
    MediumRough,             !- Roughness
    0.0254,                  !- Thickness {m}
    0.03,                    !- Conductivity {W/m-K}
    43,                      !- Density {kg/m3}
    1210;                    !- Specific Heat {J/kg-K}

  Material,
    I02 50mm insulation board,  !- Name
    MediumRough,             !- Roughness
    0.0508,                  !- Thickness {m}
    0.03,                    !- Conductivity {W/m-K}
    43,                      !- Density {kg/m3}
    1210;                    !- Specific Heat {J/kg-K}

  Material,
    I03 75mm insulation board,  !- Name
    MediumRough,             !- Roughness
    0.0762,                  !- Thickness {m}
    0.03,                    !- Conductivity {W/m-K}
    43,                      !- Density {kg/m3}
    1210;                    !- Specific Heat {J/kg-K}

  Material,
    I04 89mm batt insulation,!- Name
    VeryRough,               !- Roughness
    0.0894,                  !- Thickness {m}
    0.05,                    !- Conductivity {W/m-K}
    19,                      !- Density {kg/m3}
    960;                     !- Specific Heat {J/kg-K}

  Material,
    I05 154mm batt insulation,  !- Name
    VeryRough,               !- Roughness
    0.1544,                  !- Thickness {m}
    0.05,                    !- Conductivity {W/m-K}
    19,                      !- Density {kg/m3}
    960;                     !- Specific Heat {J/kg-K}

  Material,
    I06 244mm batt insulation,  !- Name
    VeryRough,               !- Roughness
    0.2438,                  !- Thickness {m}
    0.05,                    !- Conductivity {W/m-K}
    19,                      !- Density {kg/m3}
    960;                     !- Specific Heat {J/kg-K}

  Material,
    M01 100mm brick,         !- Name
    MediumRough,             !- Roughness
    0.1016,                  !- Thickness {m}
    0.89,                    !- Conductivity {W/m-K}
    1920,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    M02 150mm lightweight concrete block,  !- Name
    MediumRough,             !- Roughness
    0.1524,                  !- Thickness {m}
    0.49,                    !- Conductivity {W/m-K}
    512,                     !- Density {kg/m3}
    880;                     !- Specific Heat {J/kg-K}

  Material,
    M03 200mm lightweight concrete block,  !- Name
    MediumRough,             !- Roughness
    0.2032,                  !- Thickness {m}
    0.5,                     !- Conductivity {W/m-K}
    464,                     !- Density {kg/m3}
    880;                     !- Specific Heat {J/kg-K}

  Material,
    M04 300mm lightweight concrete block,  !- Name
    MediumRough,             !- Roughness
    0.3048,                  !- Thickness {m}
    0.71,                    !- Conductivity {W/m-K}
    512,                     !- Density {kg/m3}
    880;                     !- Specific Heat {J/kg-K}

  Material,
    M05 200mm concrete block,!- Name
    MediumRough,             !- Roughness
    0.2032,                  !- Thickness {m}
    1.11,                    !- Conductivity {W/m-K}
    800,                     !- Density {kg/m3}
    920;                     !- Specific Heat {J/kg-K}

  Material,
    M06 300mm concrete block,!- Name
    MediumRough,             !- Roughness
    0.3048,                  !- Thickness {m}
    1.4,                     !- Conductivity {W/m-K}
    800,                     !- Density {kg/m3}
    920;                     !- Specific Heat {J/kg-K}

  Material,
    M07 150mm lightweight concrete block (filled),  !- Name
    MediumRough,             !- Roughness
    0.1524,                  !- Thickness {m}
    0.29,                    !- Conductivity {W/m-K}
    512,                     !- Density {kg/m3}
    880;                     !- Specific Heat {J/kg-K}

  Material,
    M08 200mm lightweight concrete block (filled),  !- Name
    MediumRough,             !- Roughness
    0.2032,                  !- Thickness {m}
    0.26,                    !- Conductivity {W/m-K}
    464,                     !- Density {kg/m3}
    880;                     !- Specific Heat {J/kg-K}

  Material,
    M09 300mm lightweight concrete block (filled),  !- Name
    MediumRough,             !- Roughness
    0.3048,                  !- Thickness {m}
    0.29,                    !- Conductivity {W/m-K}
    512,                     !- Density {kg/m3}
    880;                     !- Specific Heat {J/kg-K}

  Material,
    M10 200mm concrete block (filled),  !- Name
    MediumRough,             !- Roughness
    0.2032,                  !- Thickness {m}
    0.72,                    !- Conductivity {W/m-K}
    800,                     !- Density {kg/m3}
    920;                     !- Specific Heat {J/kg-K}

  Material,
    M11 100mm lightweight concrete,  !- Name
    MediumRough,             !- Roughness
    0.1016,                  !- Thickness {m}
    0.53,                    !- Conductivity {W/m-K}
    1280,                    !- Density {kg/m3}
    840;                     !- Specific Heat {J/kg-K}

  Material,
    M12 150mm lightweight concrete,  !- Name
    MediumRough,             !- Roughness
    0.1524,                  !- Thickness {m}
    0.53,                    !- Conductivity {W/m-K}
    1280,                    !- Density {kg/m3}
    840;                     !- Specific Heat {J/kg-K}

  Material,
    M13 200mm lightweight concrete,  !- Name
    MediumRough,             !- Roughness
    0.2032,                  !- Thickness {m}
    0.53,                    !- Conductivity {W/m-K}
    1280,                    !- Density {kg/m3}
    840;                     !- Specific Heat {J/kg-K}

  Material,
    M14a 100mm heavyweight concrete,  !- Name
    MediumRough,             !- Roughness
    0.1016,                  !- Thickness {m}
    1.95,                    !- Conductivity {W/m-K}
    2240,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    M17 50mm lightweight concrete roof ballast,  !- Name
    MediumRough,             !- Roughness
    0.0508,                  !- Thickness {m}
    0.19,                    !- Conductivity {W/m-K}
    640,                     !- Density {kg/m3}
    840;                     !- Specific Heat {J/kg-K}

Material,
    Asbestos-cement board - 3.2mm,  !- Name
    Smooth,                  !- Roughness
    0.0032,                  !- Thickness {m}
    0.58,                    !- Conductivity {W/m-K}
    1900,                    !- Density {kg/m3}
    1000;                    !- Specific Heat {J/kg-K}

  Material,
    Asbestos-cement board - 6.4mm,  !- Name
    Smooth,                  !- Roughness
    0.0064,                  !- Thickness {m}
    0.58,                    !- Conductivity {W/m-K}
    1900,                    !- Density {kg/m3}
    1000;                    !- Specific Heat {J/kg-K}

  Material,
    Gypsum or plaster board - 9.5mm,  !- Name
    MediumSmooth,            !- Roughness
    0.0095,                  !- Thickness {m}
    0.58,                    !- Conductivity {W/m-K}
    800,                     !- Density {kg/m3}
    1090;                    !- Specific Heat {J/kg-K}

  Material,
    Gypsum or plaster board - 2.7mm,  !- Name
    MediumSmooth,            !- Roughness
    0.0027,                  !- Thickness {m}
    0.58,                    !- Conductivity {W/m-K}
    800,                     !- Density {kg/m3}
    1090;                    !- Specific Heat {J/kg-K}

  Material,
    Gypsum or plaster board - 5.9mm,  !- Name
    MediumSmooth,            !- Roughness
    0.0059,                  !- Thickness {m}
    0.58,                    !- Conductivity {W/m-K}
    800,                     !- Density {kg/m3}
    1090;                    !- Specific Heat {J/kg-K}

  Material,
    Plywood (Douglas Fir) - 6.4mm,  !- Name
    MediumSmooth,            !- Roughness
    0.0064,                  !- Thickness {m}
    0.12,                    !- Conductivity {W/m-K}
    540,                     !- Density {kg/m3}
    1210;                    !- Specific Heat {J/kg-K}

  Material,
    Plywood (Douglas Fir) - 9.5mm,  !- Name
    Smooth,                  !- Roughness
    0.0095,                  !- Thickness {m}
    0.12,                    !- Conductivity {W/m-K}
    540,                     !- Density {kg/m3}
    1210;                    !- Specific Heat {J/kg-K}

  Material,
    Plywood or wood panels - 19.0mm,  !- Name
    Smooth,                  !- Roughness
    0.019,                   !- Thickness {m}
    0.12,                    !- Conductivity {W/m-K}
    540,                     !- Density {kg/m3}
    1210;                    !- Specific Heat {J/kg-K}

  Material,
    Sheathing - regular density - 12.7mm,  !- Name
    Smooth,                  !- Roughness
    0.0127,                  !- Thickness {m}
    0.055,                   !- Conductivity {W/m-K}
    290,                     !- Density {kg/m3}
    1300;                    !- Specific Heat {J/kg-K}

  Material,
    Nail-base sheathing - 12.7mm,  !- Name
    Smooth,                  !- Roughness
    0.0127,                  !- Thickness {m}
    0.057,                   !- Conductivity {W/m-K}
    400,                     !- Density {kg/m3}
    1300;                    !- Specific Heat {J/kg-K}

  Material,
    Shingle backer - 9.5mm,  !- Name
    Smooth,                  !- Roughness
    0.0095,                  !- Thickness {m}
    0.063,                   !- Conductivity {W/m-K}
    290,                     !- Density {kg/m3}
    1300;                    !- Specific Heat {J/kg-K}

  Material,
    Shingle backer - 7.9mm,  !- Name
    Smooth,                  !- Roughness
    0.0079,                  !- Thickness {m}
    0.063,                   !- Conductivity {W/m-K}
    290,                     !- Density {kg/m3}
    1300;                    !- Specific Heat {J/kg-K}

  Material,
    Sound deadening board,   !- Name
    Smooth,                  !- Roughness
    0.0127,                  !- Thickness {m}
    0.063,                   !- Conductivity {W/m-K}
    240,                     !- Density {kg/m3}
    1260;                    !- Specific Heat {J/kg-K}

  Material,
    Laminated paperboard,    !- Name
    MediumSmooth,            !- Roughness
    0.0032,                  !- Thickness {m}
    0.072,                   !- Conductivity {W/m-K}
    480,                     !- Density {kg/m3}
    1380;                    !- Specific Heat {J/kg-K}

  Material,
    Hardboard Medium density,!- Name
    Smooth,                  !- Roughness
    0.019,                   !- Thickness {m}
    0.105,                   !- Conductivity {W/m-K}
    800,                     !- Density {kg/m3}
    1300;                    !- Specific Heat {J/kg-K}

  Material,
    Particleboard Low density,  !- Name
    MediumSmooth,            !- Roughness
    0.019,                   !- Thickness {m}
    0.102,                   !- Conductivity {W/m-K}
    590,                     !- Density {kg/m3}
    1300;                    !- Specific Heat {J/kg-K}

  Material,
    Particleboard Medium density,  !- Name
    MediumSmooth,            !- Roughness
    0.019,                   !- Thickness {m}
    0.135,                   !- Conductivity {W/m-K}
    800,                     !- Density {kg/m3}
    1300;                    !- Specific Heat {J/kg-K}

  Material,
    Waferboard,              !- Name
    MediumSmooth,            !- Roughness
    0.019,                   !- Thickness {m}
    0.091,                   !- Conductivity {W/m-K}
    590,                     !- Density {kg/m3}
    1300;                    !- Specific Heat {J/kg-K}

  Material,
    Wood subfloor - 19mm,    !- Name
    MediumSmooth,            !- Roughness
    0.019,                   !- Thickness {m}
    0.115,                   !- Conductivity {W/m-K}
    800,                     !- Density {kg/m3}
    1380;                    !- Specific Heat {J/kg-K}

  Material,
    Insulation: Cellular glass - 25mm,  !- Name
    MediumRough,             !- Roughness
    0.025,                   !- Thickness {m}
    0.05,                    !- Conductivity {W/m-K}
    136,                     !- Density {kg/m3}
    750;                     !- Specific Heat {J/kg-K}

  Material,
    Insulation: Cellular glass - 50mm,  !- Name
    MediumRough,             !- Roughness
    0.05,                    !- Thickness {m}
    0.05,                    !- Conductivity {W/m-K}
    136,                     !- Density {kg/m3}
    750;                     !- Specific Heat {J/kg-K}

  Material,
    Insulation: Glass fiber - organic bonded - 25mm,  !- Name
    MediumRough,             !- Roughness
    0.025,                   !- Thickness {m}
    0.036,                   !- Conductivity {W/m-K}
    64,                      !- Density {kg/m3}
    960;                     !- Specific Heat {J/kg-K}

  Material,
    Insulation: Glass fiber - organic bonded - 50mm,  !- Name
    MediumRough,             !- Roughness
    0.05,                    !- Thickness {m}
    0.036,                   !- Conductivity {W/m-K}
    140,                     !- Density {kg/m3}
    960;                     !- Specific Heat {J/kg-K}

  Material,
    Insulation: Expanded perlite - organic bonded - 25mm,  !- Name
    MediumSmooth,            !- Roughness
    0.025,                   !- Thickness {m}
    0.052,                   !- Conductivity {W/m-K}
    16,                      !- Density {kg/m3}
    1260;                    !- Specific Heat {J/kg-K}

  Material,
    Insulation: Expanded rubber (rigid) - 25mm,  !- Name
    MediumRough,             !- Roughness
    0.025,                   !- Thickness {m}
    0.032,                   !- Conductivity {W/m-K}
    72,                      !- Density {kg/m3}
    1680;                    !- Specific Heat {J/kg-K}

  Material,
    Insulation: CFC-12 exp,  !- Name
    MediumSmooth,            !- Roughness
    0.025,                   !- Thickness {m}
    0.029,                   !- Conductivity {W/m-K}
    29,                      !- Density {kg/m3}
    1210;                    !- Specific Heat {J/kg-K}

  Material,
    Insulation:HCFC-142b exp,  !- Name
    MediumSmooth,            !- Roughness
    0.025,                   !- Thickness {m}
    0.029,                   !- Conductivity {W/m-K}
    29,                      !- Density {kg/m3}
    1210;                    !- Specific Heat {J/kg-K}

  Material,
    Insulation: Expanded polystyrene - molded beads - 32 kg/m3 density,  !- Name
    VeryRough,               !- Roughness
    0.025,                   !- Thickness {m}
    0.033,                   !- Conductivity {W/m-K}
    32,                      !- Density {kg/m3}
    1210;                    !- Specific Heat {J/kg-K}

  Material,
    Insulation: Cellular polyurethane/polyisocyanuratei (CFC11 exp.) (unfaced),  !- Name
    Rough,                   !- Roughness
    0.025,                   !- Thickness {m}
    0.0245,                  !- Conductivity {W/m-K}
    24,                      !- Density {kg/m3}
    1590;                    !- Specific Heat {J/kg-K}

  Material,
    Insulation: Cellular polyisocyanuratei (CFC-11 exp.) (gaspermeable facers),  !- Name
    Rough,                   !- Roughness
    0.025,                   !- Thickness {m}
    0.0245,                  !- Conductivity {W/m-K}
    32,                      !- Density {kg/m3}
    920;                     !- Specific Heat {J/kg-K}

  Material,
    Insulation: Cellular polyisocyanuratej (CFC-11 exp.) (gasimpermeable facers),  !- Name
    Rough,                   !- Roughness
    0.025,                   !- Thickness {m}
    0.02,                    !- Conductivity {W/m-K}
    32,                      !- Density {kg/m3}
    920;                     !- Specific Heat {J/kg-K}

  Material,
    Brick - fired clay - 2400 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    1.34,                    !- Conductivity {W/m-K}
    2400,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Brick - fired clay - 2240 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    1.185,                   !- Conductivity {W/m-K}
    2240,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Brick - fired clay - 2080 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    1.02,                    !- Conductivity {W/m-K}
    2080,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Brick - fired clay - 1920 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.895,                   !- Conductivity {W/m-K}
    1920,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Brick - fired clay - 1760 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.78,                    !- Conductivity {W/m-K}
    1760,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Brick - fired clay - 1600 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.675,                   !- Conductivity {W/m-K}
    1600,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Brick - fired clay - 1440 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.57,                    !- Conductivity {W/m-K}
    1440,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Brick - fired clay - 1280 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.48,                    !- Conductivity {W/m-K}
    1280,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Brick - fired clay - 1120 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.405,                   !- Conductivity {W/m-K}
    1120,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Quartzitic and sandstone - 2880 kg/m3 - 13mm,  !- Name
    MediumRough,             !- Roughness
    0.013,                   !- Thickness {m}
    10.4,                    !- Conductivity {W/m-K}
    2880,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Quartzitic and sandstone - 2560 kg/m3 - 13mm,  !- Name
    MediumRough,             !- Roughness
    0.013,                   !- Thickness {m}
    6.2,                     !- Conductivity {W/m-K}
    2560,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Quartzitic and sandstone - 2240 kg/m3 - 13mm,  !- Name
    MediumRough,             !- Roughness
    0.013,                   !- Thickness {m}
    3.5,                     !- Conductivity {W/m-K}
    2240,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Quartzitic and sandstone - 1920 kg/m3 - 13mm,  !- Name
    MediumRough,             !- Roughness
    0.013,                   !- Thickness {m}
    1.9,                     !- Conductivity {W/m-K}
    1920,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Calcitic - dolomitic - limestone - marble - and granite - 2880 kg/m3 - 13mm,  !- Name
    MediumRough,             !- Roughness
    0.013,                   !- Thickness {m}
    4.3,                     !- Conductivity {W/m-K}
    2880,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Calcitic - dolomitic - limestone - marble - and granite - 2560 kg/m3 - 13mm,  !- Name
    MediumRough,             !- Roughness
    0.013,                   !- Thickness {m}
    3.2,                     !- Conductivity {W/m-K}
    2560,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Calcitic - dolomitic - limestone - marble - and granite - 2240 kg/m3 - 13mm,  !- Name
    MediumRough,             !- Roughness
    0.013,                   !- Thickness {m}
    2.3,                     !- Conductivity {W/m-K}
    2240,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Calcitic - dolomitic - limestone - marble - and granite - 1920 kg/m3 - 13mm,  !- Name
    MediumRough,             !- Roughness
    0.013,                   !- Thickness {m}
    1.6,                     !- Conductivity {W/m-K}
    1920,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Calcitic - dolomitic - limestone - marble - and granite - 1600 kg/m3 - 13mm,  !- Name
    MediumRough,             !- Roughness
    0.013,                   !- Thickness {m}
    1.1,                     !- Conductivity {W/m-K}
    1600,                    !- Density {kg/m3}
    790;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Sand and gravel or stone aggregate concretes - 2400 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    2.15,                    !- Conductivity {W/m-K}
    2400,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Sand and gravel or stone aggregate concretes - 2240 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    1.95,                    !- Conductivity {W/m-K}
    2240,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Sand and gravel or stone aggregate concretes - 2080 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    1.45,                    !- Conductivity {W/m-K}
    2080,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Limestone concretes - 2240 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    1.6,                     !- Conductivity {W/m-K}
    2240,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Limestone concretes - 1920 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    1.14,                    !- Conductivity {W/m-K}
    1920,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Limestone concretes - 1600 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.79,                    !- Conductivity {W/m-K}
    1600,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Gypsum-fiber concrete (87.5% gypsum - 12.5% wood chips) - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.24,                    !- Conductivity {W/m-K}
    816,                     !- Density {kg/m3}
    880;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Cement/lime - mortar - and stucco - 1920 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    1.4,                     !- Conductivity {W/m-K}
    1920,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Cement/lime - mortar - and stucco - 1600 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.97,                    !- Conductivity {W/m-K}
    1600,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Cement/lime - mortar - and stucco - 1280 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.65,                    !- Conductivity {W/m-K}
    1280,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Expanded shale - clay - slate - expanded slags - cinders - pumice - 1920 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    1.1,                     !- Conductivity {W/m-K}
    1920,                    !- Density {kg/m3}
    840;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Expanded shale - clay - slate - expanded slags - cinders - pumice - 1600 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.785,                   !- Conductivity {W/m-K}
    1600,                    !- Density {kg/m3}
    840;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Expanded shale - clay - slate - expanded slags - cinders - pumice - 1280 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.535,                   !- Conductivity {W/m-K}
    1280,                    !- Density {kg/m3}
    840;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Expanded shale - clay - slate - expanded slags - cinders - pumice - 960 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.33,                    !- Conductivity {W/m-K}
    960,                     !- Density {kg/m3}
    840;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Expanded shale - clay - slate - expanded slags - cinders - pumice - 640 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.18,                    !- Conductivity {W/m-K}
    640,                     !- Density {kg/m3}
    840;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Perlite - vermiculite - and polystyrene beads - 800 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.265,                   !- Conductivity {W/m-K}
    800,                     !- Density {kg/m3}
    795;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Perlite - vermiculite - and polystyrene beads - 640 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.21,                    !- Conductivity {W/m-K}
    640,                     !- Density {kg/m3}
    795;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Perlite - vermiculite - and polystyrene beads - 480 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.16,                    !- Conductivity {W/m-K}
    480,                     !- Density {kg/m3}
    795;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Perlite - vermiculite - and polystyrene beads - 320 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.12,                    !- Conductivity {W/m-K}
    320,                     !- Density {kg/m3}
    795;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Foam concretes - 1920 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.75,                    !- Conductivity {W/m-K}
    1920,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Foam concretes - 1600 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.6,                     !- Conductivity {W/m-K}
    1600,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Foam concretes - 1280 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.44,                    !- Conductivity {W/m-K}
    1280,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Foam concretes - 1120 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.36,                    !- Conductivity {W/m-K}
    1120,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Foam concretes and cellular concretes - 960 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.3,                     !- Conductivity {W/m-K}
    960,                     !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Foam concretes and cellular concretes - 640 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.2,                     !- Conductivity {W/m-K}
    640,                     !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Foam concretes and cellular concretes - 320 kg/m3 - 51mm,  !- Name
    MediumRough,             !- Roughness
    0.051,                   !- Thickness {m}
    0.12,                    !- Conductivity {W/m-K}
    320,                     !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Sand and gravel or stone aggregate concretes - 2400 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    2.15,                    !- Conductivity {W/m-K}
    2400,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Sand and gravel or stone aggregate concretes - 2240 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    1.95,                    !- Conductivity {W/m-K}
    2240,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Sand and gravel or stone aggregate concretes - 2080 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    1.45,                    !- Conductivity {W/m-K}
    2080,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Limestone concretes - 2240 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    1.6,                     !- Conductivity {W/m-K}
    2240,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Limestone concretes - 1920 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    1.14,                    !- Conductivity {W/m-K}
    1920,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Limestone concretes - 1600 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.79,                    !- Conductivity {W/m-K}
    1600,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Gypsum-fiber concrete (87.5% gypsum - 12.5% wood chips) - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.24,                    !- Conductivity {W/m-K}
    816,                     !- Density {kg/m3}
    880;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Cement/lime - mortar - and stucco - 1920 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    1.4,                     !- Conductivity {W/m-K}
    1920,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Cement/lime - mortar - and stucco - 1600 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.97,                    !- Conductivity {W/m-K}
    1600,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Cement/lime - mortar - and stucco - 1280 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.65,                    !- Conductivity {W/m-K}
    1280,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Expanded shale - clay - slate - expanded slags - cinders - pumice - 1920 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    1.1,                     !- Conductivity {W/m-K}
    1920,                    !- Density {kg/m3}
    840;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Expanded shale - clay - slate - expanded slags - cinders - pumice - 1600 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.785,                   !- Conductivity {W/m-K}
    1600,                    !- Density {kg/m3}
    840;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Expanded shale - clay - slate - expanded slags - cinders - pumice - 1280 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.535,                   !- Conductivity {W/m-K}
    1280,                    !- Density {kg/m3}
    840;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Expanded shale - clay - slate - expanded slags - cinders - pumice - 960 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.33,                    !- Conductivity {W/m-K}
    960,                     !- Density {kg/m3}
    840;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Expanded shale - clay - slate - expanded slags - cinders - pumice - 640 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.18,                    !- Conductivity {W/m-K}
    640,                     !- Density {kg/m3}
    840;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Perlite - vermiculite - and polystyrene beads - 800 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.265,                   !- Conductivity {W/m-K}
    800,                     !- Density {kg/m3}
    795;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Perlite - vermiculite - and polystyrene beads - 640 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.21,                    !- Conductivity {W/m-K}
    640,                     !- Density {kg/m3}
    795;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Perlite - vermiculite - and polystyrene beads - 480 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.16,                    !- Conductivity {W/m-K}
    480,                     !- Density {kg/m3}
    795;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Perlite - vermiculite - and polystyrene beads - 320 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.12,                    !- Conductivity {W/m-K}
    320,                     !- Density {kg/m3}
    795;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Foam concretes - 1920 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.75,                    !- Conductivity {W/m-K}
    1920,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Foam concretes - 1600 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.6,                     !- Conductivity {W/m-K}
    1600,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Foam concretes - 1280 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.44,                    !- Conductivity {W/m-K}
    1280,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Foam concretes - 1120 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.36,                    !- Conductivity {W/m-K}
    1120,                    !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Foam concretes and cellular concretes - 960 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.3,                     !- Conductivity {W/m-K}
    960,                     !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Foam concretes and cellular concretes - 640 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.2,                     !- Conductivity {W/m-K}
    640,                     !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete: Foam concretes and cellular concretes - 320 kg/m3 - 102mm,  !- Name
    MediumRough,             !- Roughness
    0.102,                   !- Thickness {m}
    0.12,                    !- Conductivity {W/m-K}
    320,                     !- Density {kg/m3}
    900;                     !- Specific Heat {J/kg-K}

  Material,
    Hardwood - 12.9mm,       !- Name
    MediumSmooth,            !- Roughness
    0.0129,                  !- Thickness {m}
    0.167,                   !- Conductivity {W/m-K}
    680,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    Hardwood - 19mm,         !- Name
    MediumSmooth,            !- Roughness
    0.019,                   !- Thickness {m}
    0.167,                   !- Conductivity {W/m-K}
    680,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    Hardwood - 25mm,         !- Name
    MediumSmooth,            !- Roughness
    0.025,                   !- Thickness {m}
    0.167,                   !- Conductivity {W/m-K}
    680,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    Oak - 25mm,              !- Name
    MediumSmooth,            !- Roughness
    0.025,                   !- Thickness {m}
    0.17,                    !- Conductivity {W/m-K}
    704,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    Birch - 25mm,            !- Name
    MediumSmooth,            !- Roughness
    0.025,                   !- Thickness {m}
    0.172,                   !- Conductivity {W/m-K}
    704,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    Maple - 25mm,            !- Name
    MediumSmooth,            !- Roughness
    0.025,                   !- Thickness {m}
    0.164,                   !- Conductivity {W/m-K}
    671,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    Ash - 25mm,              !- Name
    MediumSmooth,            !- Roughness
    0.025,                   !- Thickness {m}
    0.159,                   !- Conductivity {W/m-K}
    642,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    Softwood - 12.9mm,       !- Name
    MediumSmooth,            !- Roughness
    0.0129,                  !- Thickness {m}
    0.129,                   !- Conductivity {W/m-K}
    496,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    Softwood - 19mm,         !- Name
    MediumSmooth,            !- Roughness
    0.019,                   !- Thickness {m}
    0.129,                   !- Conductivity {W/m-K}
    496,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    Softwood - 25mm,         !- Name
    MediumSmooth,            !- Roughness
    0.025,                   !- Thickness {m}
    0.129,                   !- Conductivity {W/m-K}
    496,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    Southern Pine - 25mm,    !- Name
    MediumSmooth,            !- Roughness
    0.025,                   !- Thickness {m}
    0.153,                   !- Conductivity {W/m-K}
    615,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    Douglas Fir-Larch - 25mm,!- Name
    MediumSmooth,            !- Roughness
    0.025,                   !- Thickness {m}
    0.141,                   !- Conductivity {W/m-K}
    559,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    Southern Cypress - 25mm, !- Name
    MediumSmooth,            !- Roughness
    0.025,                   !- Thickness {m}
    0.131,                   !- Conductivity {W/m-K}
    508,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    West Coast Woods - Cedars - 25mm,  !- Name
    MediumSmooth,            !- Roughness
    0.025,                   !- Thickness {m}
    0.114,                   !- Conductivity {W/m-K}
    425,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    California Redwood - 25mm,  !- Name
    MediumSmooth,            !- Roughness
    0.025,                   !- Thickness {m}
    0.113,                   !- Conductivity {W/m-K}
    420,                     !- Density {kg/m3}
    1630;                    !- Specific Heat {J/kg-K}

  Material,
    Concrete Block: Limestone Aggregrate: 200mm - 16.3 kg - 2 cores,  !- Name
    MediumRough,             !- Roughness
    0.2,                     !- Thickness {m}
    1.13,                    !- Conductivity {W/m-K}
    2210,                    !- Density {kg/m3}
    920;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete Block: Limestone Aggregrate: 200mm - 16.3 kg - 2 cores - perlite filled cores,  !- Name
    MediumRough,             !- Roughness
    0.2,                     !- Thickness {m}
    1.13,                    !- Conductivity {W/m-K}
    2210,                    !- Density {kg/m3}
    920;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete Block: Sand and Gravel Aggregrate: 15-16 kg - 2 or 3 cores,  !- Name
    MediumRough,             !- Roughness
    0.2,                     !- Thickness {m}
    1.13,                    !- Conductivity {W/m-K}
    2180,                    !- Density {kg/m3}
    920;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete Block: Sand and Gravel Aggregrate: 15-16 kg - 2 or 3 cores - perlite filled cores,  !- Name
    MediumRough,             !- Roughness
    0.2,                     !- Thickness {m}
    1.13,                    !- Conductivity {W/m-K}
    2180,                    !- Density {kg/m3}
    920;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete Block: Medium Mass Aggregate: 2 or 3 cores,  !- Name
    MediumRough,             !- Roughness
    0.3,                     !- Thickness {m}
    1.13,                    !- Conductivity {W/m-K}
    1790,                    !- Density {kg/m3}
    920;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete Block: Medium Mass Aggregate: 2 or 3 cores - perlite filled cores,  !- Name
    MediumRough,             !- Roughness
    0.3,                     !- Thickness {m}
    1.13,                    !- Conductivity {W/m-K}
    1790,                    !- Density {kg/m3}
    920;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete Block: Medium Mass Aggregate: 2 or 3 cores - molded EPS (beads) filled cores,  !- Name
    MediumRough,             !- Roughness
    0.3,                     !- Thickness {m}
    1.13,                    !- Conductivity {W/m-K}
    1790,                    !- Density {kg/m3}
    920;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete Block: Medium Mass Aggregate: 2 or 3 cores - molded EPS inserts in cores,  !- Name
    MediumRough,             !- Roughness
    0.3,                     !- Thickness {m}
    1.13,                    !- Conductivity {W/m-K}
    1790,                    !- Density {kg/m3}
    920;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete Block: Low Mass Aggregate: 7.3-7.7 kg - 2 or 3 cores,  !- Name
    MediumRough,             !- Roughness
    0.15,                    !- Thickness {m}
    0.33,                    !- Conductivity {W/m-K}
    1390,                    !- Density {kg/m3}
    880;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete Block: Low Mass Aggregate: 8.6-10.0 kg - UF foam filled cores,  !- Name
    MediumRough,             !- Roughness
    0.2,                     !- Thickness {m}
    0.33,                    !- Conductivity {W/m-K}
    1380,                    !- Density {kg/m3}
    880;                     !- Specific Heat {J/kg-K}

  Material,
    Concrete Block: Low Mass Aggregate: 8.6-10.0 kg - molded EPS inserts in cores,  !- Name
    MediumRough,             !- Roughness
    0.2,                     !- Thickness {m}
    0.33,                    !- Conductivity {W/m-K}
    1380,                    !- Density {kg/m3}
    880;                     !- Specific Heat {J/kg-K}

"""

# Split into blocks for each Material entry
materials = [block.strip() for block in idf_text.split("Material,") if block.strip()]

# Debug: Print extracted blocks
print("Extracted Blocks:", materials)

# Parse each block
material_datasets = []

for block in materials:
    lines = block.split("\n")
    name = lines[0].split(",")[0].strip()  # Extract material name
    roughness = lines[1].split(",")[0].strip()  # Extract roughness
    thickness = float(lines[2].split(",")[0].strip())  # Extract thickness
    conductivity = lines[3].split(",")[0].strip()
    density = lines[4].split(",")[0].strip()
    specific_heat = lines[5].split(";")[0].strip()

    # Convert thickness to mm
    thickness_mm = float(thickness * 1000)

    material_datasets.append({
        "user": f"Create an IDF entry for the material '{name}' with {thickness_mm} mm thickness.",
        "answer": f"Material,{name},{roughness},{thickness},{conductivity},{density},{specific_heat};"
    })




# Material:AirGap Data
idf_text_air = """
  Material:AirGap,
    F04 Wall air space resistance,  !- Name
    0.15;                    !- Thermal Resistance {m2-K/W}

  Material:AirGap,
    F05 Ceiling air space resistance,  !- Name
    0.18;                    !- Thermal Resistance {m2-K/W}

  Material:AirGap,
    F11 air space resistance,  !- Name
    0.10;                    !- Thermal Resistance {m2-K/W}

  Material:AirGap,
    Ceiling air space,  !- Name
    0.11;                    !- Thermal Resistance {m2-K/W}
"""

# Split into blocks for each Material:AirGap entry
air_gap_materials = [block.strip() for block in idf_text_air.split("Material:AirGap,") if block.strip()]

# Parse each block
air_gap_datasets = []

for block in air_gap_materials:
    lines = block.split("\n")
    name = lines[0].split(",")[0].strip()  # Extract material name
    resistance = lines[1].split(";")[0].strip()

    air_gap_datasets.append({
        "user": f"Create an air gap material '{name}' with {resistance} m2-K/W.",
        "answer": f"Material:AirGap,{name},{resistance};"
    })


# Material:NoMass Data
idf_text_nomass = """
  Material:NoMass,
    Siding: Asbestos-cement 6.4mm,  !- Name
    VeryRough,               !- Roughness
    0.037;                   !- Thermal Resistance {m2-K/W}

  Material:NoMass,
    Siding: Asphalt roll,    !- Name
    VeryRough,               !- Roughness
    0.026;                   !- Thermal Resistance {m2-K/W}

  Material:NoMass,
    Siding: Asphalt insulating,  !- Name
    VeryRough,               !- Roughness
    0.26;                    !- Thermal Resistance {m2-K/W}

  Material:NoMass,
    Siding: Hardboard 11mm,  !- Name
    MediumSmooth,            !- Roughness
    0.12;                    !- Thermal Resistance {m2-K/W}

  Material:NoMass,
    Siding: Wood - drop 20 by 200mm,  !- Name
    Rough,                   !- Roughness
    0.14;                    !- Thermal Resistance {m2-K/W}

  Material:NoMass,
    Siding: Wood - bevel 13 by 200mm - lapped,  !- Name
    Rough,                   !- Roughness
    0.14;                    !- Thermal Resistance {m2-K/W}

  Material:NoMass,
    Siding: Wood - bevel 19 by 250mm - lapped,  !- Name
    Rough,                   !- Roughness
    0.18;                    !- Thermal Resistance {m2-K/W}

  Material:NoMass,
    Siding: Wood - plywood 9.5mm - lapped,  !- Name
    Rough,                   !- Roughness
    0.1;                     !- Thermal Resistance {m2-K/W}

  Material:NoMass,
    Siding: Hollow-backed,   !- Name
    Smooth,                  !- Roughness
    0.11;                    !- Thermal Resistance {m2-K/W}

  Material:NoMass,
    Siding: Insulating-board backed 9.5mm nominal,  !- Name
    Smooth,                  !- Roughness
    0.32;                    !- Thermal Resistance {m2-K/W}

  Material:NoMass,
    Siding: Insulating-board backed 9.5mm nominal - foil backed,  !- Name
    Smooth,                  !- Roughness
    0.52;                    !- Thermal Resistance {m2-K/W}

  Material:NoMass,
    Siding: Architectural (soda-lime float) glass,  !- Name
    Smooth,                  !- Roughness
    0.018;                   !- Thermal Resistance {m2-K/W}
"""

# Split into blocks for each Material:NoMass entry
no_mass_materials = [block.strip() for block in idf_text_nomass.split("Material:NoMass,") if block.strip()]

# Parse each block
no_mass_datasets = []

for block in no_mass_materials:
    lines = block.split("\n")
    name = lines[0].split(",")[0].strip()  # Extract material name
    roughness = lines[1].split(",")[0].strip()  # Extract roughness
    resistance = lines[2].split(";")[0].strip()

    no_mass_datasets.append({
        "user": f"Create a NoMass material '{name}' with {resistance} m2-K/W.",
        "answer": f"Material:NoMass,{name},{roughness},{resistance};"
    })


# Combine both datasets
all_material_datasets = material_datasets + air_gap_datasets + no_mass_datasets

# Save dataset to JSON file
with open("material_datasets.json", "w") as f:
    json.dump(all_material_datasets, f, indent=2)

# Print output for verification
print(json.dumps(all_material_datasets, indent=2))
