import subprocess as sp
import robothub_depthai
import robothub
from depthai_sdk.classes.packets import FramePacket
import utils

class StreamingApp(robothub_depthai.RobotHubApplication):

    config = robothub.CONFIGURATION
    bitrate: int = config["bitrate"]
    fps: int = config["fps"]
    key: str = config["streaming_key"]
    proc: sp.Popen = None 

    def setup_pipeline(self, camera: robothub_depthai.HubCamera):
        oak = camera.oak_camera

        cam_component = oak.create_camera(
            source="color", resolution="1080p", fps=self.fps, encode='h264'
        )

        def on_update(packet: FramePacket):
            frame_data = packet.msg.getData()
            self.proc.stdin.write(frame_data) # добавил символ новой строки
            self.proc.stdin.flush() # добавил сброс буфера

        oak.callback(cam_component.out.encoded, on_update)

        oak.build()

        cam_component.config_encoder_h26x(bitrate_kbps=self.bitrate)

    def on_start(self):
        command = utils.make_command(self.key)
        if self.proc:
            self.proc.kill()
        self.proc = sp.Popen(command, stdin=sp.PIPE, stderr=None) # добавил stdin=sp.PIPE

        self.setup_pipeline(self.unbooted_cameras[0])

    def on_stop(self):
        if hasattr(self, "proc"): # проверяем, есть ли атрибут proc
            if self.proc:
                self.proc.stdin.close()
                self.proc.kill()
        print("STREAM TERMINATED")

        super().on_stop()

