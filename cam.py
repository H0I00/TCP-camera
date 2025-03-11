import sys
import socket
import threading
import time
import os
import struct

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QRadioButton,
    QGroupBox, QFileDialog, QTextEdit, QMessageBox, QCheckBox
)
from PySide6.QtGui import QPixmap, QTextCursor
from PySide6.QtCore import Qt, Signal, QObject

# ------------------- 信号类，用于线程与UI通信 -------------------
class WorkerSignals(QObject):
    log_signal = Signal(str)       # 用于在UI上追加日志文本
    image_signal = Signal(bytes)   # 用于在UI上显示图像

# ------------------- 网络通信线程 -------------------
class NetworkThread(threading.Thread):
    """
    根据模式（服务器/客户端）启动 TCP 连接，接收数据并解析。
    接收到的文本通过 log_signal 发到 UI，接收到的图像通过 image_signal 发到 UI。
    """
    def __init__(self, 
                 is_server: bool, 
                 server_ip: str, 
                 server_port: int,
                 client_ip: str,
                 client_port: int,
                 signals: WorkerSignals):
        super().__init__()
        self.is_server = is_server
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_ip = client_ip
        self.client_port = client_port
        self.signals = signals
        self.stop_flag = False
        self.sock = None

    def run(self):
        if self.is_server:
            self.start_server()
        else:
            self.start_client()

    def start_server(self):
        """
        服务器模式：监听 server_ip:server_port，等待客户端连接
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((self.server_ip, self.server_port))
            self.sock.listen(1)
            self.signals.log_signal.emit(f"服务器模式已启动：{self.server_ip}:{self.server_port}\n等待客户端连接...\n")

            self.sock.settimeout(1.0)  # 方便检查stop_flag
            conn = None

            while not self.stop_flag:
                try:
                    conn, addr = self.sock.accept()
                except socket.timeout:
                    continue  # 继续等待
                if conn:
                    self.signals.log_signal.emit(f"客户端已连接：{addr}\n")
                    self.handle_connection(conn)
                    conn.close()
                    self.signals.log_signal.emit("客户端已断开连接。\n")

        except Exception as e:
            self.signals.log_signal.emit(f"[服务器异常] {e}\n")
        finally:
            if self.sock:
                self.sock.close()
            self.signals.log_signal.emit("服务器已停止。\n")

    def start_client(self):
        """
        客户端模式：主动连接 server_ip:server_port
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(5)
            self.sock.connect((self.server_ip, self.server_port))
            self.signals.log_signal.emit(f"客户端已连接到：{self.server_ip}:{self.server_port}\n")
            
            # 如果你想让“客户端模式”中，把自己的 IP/port 告诉对方，也可以在此处发送
            # 例如：self.sock.sendall(f"MyIP:{self.client_ip},MyPort:{self.client_port}\n".encode('utf-8'))

            # 开始接收数据
            self.handle_connection(self.sock)

        except Exception as e:
            self.signals.log_signal.emit(f"[客户端异常] {e}\n")
        finally:
            if self.sock:
                self.sock.close()
            self.signals.log_signal.emit("客户端连接已关闭。\n")


    def handle_connection(self, conn: socket.socket):
        """
        实时接收并处理图片流
        """
        conn.settimeout(1.0)
        buffer = b""  
        frame_count = 0  
        last_fps_update = time.time()  
        self.current_fps = 0  # 确保 `self.current_fps` 存在

        while not self.stop_flag:
            try:
                data = conn.recv(4096)  
                if not data:
                    break

                buffer += data  

                start_idx = buffer.find(b"\xff\xd8")  
                end_idx = buffer.find(b"\xff\xd9")  

                if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                    image_data = buffer[start_idx:end_idx+2]  
                    buffer = buffer[end_idx+2:]  

                    # **发送信号更新 UI**
                    self.signals.image_signal.emit(image_data)  

                    # **更新 FPS 计算**
                    frame_count += 1
                    if time.time() - last_fps_update >= 1.0:  
                        self.current_fps = frame_count
                        frame_count = 0
                        last_fps_update = time.time()
                        self.signals.log_signal.emit(f"当前 FPS: {self.current_fps}\n")

            except socket.timeout:
                continue  
            except Exception as e:
                self.signals.log_signal.emit(f"[handle_connection异常] {e}\n")
                break






    def stop(self):
        self.stop_flag = True
        if self.sock:
            try:
                self.sock.close()
            except:
                pass

# ------------------- 主窗口 -------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UARTDisplay-Network (Python + PySide6)")
        self.setFixedSize(1000, 600)

        # --- UI元素 ---
        # 服务器IP、Port
        self.server_ip_edit = QLineEdit("填写电脑ip")
        self.server_ip_edit.setFixedWidth(100)
        self.server_port_edit = QLineEdit("8089")
        self.server_port_edit.setFixedWidth(50)

        # 客户端IP、Port
        self.client_ip_edit = QLineEdit("填写esp8266ip")
        self.client_ip_edit.setFixedWidth(100)
        self.client_port_edit = QLineEdit("8089")
        self.client_port_edit.setFixedWidth(50)

        # 模式选择：服务器模式 / 客户端模式
        self.server_mode_check = QCheckBox("服务器模式")
        self.client_mode_check = QCheckBox("客户端模式")
        self.server_mode_check.setChecked(True)  # 默认服务器模式
        self.client_mode_check.setChecked(False)

        # 监听或连接按钮
        self.start_button = QPushButton("启动")
        self.stop_button = QPushButton("停止")
        self.stop_button.setEnabled(False)

        # 日志显示
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        # 图像显示
        self.image_label = QLabel("图像预览")
        self.image_label.setFixedSize(400, 300)
        self.image_label.setStyleSheet("QLabel { background-color: #EEE; }")
        self.image_label.setAlignment(Qt.AlignCenter)
        
        # 添加 FPS 和 图像信息
        self.fps_label = QLabel("FPS: 0")
        self.image_size_label = QLabel("分辨率: 0 x 0")

        # 设置文本居中
        self.fps_label.setAlignment(Qt.AlignCenter)
        self.image_size_label.setAlignment(Qt.AlignCenter)

        # 添加到界面
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.image_label)
        right_layout.addWidget(self.fps_label)  # 显示 FPS
        right_layout.addWidget(self.image_size_label)  # 显示分辨率
        right_layout.addStretch(1)



        # 布局
        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Server IP:"))
        top_layout.addWidget(self.server_ip_edit)
        top_layout.addWidget(QLabel("Port:"))
        top_layout.addWidget(self.server_port_edit)
        top_layout.addSpacing(20)
        top_layout.addWidget(QLabel("Client IP:"))
        top_layout.addWidget(self.client_ip_edit)
        top_layout.addWidget(QLabel("Port:"))
        top_layout.addWidget(self.client_port_edit)

        mode_layout = QHBoxLayout()
        mode_layout.addWidget(self.server_mode_check)
        mode_layout.addWidget(self.client_mode_check)
        mode_layout.addStretch(1)
        mode_layout.addWidget(self.start_button)
        mode_layout.addWidget(self.stop_button)

        left_layout = QVBoxLayout()
        left_layout.addLayout(top_layout)
        left_layout.addLayout(mode_layout)
        left_layout.addWidget(self.log_text)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.image_label)
        right_layout.addStretch(1)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout, stretch=3)
        main_layout.addLayout(right_layout, stretch=1)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # 线程相关
        self.network_thread = None
        self.signals = WorkerSignals()

        # 信号连接
        self.server_mode_check.stateChanged.connect(self.on_server_mode_changed)
        self.client_mode_check.stateChanged.connect(self.on_client_mode_changed)
        self.start_button.clicked.connect(self.start_network)
        self.stop_button.clicked.connect(self.stop_network)

        self.signals.log_signal.connect(self.append_log)
        self.signals.image_signal.connect(self.show_image)

    def on_server_mode_changed(self, state):
        """
        如果勾选服务器模式，就取消客户端模式
        """
        if state == Qt.Checked:
            self.client_mode_check.setChecked(False)

    def on_client_mode_changed(self, state):
        """
        如果勾选客户端模式，就取消服务器模式
        """
        if state == Qt.Checked:
            self.server_mode_check.setChecked(False)

    def start_network(self):
        """
        启动服务器或客户端线程
        """
        # 读取UI参数
        is_server = self.server_mode_check.isChecked()
        server_ip = self.server_ip_edit.text().strip()
        server_port = int(self.server_port_edit.text().strip())
        client_ip = self.client_ip_edit.text().strip()
        client_port = int(self.client_port_edit.text().strip())

        self.network_thread = NetworkThread(
            is_server=is_server,
            server_ip=server_ip,
            server_port=server_port,
            client_ip=client_ip,
            client_port=client_port,
            signals=self.signals
        )
        self.network_thread.start()

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_network(self):
        """
        停止服务器或客户端线程
        """
        if self.network_thread:
            self.network_thread.stop_flag = True
            self.network_thread.stop()
            self.network_thread.join()
            self.network_thread = None

        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.append_log("网络已停止。\n")

    def append_log(self, text: str):
        """
        在日志窗口追加文本
        """
        self.log_text.moveCursor(QTextCursor.End)
        self.log_text.insertPlainText(text)

    def show_image(self, img_data: bytes):
        """
        直接显示接收到的二进制图像数据，并更新 FPS、分辨率，并保存图片
        """
        pixmap = QPixmap()
        if pixmap.loadFromData(img_data):  
            # 更新 QLabel 显示
            scaled = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio)
            self.image_label.setPixmap(scaled)

            # 获取图像大小
            img_width = pixmap.width()
            img_height = pixmap.height()

            # 更新 FPS 和图像信息
            fps_text = f"FPS: {getattr(self, 'current_fps', 0)}"
            self.fps_label.setText(fps_text)
            self.image_size_label.setText(f"分辨率: {img_width} x {img_height}")

            # **保存图片**
            timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            filename = f"recv_image_{timestamp}.jpg"
            pixmap.save(filename)  # 保存到本地
            self.append_log(f"图像已保存：{filename}\n")

        else:
            self.append_log("图像无法解析为有效格式。\n")






    def closeEvent(self, event):
        """
        关闭窗口时，确保线程退出
        """
        self.stop_network()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
