¿Bajó más el error al añadir dos capas, o se estancó / empeoró? ¿Igual en NumPy y en Keras?
No, añadir más capas no mejoró el rendimiento; al contrario, en la implementación manual (04) la curva de error se estancó a un nivel más alto (0.30) en comparación con la red original de dos capas, que lograba descender mucho más. En Keras pasó algo similar: la pérdida (loss) se quedó plana alrededor de 0.2221 en la red profunda, mientras que en la original bajaba un poco más.
¿Las curvas de la notebook 04 y de Keras se parecen con la misma topología? Si no, ¿qué diferencias de implementación podrían explicarlo?
No son idénticas. Aunque ambas muestran una tendencia descendente general, la implementación en NumPy genera una curva de error más pronunciada y con un valor final distinto a la de Keras.

Con sigmoides apiladas y MSE, ¿tiene sentido que una red más profunda no aprenda mejor en Iris? Relaciónalo con lo que viste en las gráficas.
Si, el conjunto de datos Iris es un problema pequeño y relativamente sencillo. Al apilar múltiples capas con funciones de activación sigmoide junto con el error cuadrático medio, los valores de la derivada de la sigmoide son pequeños, y al multiplicarse a través de tantas capas en la retropropagación, los gradientes llegan casi a cero en las capas iniciales, impidiendo que la red aprenda eficazmente y provocando que la curva de error se estanque.
