Bueno, el compas tiene una cierta cantidad de beats/tempos. La nota redonda es la tipo nota mas larga.

1. La cifra de indcador de compás.
Lo primero es mirar los dos números al principio del pentagrama. (como $4 over 4$ o $3 over 4$)
- El número de arriba: te dice cuántos pulsos (beats) hay en cada compás.
- El número de abajo te dice que tipo de nota equivale a un pulso.

2. ¿Quien vale un pulso? (El número de abajo)
El número de abjo representa una fracción de la redonda. (que es la unidad total):
    - $compas over 1$ = Redonda
    - $compas over 2$ = Blanca
    - $compas over 4$ = Negra
    - $compas over 8$ = Corchea

Cómo obtener la cantidad de beats.
- En un $4 over 4$:
    - El número de arriba es 4, así que hay **4 pulsos**.
    - El número de abajo es 4, así que cada pulso es **Negra**.
    - **Resultado: El compás se llega con 4 negras. Una blanca aquí duraria 2 pulsos (la mitad del compás)**
- En un $3 over 4$:
    - El número de arriba es 3, así que hay **3 pulsos**.
    - El número de abajo es 4, así que cada pulso es una **Negra**
    - **Resultado: El compás se llega con 3 negras. Una blanca aquí duraria 2 pulsos (el 66.6% del compas)**

---
```python3
def get_beats_in_compass( numerator, denominator ):
    notes = {
        1: "round",
        2: "white",
        4: "black",
        8: "quaver",
        16: "semiquaver"
    }

    #if denominator in notes.keys():
    beat_compass_value = numerator * (1 / denominator)
    count_beats  = True
    beats = 1
    while count_beats:
        if (beat_compass_value*beats) == numerator:
            count_beats = False
        else:
            beats += 1
    return beats
```
