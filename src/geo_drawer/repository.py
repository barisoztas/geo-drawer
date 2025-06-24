from pathlib import Path

import geopandas as gpd
import pandas as pd
import toml
from shapely.geometry import Point


class RepositoryInitiator:
    """Class to initiate a repository"""

    def __init__(self, name, path):
        """Initialize the repository with name and path"""

        self.current_repository = None

        self.default_layers = {"point_layer", "line_layer"}

        self.metadata = {"repo_name": name, "path": Path(path)}

    @classmethod
    def from_conf(cls, name, path):
        """Create a repository from configuration"""
        # check if path exists or not
        if isinstance(path, str):
            path = Path(path)

        if not path.exists():
            msg = f"Path {path} does not exist"
            raise FileNotFoundError(msg)

        return cls(name, path)

    def create_geopackage_repository(self):
        """Create and empty geopackage repository"""
        df = pd.DataFrame(
            {
                "repo_name": [self.metadata["repo_name"]],
                "path": [str(self.metadata["path"])],
            }
        )

        file_name = f"{self.metadata['repo_name']}.gpkg"
        full_path = self.metadata["path"] / file_name

        self.current_repository = full_path

        gpd.GeoDataFrame(df).to_file(full_path, driver="GPKG")

        print(f"Geopackage repository '{file_name}' created at {full_path}")

    def add_default_layers(self):

        gdf = gpd.GeoDataFrame(
            {"id": [1], "geometry": [Point(0, 0)]}, geometry="geometry"
        )

        # This function needs proper implementation
        for layer in self.default_layers:
            gdf.to_file(self.current_repository, layer=layer, driver="GPKG")

            # report if layer writing is succesfull
            print(f"{layer} is created in {self.current_repository} repository")


conf_dict = toml.load("./src/geo_drawer/repository_conf.toml")
metadata = conf_dict["metadata"]

test_repo_initiator = RepositoryInitiator.from_conf(metadata["name"], metadata["path"])
test_repo_initiator.create_geopackage_repository()
test_repo_initiator.add_default_layers()
