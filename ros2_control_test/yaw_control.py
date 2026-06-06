import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

class YawRateStabilizer(Node):

    def __init__(self):
        super().__init__('yaw_rate_stabilizer')

        # เริ่มแบบนุ่มๆ ก่อน
        self.kp = 0.25
        self.ki = 0.08

        self.i_limit = 0.3
        self.deadband = 0.05

        self.cmd = Twist()

        self.integral = 0.0
        self.last_t = None

        self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_cb,
            10
        )

        self.create_subscription(
            Odometry,
            '/odometry/filtered',
            self.odom_cb,
            30
        )

        self.pub = self.create_publisher(
            Twist,
            '/cmd_vel_stabilize',
            10
        )

    def cmd_cb(self, msg):
        self.cmd = msg

    def odom_cb(self, msg):

        t = self.get_clock().now().nanoseconds * 1e-9

        if self.last_t is None:
            self.last_t = t
            return

        dt = t - self.last_t
        self.last_t = t

        gz = msg.twist.twist.angular.z

        if abs(gz) < self.deadband:
            gz = 0.0

        target = self.cmd.angular.z

        out = Twist()
        out.linear.x = self.cmd.linear.x
        out.linear.y = self.cmd.linear.y

        moving = (
            abs(self.cmd.linear.x) > 0.02 or
            abs(self.cmd.linear.y) > 0.02
        )

        if moving:

            err = target - gz

            self.integral += err * dt

            self.integral = max(
                -self.i_limit,
                min(self.i_limit, self.integral)
            )

            out.angular.z = (
                target +
                self.kp * err +
                self.ki * self.integral
            )

        else:

            self.integral = 0.0
            out.angular.z = target

        self.pub.publish(out)


def main():
    rclpy.init()

    node = YawRateStabilizer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()