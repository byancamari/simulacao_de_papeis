# Eleição de papéis — ROS 2

Simulação de três robôs que detectam a distância até a bola e recebem os papéis de atacante, goleiro e apoio. Implementado em Python com `rclpy`.

## Escolhas

- Usei o parâmetro ROS 2 `robot_id` para rodar três instâncias do **mesmo detector**, com IDs 1, 2 e 3. Assim, não preciso manter um arquivo diferente para cada robô.
- Cada detector publica `robot_id,distância` em `/deteccoes`. O decisor guarda a distância mais recente de cada ID.
- O robô mais próximo vira **atacante**. Se houver empate, vence o menor ID. Dos dois restantes, o menor ID vira **goleiro** e o outro, **apoio**.
- O decisor publica **uma mensagem por robô** em `/papeis`, no formato `robot_id,papel,distância`. Incluí a distância para facilitar a conferência da escolha no monitor.
- O monitor reúne as três mensagens de cada decisão em uma linha. Como as distâncias mudam, o atacante pode mudar a cada ciclo.

## Compilar

Requer ROS 2 Jazzy e `colcon`. Depois de clonar o repositório, entre na pasta criada:

```bash
git clone https://github.com/byancamari/byancamari-simulacao_de_papeis.git
cd byancamari-simulacao_de_papeis
source /opt/ros/jazzy/setup.bash
colcon build --packages-select eleicao_papeis
source install/setup.bash
```

## Executar

No mesmo terminal, rode:

```bash
ros2 run eleicao_papeis detector --ros-args -p robot_id:=1 > /tmp/detector1.log 2>&1 &
ros2 run eleicao_papeis detector --ros-args -p robot_id:=2 > /tmp/detector2.log 2>&1 &
ros2 run eleicao_papeis detector --ros-args -p robot_id:=3 > /tmp/detector3.log 2>&1 &
ros2 run eleicao_papeis decisor > /tmp/decisor.log 2>&1 &
ros2 run eleicao_papeis monitor
```

O monitor mostra os papéis e as distâncias juntos. Para encerrar, pressione `Ctrl+C` e rode `kill $(jobs -pr)` no mesmo terminal.

## Conferir os tópicos

Em outro terminal, carregue `source "/home/lk/desafio 2/install/setup.bash"` e execute:

```bash
ros2 node list
ros2 topic echo /deteccoes
ros2 topic echo /papeis
```

O desempate foi testado com os robôs 1 e 2 a `2.0 m` e o robô 3 a `5.0 m`: o robô 1 virou atacante. Com distâncias aleatórias, também foi observada a troca do atacante entre os três robôs.
