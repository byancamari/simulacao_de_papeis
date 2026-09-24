import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Decisor(Node):
    def __init__(self):
        super().__init__('decisor')

        # Guarda a última distância recebida de cada robô.
        self.distancias = {}
        self.publicador_papeis = self.create_publisher(String, '/papeis', 10)

        self.inscricao = self.create_subscription(
            String,
            '/deteccoes',
            self.receber_deteccao,
            10
        )
        self.timer = self.create_timer(4.0, self.decidir_papeis)
        self.get_logger().info('Nó decisor iniciado')

    def receber_deteccao(self, mensagem):
        robot_id_texto, distancia_texto = mensagem.data.split(',')
        robot_id = int(robot_id_texto)
        distancia = float(distancia_texto)

        self.distancias[robot_id] = distancia
        self.get_logger().info(f'Últimas distâncias: {self.distancias}')

    def decidir_papeis(self):
        if len(self.distancias) < 3:
            return

        # Menor distância vence; em caso de empate, vence o menor ID.
        atacante = min(
            self.distancias,
            key=lambda robot_id: (self.distancias[robot_id], robot_id)
        )

        restantes = sorted(
            robot_id for robot_id in self.distancias
            if robot_id != atacante
        )
        goleiro = restantes[0]
        apoio = restantes[1]

        self.get_logger().info(
            f'Robô {atacante}: atacante | '
            f'Robô {goleiro}: goleiro | '
            f'Robô {apoio}: apoio'
        )

        
        for robot_id, papel in (
            (atacante, 'atacante'),
            (goleiro, 'goleiro'),
            (apoio, 'apoio'),
        ):
            mensagem = String()
            mensagem.data = f'{robot_id},{papel},{self.distancias[robot_id]:.2f}'
            self.publicador_papeis.publish(mensagem)

def main(args=None):
    rclpy.init(args=args)
    decisor = Decisor()

    try:
        rclpy.spin(decisor)
    finally:
        decisor.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()