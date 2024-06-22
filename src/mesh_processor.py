# mesh_processor.py
from src.project import Project
import Metashape

"""
Determina la creazione della mesh del modello, la texture a partire dalle foto e il tiled model
"""

class MeshProcessor:

    def __init__(self) -> None:
        self.project = Project.get_project()

    """
    Build 3D model 
    """
    def buildModel(self, progress_printer: str, **kwargs) -> None:
        default_params = {
            'surface_type': Metashape.Arbitrary,
            'source_data': Metashape.DepthMapsData,
            'interpolation': Metashape.EnabledInterpolation,
            'face_count': Metashape.HighFaceCount,
            'vertex_colors': True,
            'vertex_confidence': True,
            'keep_depth': True,
            'build_texture': True,
            'subdivide_task': True
        }
        # update default params with the input
        default_params.update(kwargs)
        self.project.chunk.buildModel(progress=progress_printer, **default_params)
        self.project.save_project(version="buildModel")

    """
    Colorize 3D model
    """
    def colorizeModel(self, progress_printer: str) -> None:
        self.project.chunk.colorizeModel(source_data=Metashape.ImagesData, progress=progress_printer)
        self.project.save_project(version="colorizeModel")

    """
    Generate uv mapping for the model
    """
    def buildUV(self, progress_printer: str, **kwargs) -> None:
        default_params = {
            'mapping_mode': Metashape.GenericMapping,
            'page_count': 1,
            'texture_size': 8192
        }
        # update default params with the input
        default_params.update(kwargs)
        self.project.chunk.buildUV(progress=progress_printer, **default_params)
        self.project.save_project(version="buildUV")

    """
    Generate texture layer
    """
    def buildTexture(self, progress_printer: str, **kwargs) -> None:
        default_params = {
            'blending_mode': Metashape.MosaicBlending,
            'texture_size': 8192,
            'fill_holes': True,
            'ghosting_filter': True
        }
        # update default params with the input
        default_params.update(kwargs)
        self.project.chunk.buildTexture(progress=progress_printer, **default_params)
        self.project.save_project(version="buildTexture")

    # TODO: detectMarkers
        
    # TODO: buildTiledModel: https://www.agisoft.com/forum/index.php?topic=13206.0
    """
    Build tiled model
    """
    def buildTiledModel(self, progress_printer: str, **kwargs) -> None:
        default_params = {
            'pixel_size': 0,
            'tile_size': 256,
            'source_data': Metashape.DataSource.DepthMapsData,
            'face_count': 20000,
            'ghosting_filter': False,
            'transfer_texture': False,
            'keep_depth': True,
            'subdivide_task': True
        }
        # update default params with the input
        default_params.update(kwargs)
        self.project.chunk.buildTiledModel(progress=progress_printer, **default_params)
        self.project.save_project(version="buildTiledModel")

    """
    Export Model
    """
    def exportModel(self, progress_printer: str, path: str, **kwargs) -> None:
        if self.project.chunk.model:
            default_params = {
                "texture_format": Metashape.ImageFormat.ImageFormatTIFF,
                "save_texture": True,
                "save_uv": True,
                "save_normals": True,
                "save_colors": True,
                "save_confidence": True,
                "save_cameras": True,
                "save_markers": True,
                "embed_texture": True,
                "format": Metashape.ModelFormat.ModelFormatOBJ
            }
            # update default params with the input
            default_params.update(kwargs)
            self.project.chunk.exportModel(path=path+'/model/model.obj', progress= progress_printer, **default_params)
