"""
Create project configuration files.

Copies configuration templates to configuration folder for custom modification.
"""

import os
import shutil
import sys

source_folder = './configuration/templates'
dest_folder = './configuration'
region_names = [
    x.split('.yml')[0]
    for x in os.listdir('./configuration/regions')
    if x.endswith('.yml')
]

region_template = """
name: Full study region name, e.g. Las Palmas de Gran Canaria
year: Target year for analysis, e.g. 2023
country: Fully country name, e.g. España
country_code: Two character country code (ISO3166 Alpha-2 code), e.g. ES
continent: Continent name, e.g. Europe
crs:
  name: name of the coordinate reference system (CRS), e.g. REGCAN95 / LAEA Europe
  standard: acronym of the standard catalogue defining this CRS, eg. EPSG
  srid: spatial reference identifier (SRID) integer that identifies this CRS according to the specified standard, e.g. 5635 (see https://spatialreference.org/, or search for what is commonly used in your city or country; e.g. a national CRS like those listed at https://en.wikipedia.org/wiki/List_of_national_coordinate_reference_systems )
  utm: UTM grid if EPSG code is not known (used to manually derive EPSG code= 326** is for Northern Hemisphere, 327** is for Southern Hemisphere), e.g. 28N (see https://mangomap.com/robertyoung/maps/69585/what-utm-zone-am-i-in- )
study_region_boundary:
  data: Region boundary data (path relative to project directory, or GHS:variable='value'), e.g. "region_boundaries/Example/Las Palmas de Gran Canaria - Centro Nacional de Información Geográfica - WGS84 - EPSG4326.geojson"
  source: The name of the provider of this data, e.g. Centro Nacional de Información Geográfica
  publication_date: Publication date for study region area data source, or date of currency, e.g. 2019-02-01
  url: URL for the source dataset, or its provider, e.g. https://datos.gob.es/en/catalogo/e00125901-spaignllm
  licence: Licence for the data, e.g. CC-BY-4.0
  licence_url: URL for the data licence, e.g. https://www.ign.es/resources/licencia/Condiciones_licenciaUso_IGN.pdf
  ghsl_urban_intersection: Whether the provided study region boundary will be further restricted to an urban area defined by its intersection with a linked urban region dataset (see urban_region), e.g. true
population: the population record in datasets.yml to be used for this region, e.g. example_las_palmas_pop_2022
OpenStreetMap: the OpenStreetMap record defined in datasets.yml to be used for this region, e.g. las_palmas_20230221
network:
  osmnx_retain_all: If false, only retain main connected network when retrieving OSM roads, e.g. false
  buffered_region: Recommended to set to 'true'.  If false, use the study region boundary without buffering for network extraction (this may appropriate for true islands, but could be problematic for anywhere else where the network and associated amenities may be accessible beyond the edge of the study region boundary).
  polygon_iteration: Iterate over and combine polygons (this may be appropriate for a series of islands), e.g. false
  connection_threshold: Minimum distance to retain (a useful parameter for islands, like Hong Kong, but for most purposes you can leave this blank)
  intersection_tolerance: Tolerance in metres for cleaning intersections.  This is an important methodological choice, and the chosen parameter should be robust to a variety of network topologies in the city being studied.  See https://github.com/gboeing/osmnx-examples/blob/main/notebooks/04-simplify-graph-consolidate-nodes.ipynb. For example: 12
urban_region: the urban region dataset defined in datasets.yml to be optionally used for this region (such as data from the Global Human Settlements Layer Urban Centres Database, GHSL-UCDB), e.g. GHS-Example-Las-Palmas
urban_query: GHS or other linkage of covariate data (GHS:variable='value', or path:variable='value' for a dataset with equivalently named fields defined in project parameters for air_pollution_covariates), e.g. GHS:UC_NM_MN=='Las Palmas de Gran Canaria' and CTR_MN_NM=='Spain'
country_gdp:
  classification: Country GDP classification, e.g. lower-middle
  reference: Citation for the GDP classification, e.g. The World Bank. 2020. World Bank country and lending groups. https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups
covariate_data: additional covariates to be linked (currently this is designed to direct the process to retrieve additional city statistics from the GHSL UCDB entry for the city, where available), e.g. urban_query
custom_destinations: Details of custom destinations to use (e.g. as done for Maiduguri, Nigeria), in addition to those from OSM (optional, as required; else, leave blank) file name (located in study region folder), category plain name field, category full name field, Y coordinate, X coordinate, EPSG number, attribution
gtfs_feeds: Details for city specific parent folder (within GTFS data dir defined in config.yml) and feed-specific unzipped sub-folders containing GTFS feed data.  For each feed, the data provider, year, start and end dates to use, and mapping of modes are specified (only required if feed does not conform to the GTFS specification https://developers.google.com/transit/gtfs/reference). For cities with no GTFS feeds identified, this may be left blank.  Otherwise, copy the example in the example_ES_Las_Palmas_2023.yml file or other example files where multiple GTFS feeds for different modes have been defined to get started and customise this for your city.
policy_review: Optional path to results of policy indicator review for inclusion in generated reports
notes: Notes for this region
"""

print(
    'Creating project configuration files, if not already existing in the configuration folder...',
)
try:
    for folder, subfolders, files in os.walk(source_folder):
        for file in files:
            path_file = os.path.join(folder, file)
            if os.path.exists(f'{dest_folder}/{file}'):
                print(f'\t- {file} exists.')
            else:
                shutil.copyfile(path_file, path_file.replace('templates/', ''))
                print(f'\t- created {file}')
except Exception as e:
    raise Exception(f'An error occurred: {e}')

if len(sys.argv) >= 2:
    codename = sys.argv[1]
    if os.path.exists(f'./configuration/regions/{codename}.yml'):
        print(
            f"\nConfiguration file for the specified study region codename '{codename}' already exists: \nconfiguration/regions/{codename}.yml.\n\nPlease open and edit this file in a text editor following the provided example directions in order to complete configuration for your study region.  A completed example study region configuration can be viewed in the file 'configuration/regions/example_ES_Las_Palmas_2023.yml'.\n\nTo view additional guidance on configuration, run this script again without a codename. Once configuration has been completed, to proceed to analysis for this city, enter:\npython 2_analyse_region.py {codename}\n",
        )
    else:
        with open(f'./configuration/regions/{codename}.yml', 'w') as f:
            f.write(region_template)
        print(
            f"\nNew region configuration file has been initialised using the codename, '{codename}', in the folder:\nconfiguration/regions/{codename}.yml\n\nPlease open and edit this file in a text editor following the provided example directions in order to complete configuration for your study region.  A completed example study region configuration can be viewed in the file 'configuration/regions/example_ES_Las_Palmas_2023.yml'.\n\nTo view additional guidance on configuration, run this script again without a codename.\n",
        )
else:
    print(
        f"""
Before commencing analysis, your study regions will need to be configured.

Study regions are configured using .yml files located within the `configuration/regions` sub-folder. An example configuration for Las Palmas de Gran Canaria (for which data supporting analysis is included) has been provided in the file `process/configuration/regions/example_ES_Las_Palmas_2023.yml`, and further additional example regions have also been provided.  The name of the file, for example `example_ES_Las_Palmas_2023`, acts a codename for the city when used in processing and avoids issues with ambiguity when analysing multiple cities across different regions and time points: 'example' clarifies that this is an example, 'ES' clarifies that this is a Spanish city, 'Las_Palmas' is a common short way of writing the city's name, and the analysis uses data chosen to target 2023.  Using a naming convention like this is recommended when creating new region configuration files (e.g. ES_Barcelona_2023.yml, or AU_Melbourne_2023.yml).

The study region configuration files have a file extension .yml (YAML files), which means they are text files that can be edited in a text editor to define region specific details, including which datasets used - eg cities from a particular region could share common excerpts of population and OpenStreetMap, potentially).

Additional configuration may be required to define datasets referenced for regions, configuration of language for reporting using the following files:

datasets.yml: Configuration of datasets, which may be referenced by study regions of interest

_report_configuration.xlsx: (required to generate reports) Use to configure generation of images and reports generated for processed cities; in particular, the translation of prose and executive summaries for different languages.  This can be edited in a spreadsheet program like Microsoft Excel.

config.yml: (optional) Configuration of overall project, including your time zone for logging start and end times of analyses

Optional configuration of other parameters is also possible.  Please visit our tool's website for further guidance on how to use this tool:
https://global-healthy-liveable-cities.github.io/

Currently configured study regions : {', '.join(region_names)}

To initialise a new study region configuration file, you can run this script again providing your choice of codename, for example:

python 1_create_project_configuration_files.py example_ES_Las_Palmas_2023
""",
    )
