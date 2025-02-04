import json
import random

# Define parameters for variation
energyplus_versions = ["22.0", "22.4", "23.0", "23.2", "23.4", "24.0"]
cities = {
    "New York": ("40.71,-74.01,-5.00,10.00", "725030"),
    "Chicago": ("41.88,-87.63,-6.00,15.00", "725300"),
    "Los Angeles": ("34.05,-118.25,-8.00,100.00", "722950"),
    "Houston": ("29.76,-95.36,-6.00,10.00", "722430"),
    "Miami": ("25.76,-80.29,-5.00,10.00", "722020"),
    "San Francisco": ("37.77,-122.42,-7.00,10.00", "724943"),
    "Seattle": ("47.45,-122.31,-7.00,100.00", "726060"),
    "Phoenix": ("33.45,-112.07,-7.00,350.00", "722780"),
    "Denver": ("39.72,-104.75,-7.00,1726.00", "724695"),
    "Boston": ("42.36,-71.06,-5.00,15.00", "725090")
}
building_types = ["SmallOffice", "MediumOffice", "LargeOffice", "Warehouse", "Retail", "Hotel"]
timestep_values = [6, 8, 10, 12]
heat_balance_algorithms = ["ConductionTransferFunction", "MoisturePenetrationDepthConductionTransferFunction"]
surface_convection_algorithms = ["TARP", "DoE2"]
design_day_conditions = ["ASHRAEClearSky", "ASHRAETau"]

# Different question formats
question_templates = [
    "Can you generate an IDF template for EnergyPlus version {version} in {city}?",
    "I need an IDF setup for {city} using EnergyPlus {version}.",
    "Provide a basic IDF template for {city} for EnergyPlus version {version}.",
    "Give me an EnergyPlus {version} IDF file for {city}.",
    "How do I set up an IDF for EnergyPlus {version} for {city}?",
    "Can you create an IDF model for {city} using EnergyPlus {version}?",
    "What is a good IDF template for EnergyPlus {version} in {city}?",
    "Help me with an IDF configuration for {city} running on EnergyPlus {version}.",
    "Generate an IDF setup optimized for {city} in EnergyPlus {version}.",
]

# Generate synthetic dataset
dataset = []
num_samples = 500  # Adjust as needed

for _ in range(num_samples):
    city, (coords, wmo) = random.choice(list(cities.items()))
    version = random.choice(energyplus_versions)
    building = random.choice(building_types)
    timestep = random.choice(timestep_values)
    heat_balance = random.choice(heat_balance_algorithms)
    surf_inside = random.choice(surface_convection_algorithms)
    surf_outside = random.choice(surface_convection_algorithms)
    design_day = random.choice(design_day_conditions)

    # Pick a random question format
    user_question = random.choice(question_templates).format(version=version, city=city)

    entry = {
        "user": user_question,
        "assistant": [
            f"Version,{version};",
            f"Timestep,{timestep};",
            "SimulationControl,Yes, Yes, Yes, No, Yes, No, 1;",
            "Sizing:Parameters, 1.0, 1.0, 1;",
            f"Building,{building},0.0000,Various,0.0400,0.2000,FullInteriorAndExterior,25, 6;",
            "ShadowCalculation,PolygonClipping,Periodic,30,200;",
            f"SurfaceConvectionAlgorithm:Inside,{surf_inside};",
            f"SurfaceConvectionAlgorithm:Outside,{surf_outside};",
            f"HeatBalanceAlgorithm,{heat_balance},200.0000;",
            "GlobalGeometryRules,UpperLeftCorner,Counterclockwise,Relative,Relative;",
            f"Site:Location, {city}_USA WMO={wmo},{coords};",
            "SizingPeriod:DesignDay, City Ann Htg 99.6% Condns DB,",
            "12, 21, WinterDesignDay, -5.0, 0.0, DefaultMultipliers, , Wetbulb, -5.0, , , , ,",
            "101325., 3.2, 180, No, No, No, ASHRAEClearSky, , , , , 0.00;",
            "SizingPeriod:DesignDay, City Ann Clg .4% Condns DB=>MWB,",
            "7, 21, SummerDesignDay, 35.0, 22.5, DefaultMultipliers, , Wetbulb, 23.0, , , , ,",
            "101325., 4.0, 240, No, No, No, ASHRAETau, , , 0.500, 2.200;",
            "RunPeriod, RUNPERIOD 1, 1, 1, , 12, 31, , Wednesday, No, No, No, Yes, Yes;",
            "ScheduleTypeLimits ,Any Number;",
            "ScheduleTypeLimits ,Fraction , 0.0 , 1.0 ,CONTINUOUS;",
            "ScheduleTypeLimits ,Temperature ,-60,200,CONTINUOUS;",
            "ScheduleTypeLimits ,Control Type ,0,4,DISCRETE;",
            "ScheduleTypeLimits ,On/Off,0,1,DISCRETE;"
        ]
    }
    
    dataset.append(entry)

# Save dataset to JSON file
with open("idf_dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)

print(f"✅ Dataset generated with {num_samples} examples and saved as 'idf_dataset.json'")
