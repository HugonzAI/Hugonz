#!/usr/bin/env python3
"""
ESA615 Serial Connector Module
Version: 1.0

Handles serial communication with Fluke ESA615 device.
- Connect/disconnect
- Remote mode control
- File list retrieval
- DTA file download

Part of EST Converter V3.3 extension (does not modify core functions).
"""

import serial
import time


class ESA615Connector:
    """ESA615设备连接器 - 优化速度版本"""

    def __init__(self, port='COM8', baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def connect(self):
        """连接到ESA615设备"""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                write_timeout=1
            )
            time.sleep(0.3)
            return True, f"Connected to {self.port} @ {self.baudrate} baud"
        except Exception as e:
            return False, f"Connection failed: {e}"

    def send_command(self, cmd, wait_time=0.1):
        """发送命令 - 优化速度"""
        if self.ser and self.ser.is_open:
            command = f"{cmd}\r\n\n".encode('ascii')
            self.ser.write(command)
            self.ser.flush()
            if wait_time > 0:
                time.sleep(wait_time)

    def read_response(self, max_wait=0.5):
        """读取响应 - 优化速度"""
        response = b""
        start_time = time.time()

        while (time.time() - start_time) < max_wait:
            if self.ser.in_waiting > 0:
                chunk = self.ser.read(self.ser.in_waiting)
                response += chunk
                start_time = time.time()
            else:
                time.sleep(0.01)

        return response.decode('ascii', errors='ignore')

    def identify_device(self):
        """识别设备"""
        self.send_command("IDENT", wait_time=0.1)
        response = self.read_response(max_wait=0.5)
        return response.strip()

    def enter_remote_mode(self):
        """进入远程模式"""
        self.send_command("REMOTE", wait_time=0.1)
        self.read_response(max_wait=0.3)
        self.send_command("ANSURON", wait_time=0.1)
        self.read_response(max_wait=0.3)

    def exit_remote_mode(self):
        """退出远程模式"""
        self.send_command("ANSUROFF", wait_time=0.1)
        self.send_command("LOCAL", wait_time=0.1)

    def get_file_list(self):
        """获取文件列表"""
        self.send_command("GETDIR", wait_time=0.1)
        response = self.read_response(max_wait=1.0)

        files = []
        lines = response.strip().split('\r\n')
        for line in lines:
            if line.endswith('.dta'):
                files.append(line.strip())

        return files

    def download_file(self, filename):
        """下载文件 - 优化速度（3-5x faster）"""
        self.send_command(f"OPENFILE={filename},R", wait_time=0.1)
        self.read_response(max_wait=0.3)

        full_content = ""
        chunk_count = 0

        while True:
            self.send_command("GETFILE", wait_time=0.05)
            response = self.read_response(max_wait=0.3)

            if response.strip() == "*":
                break

            full_content += response
            chunk_count += 1

            if chunk_count % 10 == 0:
                time.sleep(0.05)

        return full_content

    def disconnect(self):
        """断开连接"""
        if self.ser and self.ser.is_open:
            self.ser.close()
