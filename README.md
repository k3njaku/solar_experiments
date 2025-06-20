# solar_experiments

Objective:

Scrape and compile a clean, deduplicated dataset containing all addresses with solar panels installed specifically on buildings (residential and commercial) in the North Holland province of the Netherlands, structured with specific data fields.

Required Data Fields (each in separate columns):

Objectnummer

Street

Housenumber (include additional house number letters if applicable, e.g., "10HS")

Postal code (formatted as 4 digits followed by 2 letters, e.g., "1000 AA")

City

Country ("Netherlands")

Gebruiksdoel

Functie

Company name (if the address is a business, otherwise leave blank)

Google Maps URL (must accurately pinpoint the exact building location)

Longitude (LNG)

Latitude (LAT)

Dataset Specifications:

Scope: Addresses specifically from North Holland province initially, later extendable to the entire Netherlands.

Accuracy Target: Minimum 95% accuracy, ensuring minimal false detections or misalignments.

Duplicates: Completely remove duplicate entries.

Data validation: Confirm and verify the accuracy and correctness of addresses, postal codes, and geocoordinates through street view or high-resolution imagery.

Suggested Workflow:

Initial Scrape:

Extract solar panel locations from sources such as OpenStreetMap via Overpass API.

Enrichment:

Use official Netherlands BAG datasets (bag.gpkg) to add missing data fields like Gebruiksdoel, Functie, and potentially Company Name.

Intersect solar panel points with building footprints to ensure accuracy.

Data Validation & Cleaning:

Validate data points against Google Maps street view or satellite imagery.

Correct postal codes and format consistently.

Identify and remove non-building solar panel installations.

Output Format:

Provide clean CSV files structured exactly as specified above, ensuring all columns are accurately filled.

Clearly labeled headers and consistent formatting across all files.

Delivery:

Data should initially be delivered incrementally, city by city within North Holland, followed by complete North Holland province, and eventually the entire Netherlands.

Organize all output files within one clearly labeled folder for ease of access and further enrichment or analysis.

## Quickstart

This repository includes a basic Python script to fetch solar panel locations from the Overpass API and join them with your local BAG dataset.

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Download BAG data**
   Obtain the official `bag.gpkg` from the Dutch Kadaster and store it locally. The file is too large to include in the repository, so provide the path when running the script.

3. **Run the script**
   ```bash
   python scripts/overpass_to_csv.py --bag_path /path/to/bag.gpkg --output north_holland.csv
   ```
   This will download solar panel features from OpenStreetMap, intersect them with buildings from BAG, and output a CSV with the required columns.

The script is a starting point and can be extended to split results per city or to perform additional validation.
