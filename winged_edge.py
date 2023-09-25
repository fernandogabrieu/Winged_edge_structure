#autor: Fernando Gabriel
###############################################################
##################### FUNÇÕES DE CONSULTA #####################
###############################################################

def consulta_faces_compartilham_aresta(edge_list):
    #Solicita ao usuário os índices dos vértices que compõem a aresta
    index1 = int(input("Digite o índice do primeiro vértice: "))
    index2 = int(input("Digite o índice do segundo vértice: "))

    #Encontra a aresta correspondente na lista de arestas
    matching_edges = [edge for edge in edge_list if
                      (edge.vertex1 == index1 and edge.vertex2 == index2) or
                      (edge.vertex1 == index2 and edge.vertex2 == index1)]

    if not matching_edges:
        print("A aresta não foi encontrada.")
        return

    print("Faces que compartilham a aresta:")
    for edge in matching_edges:
        if edge.face_left:
            print(f"Face esquerda: {edge.face_left.edge1.vertex1, edge.face_left.edge2.vertex1, edge.face_left.edge3.vertex1}")
        if edge.face_right:
            print(f"Face direita: {edge.face_right.edge1.vertex1, edge.face_right.edge2.vertex1, edge.face_right.edge3.vertex1}")

#------------------------------------------------------#
def consulta_arestas_compartilham_vertice(vertex_list):
    #Solicita ao usuário o índice do vértice de interesse
    index = int(input("Digite o índice do vértice: "))

    #Encontra o vértice correspondente na lista de vértices
    target_vertex = None
    for vertex in vertex_list:
        if vertex.index == index:
            target_vertex = vertex
            break

    if target_vertex is None:
        print("O vértice não foi encontrado.")
        return

    # Acessa as arestas que incidem no vértice
    incident_edges = target_vertex.incident_edges

    print("Arestas que compartilham o vértice:")
    for edge in incident_edges:
        print(edge.vertex1, edge.vertex2)

#------------------------------------------------------#
def consulta_vertices_compartilham_face(face_list):
    #Solicita ao usuário o número da face de interesse
    face_number = int(input("Digite o número da face: "))

    # Verifica se o número da face está dentro dos limites
    if face_number < 1 or face_number > len(face_list):
        print("Número de face inválido.")
        return

    #Acessa a face de interesse
    target_face = face_list[face_number - 1]

    #Acessa as arestas da face e, em seguida, os vértices dessas arestas
    edges = [target_face.edge1, target_face.edge2, target_face.edge3]

    print("Vértices que compartilham a face:")
    for edge in edges:
        print([edge.vertex1, edge.vertex2])

###############################################################
########################## CLASSES ############################
###############################################################

class Vertex:
    def __init__(self, x = float, y = float, z= float, index = int):
        self.x = x
        self.y = y
        self.z = z
        self.index = index
        self.incident_edges = []

class Edge:
    def __init__(self, vertex1 = int, vertex2 = int):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.face_left = None
        self.face_right = None
        self.edge_left_pre = None
        self.edge_left_suc = None
        self.edge_right_pre = None
        self.edge_right_suc = None
        self.label = [vertex1, vertex2]

class Face:
    def __init__(self, edge1 = Edge, edge2 = Edge, edge3 = Edge):
        self.edge1 = edge1
        self.edge2 = edge2
        self.edge3 = edge3
        self.label = [edge1.vertex1, edge1.vertex1, edge3.vertex1]
   
vertex_list = []
face_list  = []
edge_list  = []

###########################################################################
########### FUNÇÃO QUE PROCESSA O ARQUIVO OBJ E CRIA OS OBJETOS ###########
###########################################################################

def parse_obj_file(filename):
    i = 0
    vetor_auxiliar = []
    with open(filename, "r") as arquivo:
        obj = arquivo.readlines()
    for line in obj:                        #fazendo varredura de cada linha do arquivo
        element = line.strip().split()      #cada string/int/item da linha é coloca em um vetor element

        if not element:
            continue

        if element[0] == "v":               #se o primeiro elemento do vetor for v, então estamos na notação de vértice (v,  0.0,  0.0,  0.0)
            i += 1
            x, y, z = map(float, element[1:])
            vertex = Vertex(x, y, z, i)     #crio então um objeto Vertex com coordenadas x, y e z
            vertex_list.append(vertex)      #coloco esse objeto na lista de vértices

        if element[0] == "f":               #se o primeiro elemento do vetor for f, então estamos na notação de face (f  1//2  7//2  5//2)
                                            # e com isso vamos construir as arestas além das faces.

            #separo cada índice dos vértices referentes a respectiva face (1, 7, 5)
            vertex_indices = [int(part.split("//")[0]) for part in element[1:]]

            #crio uma aresta → objeto Edge(1, 7)
            edge1 = Edge(vertex_indices[0], vertex_indices[1])
            vertex_list[vertex_indices[0]-1].incident_edges.append(edge1)

            #verifico se já não existe uma aresta com esses vértices na lista de arestas considerando a reversão (1,7) = (7,1)
            if ([vertex_indices[1], vertex_indices[0]] and [vertex_indices[0], vertex_indices[1]]) not in vetor_auxiliar:
                #adiciono essa aresta na lista de arestas edge_list
                edge_list.append(edge1)
                #adiciono os índices no vetor de controle para evitar arestas duplicadas
                vetor_auxiliar.append([vertex_indices[1], vertex_indices[0]])
                vetor_auxiliar.append([vertex_indices[0], vertex_indices[1]])

            #crio uma aresta → objeto Edge(7, 5)
            edge2 = Edge(vertex_indices[1], vertex_indices[2])
            vertex_list[vertex_indices[1]-1].incident_edges.append(edge2)

            #verifico se já não existe uma aresta com esses vértices (7,5) e (5,7)
            if ([vertex_indices[2], vertex_indices[1]] and [vertex_indices[1], vertex_indices[2]]) not in vetor_auxiliar:
                #adiciono essa aresta na lista de arestas edge_list
                edge_list.append(edge2)
                #adiciono os índices no vetor de controle para evitar arestas duplicadas
                vetor_auxiliar.append([vertex_indices[2], vertex_indices[1]])
                vetor_auxiliar.append([vertex_indices[1], vertex_indices[2]])

            #crio uma aresta → objeto Edge(5, 1)
            edge3 = Edge(vertex_indices[2], vertex_indices[0])
            vertex_list[vertex_indices[2]-1].incident_edges.append(edge3)

            #verifico se já não existe uma aresta com esses vértices (5,1) e (1,5)
            if ([vertex_indices[0], vertex_indices[2]] and [vertex_indices[2], vertex_indices[0]]) not in vetor_auxiliar:
                #adiciono essa aresta na lista de arestas edge_list
                edge_list.append(edge3)
                #adiciono os índices no vetor de controle para evitar arestas duplicadas
                vetor_auxiliar.append([vertex_indices[2], vertex_indices[0]])
                vetor_auxiliar.append([vertex_indices[0], vertex_indices[2]])
            
            #Criando os objetos Face
            face = Face(edge1, edge2, edge3)
            face_list.append(face) 

    #Associo as arestas às faces direita e esquerda
    for face in face_list:
        #print('Analisando face ' ,  face.edge1.vertex1, face.edge2.vertex1, face.edge3.vertex1)
        for edge in edge_list:
            #print('Analisando edge ' ,  edge.vertex1, edge.vertex2)
            if  (edge.vertex1, edge.vertex2) == (face.edge1.vertex1, face.edge2.vertex1) or (edge.vertex1, edge.vertex2) == (face.edge2.vertex1, face.edge3.vertex1) or (edge.vertex1, edge.vertex2) == (face.edge3.vertex1, face.edge1.vertex1) or (edge.vertex2, edge.vertex1) == (face.edge1.vertex1, face.edge2.vertex1) or (edge.vertex2, edge.vertex1) == (face.edge2.vertex1, face.edge3.vertex1) or (edge.vertex2, edge.vertex1) == (face.edge3.vertex1, face.edge1.vertex1):
                if edge.face_left is None:
                    edge.face_left = face
                elif edge.face_right is None:
                    edge.face_right = face
                else:
                    # Se a aresta já possui duas faces associadas, pare de procurar
                    break
    #print(len(vertex_list))
    #print(len(edge_list))
    #print(len(face_list))
    return vertex_list, edge_list, face_list

###########################################################################
############################# FUNÇÃO MAIN #################################
###########################################################################

def main():
  
  vertex_list, edge_list, face_list = parse_obj_file("cube.txt")

  while True:
    print("\nEscolha uma opção:")
    print("1. Consultar as faces que compartilham uma determinada aresta")
    print("2. Consultar as arestas que compartilham um determinado vértice")
    print("3. Consultar os vértices que compartilham uma determinada face")
    print("4. Sair")
    
    opcao = input("Opção: ")

    if opcao == "1":
        consulta_faces_compartilham_aresta(edge_list)
    elif opcao == "2":
        consulta_arestas_compartilham_vertice(vertex_list)
    elif opcao == "3":
        consulta_vertices_compartilham_face(face_list)
    elif opcao == "4":
        print("Saindo do programa.")
        break
    else:
        print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()