import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, TwistStamped


class JoyControl(Node):
    def __init__(self):
        super().__init__("joy_control")
        self.sub_ = self.create_subscription(Twist, "/cmd_vel", self.callback, 10)
        self.pub_ = self.create_publisher(
            TwistStamped, "/mecanum_drive_controller/reference", 10)

        self.last = TwistStamped()
        self.last.header.frame_id = "base_link"

        # republish 30Hz -> stream ต่อเนื่อง, ค้างค่าล่าสุดจนกว่าจะมีคำสั่งใหม่
        self.timer_ = self.create_timer(1.0 / 30.0, self.republish)

    def callback(self, msg: Twist):
        out = TwistStamped()
        out.header.frame_id = "base_link"
        out.twist = msg
        self.last = out

    def republish(self):
        # ค้างค่าล่าสุดเสมอ (ไม่มี timeout) — หยุดเฉพาะเมื่อได้คำสั่งศูนย์
        self.last.header.stamp = self.get_clock().now().to_msg()
        self.pub_.publish(self.last)


def main():
    rclpy.init()
    node = JoyControl()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()