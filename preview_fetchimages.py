import os
import numpy as np
from qgis.PyQt import uic, QtWidgets
from qgis.PyQt.QtWidgets import QFileDialog, QGraphicsScene
from qgis.PyQt.QtGui import QImage, QPixmap, QColor
from qgis.PyQt.QtCore import Qt
from osgeo import gdal

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'preview_fetchimages.ui'))

class PreviewFetchImages(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(PreviewFetchImages, self).__init__(parent)
        self.setupUi(self)

        #self.seed_background_pixmap = None
        
        self.overlay_pixmap = None
        
        self.btnClose.clicked.connect(self.close)

        self.preview_scene = QGraphicsScene()
        self.graphicsView.setScene(self.preview_scene)

    #---code copied from preview_window.py TO BE CHECKED---#
    #    ds = gdal.Open(file_path)
    #    if ds is None or ds.RasterCount < 8:
    #        print("Invalid Sentinel-2 file.")
    #        return

 #       try:
 #           band_nir = ds.GetRasterBand(8).ReadAsArray().astype(np.float32)
 #           band_red = ds.GetRasterBand(4).ReadAsArray().astype(np.float32)
 #           band_green = ds.GetRasterBand(3).ReadAsArray().astype(np.float32)

 #           nir = self.normalize_band(band_nir)
 #           red = self.normalize_band(band_red)
 #           green = self.normalize_band(band_green)

 #           h, w = nir.shape
 #           rgb = np.zeros((h, w, 3), dtype=np.uint8)
 #           rgb[..., 0] = nir
 #           rgb[..., 1] = red
 #           rgb[..., 2] = green

 #           image = QImage(rgb.data, w, h, 3 * w, QImage.Format_RGB888)
 #           pixmap = QPixmap.fromImage(image.copy())

 #           self.seed_background_pixmap = pixmap
 #           self.grow_background_pixmap = pixmap

 #           self.draw_seed_scene()
 #           self.draw_grow_scene()

   #     except Exception as e:
  #          print(f"Error creating false color composite: {e}")

    def load_image_for_preview(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select image", "", "TIFF files (*.tif *.tiff)")
        if not file_path:
            return

        ds = gdal.Open(file_path)
        if ds is None:
            print("Error: Could not open the raster.")
            return

        #band = ds.GetRasterBand(1)
        #self.current_grow_matrix = band.ReadAsArray().astype(float)
        #self.update_grow_threshold_preview(self.thresholdSliderGrow.value())

    def draw_scene(self):
        self.preview_scene.clear()

        if self.radioButton_RGB.isChecked():
            # RGB composito: bande 4-3-2
            r = ds.GetRasterBand(4).ReadAsArray().astype(np.float32)
            g = ds.GetRasterBand(3).ReadAsArray().astype(np.float32)
            b = ds.GetRasterBand(2).ReadAsArray().astype(np.float32)

            # Normalizzazione
            rgb = np.stack([r, g, b], axis=-1)
            rgb = ((rgb - rgb.min()) / (rgb.max() - rgb.min() + 1e-6) * 255).astype(np.uint8)

            h, w, _ = rgb.shape
            img = QImage(rgb.data, w, h, 3 * w, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(img.copy())
            self.overlay_pixmap = pixmap

        elif self.radioButton_NBR.isChecked():
            # NBR: (NIR - SWIR) / (NIR + SWIR)
            nir = ds.GetRasterBand(8).ReadAsArray().astype(np.float32)
            swir = ds.GetRasterBand(12).ReadAsArray().astype(np.float32)
            nbr = (nir - swir) / (nir + swir + 1e-6)

            # Normalization
            nbr_scaled = ((nbr - nbr.min()) / (nbr.max() - nbr.min() + 1e-6) * 255).astype(np.uint8)

            h, w = nbr_scaled.shape
            img = QImage(w, h, QImage.Format_RGB32)
            for y in range(h):
                for x in range(w):
                    val = nbr_scaled[y, x]
                    color = QColor(val, 255 - val, 0, 255)  # colormap: verde → rosso
                    img.setPixelColor(x, y, color)

            pixmap = QPixmap.fromImage(img.copy())
            self.overlay_pixmap = pixmap

        # Show scene
        if self.overlay_pixmap:
            self.preview_scene.addPixmap(self.overlay_pixmap)
            self.graphicsView.fitInView(self.preview_scene.itemsBoundingRect(), Qt.KeepAspectRatio)
            self.graphicsView.viewport().update()


    #def draw_scene(self):
    #   self.seed_preview_scene.clear()
    #    if self.overlay_pixmap:
    #        self.preview_scene.addPixmap(self.seed_overlay_pixmap)
    #    self.graphicsView.fitInView(self.seed_preview_scene.itemsBoundingRect(), Qt.KeepAspectRatio)
    #    self.graphicsView.viewport().update()



    #    data = self.current_seed_matrix
    #    mask = data >= threshold
    #    if not np.any(mask):
    #        self.seed_overlay_pixmap = None
    #        self.draw_seed_scene()
    #        return

    #    min_val = np.min(data[mask])
    #    max_val = np.max(data[mask])
    #    scale = 255 / (max_val - min_val + 1e-6)
    #    normalized = ((data - min_val) * scale).clip(0, 255).astype(np.uint8)

    #    h, w = normalized.shape
    #    img = QImage(w, h, QImage.Format_ARGB32)

    #    for y in range(h):
    #        for x in range(w):
    #            if mask[y, x]:
    #                gray = normalized[y, x]
    #                color = QColor(gray, gray, gray, 128)
    #            else:
    #                color = QColor(0, 0, 0, 0)
    #            img.setPixelColor(x, y, color)

    #    self.seed_overlay_pixmap = QPixmap.fromImage(img.copy())
    #    self.draw_seed_scene()

