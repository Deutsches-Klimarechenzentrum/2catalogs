#!/usr/bin/env python
# coding: utf-8

"""
CLI tool to convert Zarr stores, reference:: Parquet inputs,
and Intake v1 YAML catalogs into Intake v2 catalogs.
"""

from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path

import fsspec
import intake
import yaml
from intake.readers.datatypes import Zarr as Zarrtype
from intake.readers.datatypes import HDF5 as HDF5type
#from intake.readers.datatypes import YAMLFile
from intake.readers.readers import PandasParquet, XArrayDatasetReader, YAMLCatalogReader
from tqdm import tqdm


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logger = logging.getLogger("tointake2")


def setup_logging(level=logging.INFO):
    """Configure root logging for the CLI."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


# -----------------------------------------------------------------------------
# Input classification helpers
# -----------------------------------------------------------------------------

NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def is_reference(inp: str) -> bool:
    """Return True if input is a reference:: URI."""
    return inp.startswith("reference::")


def is_valid_input(arg: str) -> bool:
    """
    Check whether an argument is a valid input source.

    Valid inputs are:
    - reference:: URIs
    - existing filesystem paths
    """
    if is_reference(arg):
        return True

    return Path(arg).exists()


def parse_inputname(inp: str) -> tuple[str | None, str]:
    """
    Parse optional dataset name from CLI argument.

    Accepts inputs of the form:
        name=path

    Returns
    -------
    (name, path)
        name is None if no explicit name was provided
    """
    inpname = None
    inppath = inp

    if inp.count("=") == 1:
        name, path = inp.split("=", 1)
        if NAME_RE.match(name):
            inpname = name
            inppath = path

    return inpname, inppath


# -----------------------------------------------------------------------------
# Handlers
# -----------------------------------------------------------------------------

def handle_reference(
    entryname: str,
    inp: list[str],
    outcat: intake.entry.Catalog,
    storage_options: dict,
):
    """
    Add reference:: Parquet inputs as PandasParquet readers.

    Each reference target is added as a separate catalog entry.
    """
    logger.info("Adding reference parquet inputs for entry '%s'", entryname)

    storage_options["lazy"] = True
    storage_options["consolidated"] = False
    rp = storage_options.get("remote_protocol")
    if rp:
        rp = rp.split(':')[0]
        if rp.startswith("http"):
            storage_options["remote_options"] = dict(asynchronous=True)
            #storage_options["asynchronous"]=True

    else:
        storage_options["remote_protocol"]="file"
    
    parquet_dirs = [
        ":".join(a.split(":")[2:]).replace("//", "/") for a in inp
    ]

    readers = [
        PandasParquet(path, engine="fastparquet")
        for path in parquet_dirs
    ]

    for idx, reader in enumerate(readers):
        key = f"{entryname}_parquet_{idx}"
        outcat[key] = reader
        logger.debug("Added parquet reader '%s'", key)

    return outcat

def add_catalog_dir(outcat, inp):
    oldcat_parent = Path(inp).parent.resolve().as_posix() + "/"
    outcat.user_parameters["CATALOG_DIR"] = intake.readers.user_parameters.SimpleUserParameter(
         default=oldcat_parent, dtype=str
    )
    return outcat

def clean_braces(obj):
    if isinstance(obj, str):
        return obj.replace("{{", "{").replace("}}", "}")
    
    if isinstance(obj, dict):
        return {k: clean_braces(v) for k, v in obj.items()}
    
    if isinstance(obj, list):
        return [clean_braces(v) for v in obj]
    
    return obj  # leave other types unchanged

def update_metadata(reader, entryname, md=None):
    # Populate metadata from dataset attributes
    read = None
    try:
        read = reader.read()
    except:
        logger.debug(f"Could not load '{entryname}'")
    
    if read:
        reader.metadata=read.attrs.copy()

    if md:
        reader.metadata.update(md)


def handle_netcdf_input(
    entryname: str,
    inp: str | list[str],
    outcat: intake.entry.Catalog,
    chunks: str = "auto",
    md: dict | None = None,
    pms: dict | None = None,
    so: dict | None = None
):
    """
    Add a Zarr (or reference-backed Zarr) input to the catalog.
    """
    if isinstance(inp, str):
        inp = [inp]
    
    logger.info("Adding NetCDF input '%s'", entryname)

    storage_options: dict = so if so is not None else {}
    
    data = HDF5type(inp, storage_options=storage_options)

    if pms:
        logger.info("Cannot handle parameter yet")
        #uplists = [pm_dict["allowed"] for up in pms]
        #upproduct = list(itertools.product(*uplists))
        #up_combs = [{ups[i]["name"]: comb[i] for i in range(len(pms))} for comb in upproduct]
        #for pm_name,pm_dict in pms.items():

            #options = {x: x for x in pm_dict["allowed"]}
            #outcat.user_parameters[pm_name] = intake.readers.user_parameters.OptionsUserParameter(
            #    options, default=pm_dict["default"], dtype=str, description=pm_dict.get("description", "NaN")
            #)        

    reader = XArrayDatasetReader(
        data,
        chunks=chunks
    )

    update_metadata(reader, entryname, md=md)
    
    outcat[entryname] = reader
    logger.debug("Added Netcdf reader '%s'", entryname)

    return outcat

def handle_zarr_input(
    entryname: str,
    inp: str | list[str],
    outcat: intake.entry.Catalog,
    chunks: str = "auto",
    md: dict | None = None,
    pms: dict | None = None,
    so: dict | None = None
):
    """
    Add a Zarr (or reference-backed Zarr) input to the catalog.
    """
    if isinstance(inp, str):
        inp = [inp]
    
    logger.info("Adding Zarr input '%s'", entryname)

    storage_options: dict = so if so is not None else {}

    if any(is_reference(a) for a in inp):
        if not all(is_reference(a) for a in inp):
            raise ValueError("Mixed reference and non-reference inputs found")

        handle_reference(
            entryname=entryname,
            inp=inp,
            outcat=outcat,
            storage_options=storage_options,
        )

    data = Zarrtype(inp, storage_options=storage_options)
    
    if pms:
        logger.info("Cannot handle parameter yet")
        #uplists = [pm_dict["allowed"] for up in pms]
        #upproduct = list(itertools.product(*uplists))
        #up_combs = [{ups[i]["name"]: comb[i] for i in range(len(pms))} for comb in upproduct]
        #for pm_name,pm_dict in pms.items():

            #options = {x: x for x in pm_dict["allowed"]}
            #outcat.user_parameters[pm_name] = intake.readers.user_parameters.OptionsUserParameter(
            #    options, default=pm_dict["default"], dtype=str, description=pm_dict.get("description", "NaN")
            #)        


    zarr_format = 2 if any("::" in a for a in inp) else None

    reader = XArrayDatasetReader(
        data,
        chunks=chunks,
        zarr_format=zarr_format,
    )

    # Populate metadata from dataset attributes
    update_metadata(reader, entryname, md=md)
        
    outcat[entryname] = reader
    logger.debug("Added Zarr reader '%s'", entryname)

    return outcat

def handle_intake1_nested(
    inp:str,
    key:str,
    outcat: intake.entry.Catalog
):
    oldcat = intake.open_catalog(inp)
    try:
        oldcat_entry = oldcat[key]
    except:
        logger.info(f"{key} did not work")
        return outcat
    oldcat_entry_desc = oldcat_entry.describe()
    oldcat_entry_desc = clean_braces(oldcat_entry_desc)
    oldcat_entry_md = oldcat_entry_desc["metadata"]
    oldcat_entry_md.pop("plots",None)
    oldcat_entry_path = oldcat_entry_desc["args"]["path"]
    outcat_entry_path = oldcat_entry_path.replace("main.yaml","main2.yaml")
    if outcat_entry_path == oldcat_entry_path:
        outcat_entry_path = '.'.join(oldcat_entry_path.split('.')[:-1])+"2."+oldcat_entry_path.split('.')[-1]
    logger.info(
        f"We change its path from '{oldcat_entry_path}' to '{outcat_entry_path}'. You have to create the new path as intake v2."
    )
    
    oldcat_entry_new = YAMLCatalogReader(
        outcat_entry_path,
        metadata=oldcat_entry_md
    )
    outcat[key] = oldcat_entry_new
    return outcat


def handle_intake1_yaml(
    catalog_v1: dict,
    outcat: intake.entry.Catalog,
    inp: str = None
):
    """
    Convert an Intake v1 YAML catalog into Intake v2 entries.
    """
    logger.info("Converting Intake v1 catalog")
    logger.info("Adding Parameters")
    sources = catalog_v1.get("sources", {})
    global_md = catalog_v1.get("metadata")
    pms = {}
    if global_md:
        pms = global_md.get("parameters")  
        
    for pm_name,pm_dict in pms.items():
        if not pm_dict["type"] == "str":
            logger.info("Can only handle parameter of type str")
            logger.info(f"Skip {pm_name}")            
            continue
        if pm_dict.get("allowed"):
            outcat.user_parameters[pm_name] = intake.readers.user_parameters.OptionsUserParameter(
                pm_dict["allowed"], default=pm_dict["default"], dtype=str, description=pm_dict.get("description", "NaN")
            )
        else:
            outcat.user_parameters[pm_name] = intake.readers.user_parameters.SimpleUserParameter(
                default=pm_dict["default"], dtype=str, description=pm_dict["description"]
            )


    for key, value in tqdm(sources.items(), total=len(sources)):
        logger.debug("Processing v1 source '%s'", key)

        md = value.get("metadata")
        driver = value.get("driver")
        urlpath = value["args"].get("urlpath")
        
        if driver == "yaml_file_cat":            
            outcat = handle_intake1_nested(
                inp,
                key,
                outcat
            )
            continue
        elif driver == "netcdf" or "netcdf" in driver:
            outcat = handle_netcdf_input(
                entryname=key,
                inp=urlpath,
                outcat=outcat,
                md=md,
                #so=so
                #pms=pms
            )
            continue
            
        so = value["args"].get("storage_options")
        if not urlpath:
            logger.debug(f"{key} does not contain an urlpath, skipped that one.")
            continue

        #pms = value.get("parameters")
        outcat = handle_zarr_input(
            entryname=key,
            inp=urlpath,
            outcat=outcat,
            md=md,
            so=so
            #pms=pms
        )
# -----------------------------------------------------------------------------
# Main conversion logic
# -----------------------------------------------------------------------------

def convert_to_intake2(inputs: list[str], output: str | None):
    """
    Convert inputs into an Intake v2 catalog.
    """
    if output is None:
        output = "intake2.yaml"

    outpath = Path(output)

    if outpath.exists():
        logger.info("Appending to existing catalog '%s'", output)
        outcat = intake.open_catalog(output)
    else:
        logger.info("Creating new catalog")
        outcat = intake.entry.Catalog()

    for inp in inputs:
        logger.info("Processing input '%s'", inp)

        catalog_input = None
        try:
            catalog_input = yaml.safe_load(fsspec.open(inp).open())
        except Exception:
            pass

        if isinstance(catalog_input, dict) and "sources" in catalog_input:
            logger.info("Detected Intake v1 YAML '%s'", inp)
            logger.info("Clean braces")
            catalog_input = clean_braces(catalog_input)
            logger.info("Adding CATALOG_PATH")
            add_catalog_dir(outcat, inp)
            handle_intake1_yaml(catalog_input, outcat, inp=inp)
        else:
            inpname, inppath = parse_inputname(inp)
            if inpname is None:
                inpname = Path(inppath).stem

            handle_zarr_input(
                entryname=inpname,
                inp=inppath,
                outcat=outcat,
            )

    logger.info("Writing catalog to '%s'", output)
    outcat.to_yaml_file(output)


# -----------------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------------

def main():
    """CLI entry point."""
    setup_logging()

    parser = argparse.ArgumentParser(
        description="Convert Zarr, reference, or Intake v1 catalogs to Intake v2 catalogs"
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="Input(s) followed optionally by output catalog",
    )
    
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity",
    )    
    
    parser.add_argument(
        "-o", "--out",
        default="intake2.yaml",
        help="Output Intake v2 catalog (default: intake2.yaml)"
    )    

    args = parser.parse_args()
    
    setup_logging(getattr(logging, args.log_level))

    inputs = args.paths
    output = args.out

    if len(inputs) > 1 and output is None:
        parser.error("Multiple inputs require an explicit output catalog")

    convert_to_intake2(inputs, output)


if __name__ == "__main__":
    main()
