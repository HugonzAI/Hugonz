#!/usr/bin/env python3
"""
ESA615 UI Addon Module
Version: 1.0

Provides UI components for ESA615 device integration:
- Connection status and controls
- File list with selection
- Download management
- Progress tracking

Part of EST Converter V3.3 extension (UI layer only, does not modify core).
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem,
    QCheckBox, QComboBox
)
from PySide6.QtCore import Qt, QThread, Signal
import os
from esa615_connector import ESA615Connector
from dta_to_csv_converter import DTAtoCSVConverter


class ESA615DownloadThread(QThread):
    """后台下载线程"""
    progress = Signal(str)
    finished = Signal(bool, str, list)

    def __init__(self, port, selected_files, output_dir):
        super().__init__()
        self.port = port
        self.selected_files = selected_files
        self.output_dir = output_dir

    def run(self):
        try:
            conn = ESA615Connector(self.port, 115200)

            success, msg = conn.connect()
            if not success:
                self.finished.emit(False, msg, [])
                return

            self.progress.emit(f"✓ {msg}")

            device_info = conn.identify_device()
            self.progress.emit(f"Device: {device_info}")

            conn.enter_remote_mode()
            self.progress.emit("✓ Remote mode")

            downloaded = []
            total = len(self.selected_files)

            for i, filename in enumerate(self.selected_files):
                self.progress.emit(f"[{i+1}/{total}] {filename}")

                dta_content = conn.download_file(filename)

                csv_filename = filename.replace('.dta', '.csv')
                csv_path = os.path.join(self.output_dir, csv_filename)

                converter = DTAtoCSVConverter(dta_content)
                converter.to_csv(csv_path)

                downloaded.append(csv_path)
                self.progress.emit(f"✓ {csv_filename}")

            conn.exit_remote_mode()
            conn.disconnect()
            self.progress.emit("✓ Disconnected")

            self.finished.emit(True, f"Downloaded {len(downloaded)} files", downloaded)

        except Exception as e:
            self.finished.emit(False, str(e), [])


class ESA615Widget(QWidget):
    """ESA615面板：连接+文件列表+下载"""
    files_downloaded = Signal(list)  # 发送已下载的CSV文件路径

    def __init__(self, output_dir, log_callback):
        super().__init__()
        self.output_dir = output_dir
        self.log = log_callback
        self.download_thread = None
        self.device_files = []

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # 顶部：连接状态 + 操作按钮
        top_row = QHBoxLayout()

        # COM端口选择（隐藏显示，默认COM8）
        self.port_combo = QComboBox()
        self.port_combo.addItems(['COM1', 'COM2', 'COM3', 'COM4', 'COM5',
                                  'COM6', 'COM7', 'COM8', 'COM9', 'COM10'])
        self.port_combo.setCurrentText('COM8')
        self.port_combo.setMaximumWidth(80)

        # 状态指示灯
        self.status_indicator = QLabel("●")
        self.status_indicator.setStyleSheet("color: gray; font-size: 20pt;")
        self.status_indicator.setToolTip("Disconnected")

        self.status_label = QLabel("Not connected")
        self.status_label.setStyleSheet("color: #666; font-weight: bold;")

        self.btn_connect = QPushButton("🔌 Connect")
        self.btn_connect.setFixedHeight(36)
        self.btn_connect.clicked.connect(self.toggle_connection)

        self.btn_refresh = QPushButton("🔄 Refresh")
        self.btn_refresh.setFixedHeight(36)
        self.btn_refresh.setEnabled(False)
        self.btn_refresh.clicked.connect(self.refresh_file_list)

        top_row.addWidget(QLabel("Port:"))
        top_row.addWidget(self.port_combo)
        top_row.addWidget(self.status_indicator)
        top_row.addWidget(self.status_label)
        top_row.addStretch()
        top_row.addWidget(self.btn_connect)
        top_row.addWidget(self.btn_refresh)

        # 文件列表（带勾选框）
        list_header = QHBoxLayout()
        self.btn_select_all = QPushButton("☑ Select All")
        self.btn_select_all.setMaximumWidth(100)
        self.btn_select_all.clicked.connect(self.select_all)

        self.btn_deselect_all = QPushButton("☐ Clear")
        self.btn_deselect_all.setMaximumWidth(100)
        self.btn_deselect_all.clicked.connect(self.deselect_all)

        self.btn_delete = QPushButton("🗑 Delete")
        self.btn_delete.setMaximumWidth(100)
        self.btn_delete.clicked.connect(self.delete_selected)

        self.file_count_label = QLabel("Files: 0")
        self.file_count_label.setStyleSheet("font-weight: bold;")

        list_header.addWidget(QLabel("Test Results on Device:"))
        list_header.addStretch()
        list_header.addWidget(self.file_count_label)
        list_header.addWidget(self.btn_select_all)
        list_header.addWidget(self.btn_deselect_all)
        list_header.addWidget(self.btn_delete)

        self.file_list = QListWidget()
        self.file_list.setMinimumHeight(250)
        self.file_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 8px;
                background: white;
                font-family: 'Consolas', monospace;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QListWidget::item:hover {
                background: #f5f5f5;
            }
        """)

        # 底部：下载按钮
        self.btn_download = QPushButton("📥 Download Selected")
        self.btn_download.setEnabled(False)
        self.btn_download.setMinimumHeight(40)
        self.btn_download.setStyleSheet("""
            QPushButton {
                background: #10b981;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background: #059669;
            }
            QPushButton:disabled {
                background: #d1d5db;
                color: #9ca3af;
            }
        """)
        self.btn_download.clicked.connect(self.download_selected)

        # 组装
        layout.addLayout(top_row)
        layout.addLayout(list_header)
        layout.addWidget(self.file_list)
        layout.addWidget(self.btn_download)

        self.setLayout(layout)
        self.connected = False

    def toggle_connection(self):
        """连接/断开ESA615"""
        if not self.connected:
            self.connect_device()
        else:
            self.disconnect_device()

    def connect_device(self):
        """连接设备"""
        port = self.port_combo.currentText()
        self.log(f"Connecting to {port}...")

        try:
            self.conn = ESA615Connector(port, 115200)
            success, msg = self.conn.connect()

            if success:
                device_info = self.conn.identify_device()
                self.log(f"✓ {msg}")
                self.log(f"Device: {device_info}")

                self.connected = True
                self.status_indicator.setStyleSheet("color: #10b981; font-size: 20pt;")
                self.status_indicator.setToolTip("Connected")
                self.status_label.setText("Connected")
                self.status_label.setStyleSheet("color: #10b981; font-weight: bold;")
                self.btn_connect.setText("🔌 Disconnect")
                self.btn_refresh.setEnabled(True)
                self.btn_download.setEnabled(True)

                # 自动刷新文件列表
                self.refresh_file_list()
            else:
                self.log(f"✗ {msg}")

        except Exception as e:
            self.log(f"✗ Error: {e}")

    def disconnect_device(self):
        """断开设备"""
        try:
            if hasattr(self, 'conn'):
                self.conn.disconnect()

            self.connected = False
            self.status_indicator.setStyleSheet("color: gray; font-size: 20pt;")
            self.status_indicator.setToolTip("Disconnected")
            self.status_label.setText("Disconnected")
            self.status_label.setStyleSheet("color: #666; font-weight: bold;")
            self.btn_connect.setText("🔌 Connect")
            self.btn_refresh.setEnabled(False)
            self.btn_download.setEnabled(False)

            self.log("✓ Disconnected from ESA615")

        except Exception as e:
            self.log(f"✗ Disconnect error: {e}")

    def refresh_file_list(self):
        """刷新设备文件列表"""
        if not self.connected:
            return

        try:
            self.conn.enter_remote_mode()
            self.device_files = self.conn.get_file_list()
            self.conn.exit_remote_mode()

            self.file_list.clear()

            for filename in self.device_files:
                item = QListWidgetItem()

                checkbox = QCheckBox(filename)
                checkbox.setStyleSheet("font-family: 'Consolas'; padding: 4px;")

                self.file_list.addItem(item)
                self.file_list.setItemWidget(item, checkbox)

            self.file_count_label.setText(f"Files: {len(self.device_files)}")
            self.log(f"✓ Found {len(self.device_files)} test files")

        except Exception as e:
            self.log(f"✗ Refresh error: {e}")

    def select_all(self):
        """全选"""
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            widget = self.file_list.itemWidget(item)
            if isinstance(widget, QCheckBox):
                widget.setChecked(True)

    def deselect_all(self):
        """取消全选"""
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            widget = self.file_list.itemWidget(item)
            if isinstance(widget, QCheckBox):
                widget.setChecked(False)

    def delete_selected(self):
        """删除选中的列表项（仅UI，不删除设备文件）"""
        items_to_remove = []
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            widget = self.file_list.itemWidget(item)
            if isinstance(widget, QCheckBox) and widget.isChecked():
                items_to_remove.append(i)

        for i in reversed(items_to_remove):
            self.file_list.takeItem(i)

        self.file_count_label.setText(f"Files: {self.file_list.count()}")
        self.log(f"Removed {len(items_to_remove)} items from list")

    def download_selected(self):
        """下载选中的文件"""
        if not self.connected:
            self.log("✗ Not connected to device")
            return

        selected = []
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            widget = self.file_list.itemWidget(item)
            if isinstance(widget, QCheckBox) and widget.isChecked():
                selected.append(widget.text())

        if not selected:
            self.log("✗ No files selected")
            return

        self.log(f"Downloading {len(selected)} file(s)...")
        self.btn_download.setEnabled(False)

        self.download_thread = ESA615DownloadThread(
            self.port_combo.currentText(),
            selected,
            self.output_dir
        )

        self.download_thread.progress.connect(self.log)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.start()

    def on_download_finished(self, success, message, csv_files):
        """下载完成"""
        self.btn_download.setEnabled(True)

        if success:
            self.log(f"✓ {message}")
            # 通知主窗口已下载的CSV文件
            self.files_downloaded.emit(csv_files)
        else:
            self.log(f"✗ {message}")
