import os
import numpy as np
from qgis.PyQt import uic, QtWidgets
from qgis.PyQt.QtWidgets import QFileDialog, QGraphicsScene
from qgis.PyQt.QtGui import QImage, QPixmap, QColor
from qgis.PyQt.QtCore import Qt
from osgeo import gdal

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'preview_window.ui'))

class PreviewWindow(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(PreviewWindow, self).__init__(parent)
        self.setupUi(self)

        self.seed_background_pixmap = None
        self.grow_background_pixmap = None
        self.seed_overlay_pixmap = None
        self.grow_overlay_pixmap = None

        self.btnLoadBackground.clicked.connect(self.load_background_image)
        self.btnLoadGrowPreview.clicked.connect(self.load_grow_for_preview)
        self.btnLoadSeedPreview.clicked.connect(self.load_seed_for_preview)
        self.btnClose.clicked.connect(self.close)

        self.thresholdSliderGrow.setMinimum(0)
        self.thresholdSliderGrow.setMaximum(100)
        self.thresholdSliderGrow.setValue(1)

        self.thresholdSliderSeed.setMinimum(0)
        self.thresholdSliderSeed.setMaximum(100)
        self.thresholdSliderSeed.setValue(1)

        self.thresholdSliderGrow.valueChanged.connect(self.update_grow_threshold_preview)
        self.thresholdSliderSeed.valueChanged.connect(self.update_seed_threshold_preview)

        self.grow_preview_scene = QGraphicsScene()
        self.graphicsView_2.setScene(self.grow_preview_scene)

        self.seed_preview_scene = QGraphicsScene()
        self.graphicsView.setScene(self.seed_preview_scene)

        self.current_grow_matrix = None
        self.current_seed_matrix = None

        self.labelGrowValue.setText(f"Value: {self.thresholdSliderGrow.value() / 100.0:.2f}")
        self.labelSeedValue.setText(f"Value: {self.thresholdSliderSeed.value() / 100.0:.2f}")

    def normalize_band(self, band):
        band_min, band_max = np.percentile(band, (2, 98))
        return ((band - band_min) / (band_max - band_min + 1e-6) * 255).clip(0, 255).astype(np.uint8)

    def load_background_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Sentinel-2 Image (Multi-band)", "", "TIFF files (*.tif *.tiff)"
        )
        if not file_path:
            return

        ds = gdal.Open(file_path)
        if ds is None or ds.RasterCount < 8:
            print("Invalid Sentinel-2 file or not enough bands.")
            return

        try:
            band_nir = ds.GetRasterBand(8).ReadAsArray().astype(np.float32)
            band_red = ds.GetRasterBand(4).ReadAsArray().astype(np.float32)
            band_green = ds.GetRasterBand(3).ReadAsArray().astype(np.float32)

            nir = self.normalize_band(band_nir)
            red = self.normalize_band(band_red)
            green = self.normalize_band(band_green)

            h, w = nir.shape
            rgb = np.zeros((h, w, 3), dtype=np.uint8)
            rgb[..., 0] = nir
            rgb[..., 1] = red
            rgb[..., 2] = green

            image = QImage(rgb.data, w, h, 3 * w, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image.copy())

            self.seed_background_pixmap = pixmap
            self.grow_background_pixmap = pixmap

            self.draw_seed_scene()
            self.draw_grow_scene()

        except Exception as e:
            print(f"Error creating false color composite: {e}")

    def load_grow_for_preview(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Grow Raster", "", "TIFF files (*.tif *.tiff)")
        if not file_path:
            return

        ds = gdal.Open(file_path)
        if ds is None:
            print("Error: Could not open the raster.")
            return

        band = ds.GetRasterBand(1)
        self.current_grow_matrix = band.ReadAsArray().astype(float)
        self.update_grow_threshold_preview(self.thresholdSliderGrow.value())

    def load_seed_for_preview(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Seed Raster", "", "TIFF files (*.tif *.tiff)")
        if not file_path:
            return

        ds = gdal.Open(file_path)
        if ds is None:
            print("Error: Could not open the raster.")
            return

        band = ds.GetRasterBand(1)
        self.current_seed_matrix = band.ReadAsArray().astype(float)
        self.update_seed_threshold_preview(self.thresholdSliderSeed.value())

    def draw_seed_scene(self):
        self.seed_preview_scene.clear()
        if self.seed_background_pixmap:
            self.seed_preview_scene.addPixmap(self.seed_background_pixmap)
        if self.seed_overlay_pixmap:
            self.seed_preview_scene.addPixmap(self.seed_overlay_pixmap)
        self.graphicsView.fitInView(self.seed_preview_scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        self.graphicsView.viewport().update()

    def draw_grow_scene(self):
        self.grow_preview_scene.clear()
        if self.grow_background_pixmap:
            self.grow_preview_scene.addPixmap(self.grow_background_pixmap)
        if self.grow_overlay_pixmap:
            self.grow_preview_scene.addPixmap(self.grow_overlay_pixmap)
        self.graphicsView_2.fitInView(self.grow_preview_scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        self.graphicsView_2.viewport().update()

    def update_seed_threshold_preview(self, slider_value):
        if self.current_seed_matrix is None:
            print("No seed matrix loaded")
            return

        threshold = slider_value / 100.0
        self.labelSeedValue.setText(f"Value: {threshold:.2f}")

        data = self.current_seed_matrix
        mask = data >= threshold
        if not np.any(mask):
            self.seed_overlay_pixmap = None
            self.draw_seed_scene()
            return

        min_val = np.min(data[mask])
        max_val = np.max(data[mask])
        scale = 255 / (max_val - min_val + 1e-6)
        normalized = ((data - min_val) * scale).clip(0, 255).astype(np.uint8)

        h, w = normalized.shape
        img = QImage(w, h, QImage.Format_ARGB32)

        for y in range(h):
            for x in range(w):
                if mask[y, x]:
                    gray = normalized[y, x]
                    color = QColor(gray, gray, gray, 128)
                else:
                    color = QColor(0, 0, 0, 0)
                img.setPixelColor(x, y, color)

        self.seed_overlay_pixmap = QPixmap.fromImage(img.copy())
        self.draw_seed_scene()

    def update_grow_threshold_preview(self, slider_value):
        if self.current_grow_matrix is None:
            print("No grow matrix loaded")
            return

        threshold = slider_value / 100.0
        self.labelGrowValue.setText(f"Value: {threshold:.2f}")

        data = self.current_grow_matrix
        mask = data >= threshold
        if not np.any(mask):
            self.grow_overlay_pixmap = None
            self.draw_grow_scene()
            return

        min_val = np.min(data[mask])
        max_val = np.max(data[mask])
        scale = 255 / (max_val - min_val + 1e-6)
        normalized = ((data - min_val) * scale).clip(0, 255).astype(np.uint8)

        h, w = normalized.shape
        img = QImage(w, h, QImage.Format_ARGB32)

        for y in range(h):
            for x in range(w):
                if mask[y, x]:
                    gray = normalized[y, x]
                    color = QColor(gray, gray, gray, 128)
                else:
                    color = QColor(0, 0, 0, 0)
                img.setPixelColor(x, y, color)

        self.grow_overlay_pixmap = QPixmap.fromImage(img.copy())
        self.draw_grow_scene()
