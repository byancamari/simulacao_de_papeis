import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Detector(Node):
    def __init__(self):
        super().__init__('detector')

        self.declare_parameter('robot_id', 1)
        self.robot_id = self.get_parameter('robot_id').value

        self.publicador = self.create_publisher(String, '/deteccoes', 10)
        self.timer = self.create_timer(1.0, self.publicar_deteccao)

        self.get_logger().info(f'Detector do robô {self.robot_id} iniciado')

    def publicar_deteccao(self):
        distancia = round(random.uniform(0.5, 10.0), 2)

        mensagem = String()
        mensagem.data = f'{self.robot_id},{distancia}'
        self.publicador.publish(mensagem)

        self.get_logger().info(
            f'Robô {self.robot_id}: distância {distancia} metros'
        )


def main(args=None):
    rclpy.init(args=args)
    detector = Detector()

    try:
        rclpy.spin(detector)
    finally:
        detector.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()