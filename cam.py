import sys
import socket
import threading
import time
from collections import deque

from PySide6.QtWidgets import QApplication,QWidget
from PySide6.QtGui import QPixmap, QTextCursor
from PySide6.QtCore import Qt, Signal, QObject

from ui_form import Ui_tcpui

# ------------------- 信号类，用于线程与UI通信 -------------------
class WorkerSignals(QObject):
    log_signal = Signal(str)       # 用于在UI上追加日志文本
    image_signal = Signal(bytes)   # 用于在UI上显示图像
    fps_signal = Signal(float)     # 用于在UI上显示 FPS
    update_client_port_signal = Signal(str)  # 用于更新客户端端口号

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
        self.stop_event = threading.Event()  # 使用Event来控制线程停止
        self.sock = None
        self.frame_times = deque(maxlen=10)

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

            self.sock.settimeout(5.0)  # 方便检查stop_flag
            conn = None

            while not self.stop_event.is_set():
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
            self.close_socket()  # 关闭socket
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

            # 开始接收数据
            self.handle_connection(self.sock)

        except Exception as e:
            self.signals.log_signal.emit(f"[客户端异常] {e}\n")
        finally:
            self.close_socket()  # 关闭socket
            self.signals.log_signal.emit("客户端连接已关闭。\n")


    def handle_connection(self, conn: socket.socket):
        """
        实时接收并处理图片流
        """
        conn.settimeout(1.0)
        buffer = b""  # 缓存接收到的数据
        
        client_port = conn.getpeername()[1]
        self.signals.log_signal.emit(f"客户端端口：{client_port}\n")
        self.signals.update_client_port_signal.emit(str(client_port))  # 更新UI中的client_port_edit

        while not self.stop_event.is_set():
            try:
                data = conn.recv(1460)  
                if not data:
                    break

                buffer += data  
                start_idx = buffer.find(b"\xff\xd8")  # JPEG开始标志
                end_idx = buffer.find(b"\xff\xd9")    # JPEG结束标志

                if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                    image_data = buffer[start_idx:end_idx+2]  # 提取图像数据
                    buffer = buffer[end_idx+2:]  # 更新缓冲区

                    # 计算 FPS
                    self.frame_times.append(time.time())
                    if len(self.frame_times) > 1:
                        fps = len(self.frame_times) / (self.frame_times[-1] - self.frame_times[0])
                    else:
                        fps = 0
                        
                    self.signals.image_signal.emit(image_data)  # 只发送图像数据
                    self.signals.fps_signal.emit(fps)  # 发送 FPS 信息

            except (socket.timeout, ConnectionResetError, socket.error, OSError) as e:
                self.signals.log_signal.emit(f"[网络异常] {e}\n")
                continue  # 继续接收数据
            except Exception as e:
                self.signals.log_signal.emit(f"[handle_connection异常] {e}\n")
                break

    def close_socket(self):
        """关闭socket连接"""
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
            except socket.error as e:
                self.signals.log_signal.emit(f"[关闭异常] {e}\n")

    def stop(self):
        self.stop_event.set()  # 停止线程
        self.close_socket()  # 确保socket关闭

# ------------------- 主窗口 -------------------
class tcpui(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_tcpui()
        self.ui.setupUi(self)
        self.setWindowTitle("UARTDisplay-Network (Python + PySide6)")
       
        # 线程相关
        self.network_thread = None
        self.signals = WorkerSignals()

        self.ui.start_button.setEnabled(True)
        self.ui.stop_button.setEnabled(False)

        # 信号连接       
        self.ui.start_button.clicked.connect(self.start_network)
        self.ui.stop_button.clicked.connect(self.stop_network)

        self.signals.log_signal.connect(self.append_log)
        self.signals.image_signal.connect(self.show_image)
        self.signals.fps_signal.connect(self.update_fps)
        self.signals.update_client_port_signal.connect(self.update_client_port)

    def update_ui_for_network_status(self, running: bool):
        """更新UI界面状态，并改变输入框的背景颜色"""
        disabled_style = "background-color:rgb(220, 220, 220);"  # 灰色背景
        enabled_style = ""  # 恢复默认背景

        # 设置禁用状态
        self.ui.server_ip_edit.setEnabled(not running)
        self.ui.server_port_edit.setEnabled(not running)
        self.ui.client_ip_edit.setEnabled(not running)
        self.ui.client_port_edit.setEnabled(not running)

        # 修改背景色
        self.ui.server_ip_edit.setStyleSheet(disabled_style if running else enabled_style)
        self.ui.server_port_edit.setStyleSheet(disabled_style if running else enabled_style)
        self.ui.client_ip_edit.setStyleSheet(disabled_style if running else enabled_style)
        self.ui.client_port_edit.setStyleSheet(disabled_style if running else enabled_style)

        self.ui.start_button.setEnabled(not running)
        self.ui.stop_button.setEnabled(running)


    def start_network(self):
        """
        启动服务器或客户端线程
        """
        # 读取UI参数
        is_server = self.ui.server_mode_check.isChecked()
        server_ip = self.ui.server_ip_edit.text().strip()
        server_port = int(self.ui.server_port_edit.text().strip())
        client_ip = self.ui.client_ip_edit.text().strip()
        client_port = int(self.ui.client_port_edit.text().strip())
        
        # 禁用输入框
        self.update_ui_for_network_status(True)

        self.network_thread = NetworkThread(
            is_server=is_server,
            server_ip=server_ip,
            server_port=server_port,
            client_ip=client_ip,
            client_port=client_port,
            signals=self.signals
        )
        self.network_thread.start()

    def stop_network(self):
        """
        停止服务器或客户端线程
        """
        if self.network_thread:
            self.network_thread.stop()  # 确保 socket 关闭
            if self.network_thread.is_alive():
                self.network_thread.join()  # 等待线程安全退出
            self.network_thread = None

        # 启用输入框
        self.update_ui_for_network_status(False)

        self.append_log("网络已停止。\n")

    def append_log(self, text: str):
        """
        在日志窗口追加文本
        """
        self.ui.textBrowser.moveCursor(QTextCursor.End)
        self.ui.textBrowser.insertPlainText(text)

    def show_image(self, img_data: bytes):
        """
        直接显示接收到的二进制图像数据，并更新 FPS、分辨率，并保存图片
        """
        pixmap = QPixmap()
        if pixmap.loadFromData(img_data):  
            # 更新 QLabel 显示
            scaled = pixmap.scaled(self.ui.image_label.size(), Qt.KeepAspectRatio)
            self.ui.image_label.setPixmap(scaled)

            # 获取图像大小
            img_width = pixmap.width()
            img_height = pixmap.height()

            # 更新图像信息
            self.ui.image_size_label.setText(f"分辨率: {img_width} x {img_height}")

            # **保存图片**
        if self.ui.save_check.isChecked():
            timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
            filename = f"recv_image_{timestamp}.jpg"
            pixmap.save(filename)  # 保存到本地
            self.append_log(f"图像已保存：{filename}\n")

    def update_fps(self, fps: float):
        """
        更新 FPS 信息
        """
        self.ui.fps_label.setText(f"FPS: {fps:.2f}")
        
    def update_client_port(self, port: str):
        """
        更新客户端端口
        """
        self.ui.client_port_edit.setText(port)  # 更新client_port_edit显示的内容

    def closeEvent(self, event):
        """
        关闭窗口时，确保线程退出
        """
        self.stop_network()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = tcpui()
    widget.show()
    sys.exit(app.exec())
