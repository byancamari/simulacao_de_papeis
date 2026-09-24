import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Monitor(Node):
    def __init__(self):
        super().__init__('monitor')
        self.papeis = {}
        self.inscricao = self.create_subscription(
            String, '/papeis', self.receber_papel, 10
        )
        self.get_logger().info('Nó monitor iniciado')

    def receber_papel(self, mensagem):
        robot_id_texto, papel, distancia_texto = mensagem.data.split(',')
        robot_id = int(robot_id_texto)
        distancia = float(distancia_texto)

        if papel == 'atacante':
            self.papeis = {}

        if not self.papeis and papel != 'atacante':
            return

        self.papeis[robot_id] = (papel, distancia)

        if papel == 'apoio' and len(self.papeis) == 3:
            resumo = ' | '.join(
                f'Robô {id}: {self.papeis[id][0]} '
                f'({self.papeis[id][1]:.2f} m)'
                for id in sorted(self.papeis)
            )
            self.get_logger().info(resumo)
            self.papeis = {}

def main(args=None):
    rclpy.init(args=args)
    monitor = Monitor()

    try:
        rclpy.spin(monitor)
    finally:
        monitor.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()