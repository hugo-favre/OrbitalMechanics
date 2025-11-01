from src.display.earth_satellite_display import orbit_display
from src.display.two_body_display import twobody_display
from src.analysis.orbit_analysis import orbit_analysis
from src.tools.readfile import read_input_file

def main():
    filename = "data/inputs/Molniya.txt"
    params = read_input_file(filename)

    mode = params['mode']
    perturbations = params['perturbations'] # Useless for now
    for m in mode:
        if m == 'orbit_display':
            orbit_display(params)
        if m == 'orbit_analysis':
            orbit_analysis(params)
        if m == 'two_body_display':
            twobody_display(params)

if __name__ == "__main__":
    main()