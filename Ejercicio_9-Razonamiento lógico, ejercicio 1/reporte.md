El programa implementa un motor de inferencia lógica basado en cláusulas definidas para resolver un problema de acceso nocturno a una biblioteca. La arquitectura del software está dividida en herramientas lógicas fundamentales y dos algoritmos principales de razonamiento:

Forward chaining: Es un algoritmo dirigido por los datos. Itera en rondas evaluando todas las reglas contra los hechos conocidos al inicio de cada ciclo. Los descubrimientos de una ronda se incorporan a los hechos generales hasta que el sistema deja de producir nueva información.

Backward chaining: Es un algoritmo dirigido por la meta. Parte de una consulta específica (objetivo) y busca recursivamente hechos directos o reglas que la satisfagan. Utiliza una pila de visitados para cortar ciclos y descarta cualquier cálculo o regla que no sea estrictamente necesario para la consulta.

¿Por qué Becario(Ana) sale en el encadenamiento hacia adelante de AccesoNoche(Ana) y no en el de hacia atrás?
El forward chaining es un proceso dirigido por los datos que deduce absolutamente todas las consecuencias posibles de la base de conocimiento, por lo que genera Becario(Ana) de forma colateral. En cambio, el backward chaining es dirigido por la meta y solo explora los caminos estrictamente necesarios para resolver la consulta solicitada, omitiendo reglas e información que no necesita para probar el acceso.  

¿Por qué hacia atrás prueba R_miembro_est al buscar Miembro(Marta), si Marta es profesora?
Porque el algoritmo de backward chaining evalúa las reglas respetando estrictamente el orden en el que se encuentran declaradas en la tabla. Al aparecer la regla de estudiantes (R_miembro_est) antes que la de profesores (R_miembro_prof), el sistema intenta resolverla primero y falla al no encontrar el hecho de que Marta sea estudiante, antes de pasar a la regla correcta.   

Si se añade el hecho TieneCredencial(Luis) y se vuelve a preguntar AccesoNoche(Luis), ¿qué átomos nuevos aparecen y la consulta queda probada?
Al incorporar ese nuevo hecho, se activan las reglas correspondientes y aparecen los átomos nuevos Miembro(Luis), Becario(Luis) y AccesoNoche(Luis), provocando que la consulta de acceso nocturno para Luis quede completamente probada y resulte exitosa.
