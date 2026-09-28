import argparse
import json
import sys
import xarray as xr
from tocatalogs.stac.xarray_dataset_to_stac_item import xarray_dataset_to_stac_item

def main():
    parser = argparse.ArgumentParser(description="Generate a STAC item from an xarray dataset.")
    parser.add_argument("input", help="Path to the input xarray dataset (e.g., a Zarr store or NetCDF file).")
    parser.add_argument("--engine", default="zarr", choices=["zarr", "kerchunk", "h5netcdf", "h5py", "netcdf4"], help="Engine for the input dataset (default: zarr).")
    parser.add_argument("--output", help="Path to save the generated STAC item JSON. If not provided, prints to stdout.")
    parser.add_argument("--geoparquet", help="Path to save the STAC item as a GeoParquet file.")
    parser.add_argument("--item-id", help="Explicit ID for the STAC item.")
    parser.add_argument("--collection-id", help="Collection ID for the STAC item.")
    parser.add_argument("--exp-license", help="SPDX license ID for the experiment.")
    parser.add_argument("--title", help="Title for the STAC item.")
    parser.add_argument("--asset-access", default="dkrz-disk", help="Name of the primary data asset (default: dkrz-disk).")
    parser.add_argument("--l-eeriecloud", action="store_true", help="If also available via eerie.cloud specific features.")
    parser.add_argument("--l-cubeextension", action="store_true", help="Enable cube: extension (default: True).")
    parser.add_argument("--l-gridlook", action="store_true", help="Enable gridlook asset (default: True).")

    args = parser.parse_args()

    try:
        # Load the dataset
        if args.engine in ["zarr", "kerchunk", "h5netcdf", "h5py", "netcdf4"]:
            ds = xr.open_dataset(args.input, engine=args.engine)
        else:
            raise ValueError(f"Unsupported engine: {args.engine}")

        # Generate the STAC item
        item = xarray_dataset_to_stac_item(
            ds=ds,
            ds_format=args.engine,
            item_id=args.item_id,
            collection_id=args.collection_id,
            exp_license=args.exp_license,
            title=args.title,
            asset_access=args.asset_access,
            l_eeriecloud=args.l_eeriecloud,
            l_cubeextension=args.l_cubeextension,
            l_gridlook=args.l_gridlook
        )

        # Convert to dict
        item_dict = item.to_dict()

        # Output the result
        if args.geoparquet:
            import os
            import pandas as pd
            import geopandas as gpd
            from shapely.geometry import shape

            # Convert STAC item to a single-row GeoDataFrame
            geom = shape(item_dict["geometry"])
            properties = item_dict["properties"]
            properties["id"] = item_dict["id"]

            gdf = gpd.GeoDataFrame([properties], geometry=[geom])

            if os.path.exists(args.geoparquet):
                existing_gdf = gpd.read_parquet(args.geoparquet)
                gdf = pd.concat([existing_gdf, gdf], ignore_index=True)

            gdf.to_parquet(args.geoparquet)
            print(f"STAC item added to GeoParquet file: {args.geoparquet}")

        if args.output:
            with open(args.output, "w") as f:
                json.dump(item_dict, f, indent=2)
            print(f"STAC item saved to {args.output}")
        else:
            print(json.dumps(item_dict, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
