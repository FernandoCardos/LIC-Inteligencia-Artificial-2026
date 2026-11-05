Reporte Ejercicio 7:

¿Por qué el codo prefiere k=4 si make_blobs usó 5 centros?
En el conjunto de datos original de Géron, los blobs situados en la parte inferior izquierda se encuentran demasiado cercanos entre sí. Esto provoca que el algoritmo de K-medias no logre distinguirlos como regiones independientes y los fusione, interpretándolos como un único clúster. En pocas palabras al estar tan pegaditos los interpreta como un mismo grupo. Por lo tanto, la inercia experimenta su punto de inflexión óptimo en k=4.

Con tus blobs separados, ¿el codo y la silueta coinciden en el mismo k? ¿Ese k es 5?
Sí. Al modificar las coordenadas en blob_centers para alejar los centros y asegurar que las cinco nubes de puntos sean distinguibles a simple vista, la curva de inercia (codo) y la gráfica del coeficiente de silueta coinciden claramente en señalar k=5 como el número óptimo de clústeres.
Valores de los 5 centros y 5 std utilizados:
-blob_centers = np.array([[0.2, 2.4], [-1.5, 3.3], [-1.8, 5.8], [-1.8, 1.8], [-1.8, 0.3]])   

-blob_std = np.array([0.1, 0.1, 0.1, 0.1, 0.1])   


Si el codo hubiera seguido en 4, ¿qué faltaría por mover?
Si el codo persistiera en k=4, significaría que la distancia entre los centros sigue siendo insuficiente en relación con su dispersión (blob_std), provocando solapamiento. Para solucionarlo, habría sido necesario incrementar aún más la distancia euclidiana entre los centros o reducir la desviación estándar de las nubes para garantizar fronteras de decisión bien definidas que K-medias pueda detectar.
