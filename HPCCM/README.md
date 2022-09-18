
# Desenvolvimento: Imagem de contêiner com HPCCM

Template HPCCM para geração de Dockerfile de container com a aplicação miniVite versão 1.2.


## Download da imagem

```bash
  docker pull iojoaomarcos/minivite
```


    
## Demonstração

Iniciar contêiner com o seguinte comando:

```bash
  sudo docker run minivite mpirun --allow-run-as-root -n [QTDD_SLOTS] /miniVite -l -n [NUM_NODES]
```
Sendo [QTDD_SLOTS] a quantidade de unidades alocáveis que o MPI poderá usar para lançar um
processo e [NUM_NODES] o número de vertices que o miniVite processará (e.g.: 1073), deverá trazer o seguinte resultado:

```bash
    Average time to generate 2146 random numbers using LCG (in s): 2.8382e-05

    -------------------------------------------------------
    Graph edge distribution characteristics
    -------------------------------------------------------
    Number of vertices: 1073
    Number of edges: 6972
    Maximum number of edges: 6972
    Average number of edges: 6972
    Expected value of X^2: 4.86088e+07
    Variance: 0
    Standard deviation: 0
    -------------------------------------------------------
    Time to generate distributed graph of 1073 vertices (in s): 0.0075624
    -------------------------------------------------------
    64-bit datatype
    -------------------------------------------------------
    Average total time (in s), #Processes: 0.00604968, 1
    Modularity, #Iterations: 0.74861, 12
    MODS (final modularity * average time): 0.00452886
    -------------------------------------------------------
```