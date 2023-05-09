# Data Processing

Just ignore all the files except the ones I mention here.

- `plans/[0-3].jpg` - Images of the floor plans. Note that 0 corresponds to the basement.
- `plans/[0-3]_cleaned.jpg` - Removed most of the text from the floor plans.
- `locs.json` - Locations in `{"name": (pixel_x, pixel_y)}` format.
- `connections.json` - List of connections for each location. Format is `{"loc0": ["loc1", "loc2", "loc3"]}`.