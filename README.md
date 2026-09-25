# Eleição de papéis — ROS 2

Simulação em Python com `rclpy`: três robôs informam distâncias até a bola e recebem os papéis de atacante, goleiro e apoio.

## Como funciona

- Usei o parâmetro ROS 2 `robot_id` para executar três instâncias do mesmo detector, com IDs 1, 2 e 3. Assim, não preciso duplicar o código para cada robô.
- Cada detector publica `robot_id,distância` em `/deteccoes`. O decisor mantém a distância mais recente informada por cada ID.
- O robô com menor distância vira atacante. Em caso de empate, vence o menor ID. Dos dois restantes, o menor ID vira goleiro e o outro vira apoio.
- O decisor publica uma mensagem por robô em `/papeis`, no formato `robot_id,papel,distância`. Incluí a distância para conferir a escolha no monitor.
- O monitor reúne as três mensagens da decisão em uma linha. Como as distâncias simuladas mudam, o atacante também pode mudar.

## Compilar

Requer ROS 2 Jazzy e `colcon`:

```bash
git clone https://github.com/byancamari/byancamari-simulacao_de_papeis.git
cd byancamari-simulacao_de_papeis
source /opt/ros/jazzy/setup.bash
colcon build --packages-select eleicao_papeis
source install/setup.bash
```

## Executar

No **terminal 1**, dentro da pasta do repositório, carregue o ambiente e inicie os três detectores e o decisor:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 run eleicao_papeis detector --ros-args -p robot_id:=1 > /tmp/detector1.log 2>&1 &
ros2 run eleicao_papeis detector --ros-args -p robot_id:=2 > /tmp/detector2.log 2>&1 &
ros2 run eleicao_papeis detector --ros-args -p robot_id:=3 > /tmp/detector3.log 2>&1 &
ros2 run eleicao_papeis decisor > /tmp/decisor.log 2>&1 &
```

No **terminal 2**, entre na mesma pasta, carregue o ambiente e execute o monitor:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
ros2 run eleicao_papeis monitor
```

O monitor exibe os papéis e as distâncias juntos. Para encerrar, pressione `Ctrl+C` no terminal do monitor. Depois, no terminal 1, execute `kill $(jobs -pr)`.

## Verificar os tópicos

Com os detectores e o decisor em execução, use um terminal com o ambiente carregado:

```bash
ros2 node list
ros2 topic echo /deteccoes
ros2 topic echo /papeis
```

Cada `ros2 topic echo` continua mostrando mensagens até você pressionar `Ctrl+C`; execute um por vez.
