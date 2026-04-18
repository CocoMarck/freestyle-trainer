import datetime, calendar

# Constantes
MULTIPLER_MILLISECOND = 1
MULTIPLER_SECOND = 1000
MULTIPLER_MINUTE = 60
MULTIPLER_HOUR = 60
MULTIPLER_DAY = 24

MILLISECOND = 1 * MULTIPLER_MILLISECOND
MILLISECOND_PER_SECOND = MILLISECOND * MULTIPLER_SECOND
MILLISECOND_PER_MINUTE = MILLISECOND_PER_SECOND * MULTIPLER_MINUTE
MILLISECOND_PER_HOUR = MILLISECOND_PER_MINUTE * MULTIPLER_HOUR
MILLISECOND_PER_DAY = MILLISECOND_PER_HOUR * MULTIPLER_DAY


# Diccionario
TIME_VALUES = {
    "millisecond": MILLISECOND,
    "second": MILLISECOND_PER_SECOND,
    "minute": MILLISECOND_PER_MINUTE,
    "hour": MILLISECOND_PER_HOUR,
    "day": MILLISECOND_PER_DAY
}

TIME_MULTIPLER = {
    "millisecond": MULTIPLER_MILLISECOND,
    "second": MULTIPLER_SECOND,
    "minute": MULTIPLER_MINUTE,
    "hour": MULTIPLER_HOUR,
    "day": MULTIPLER_DAY
}


def get_time( 
        value: int, value_type: str = "minute", convert_to: str = "hour"
    ):
    '''
    # Función milisegundos, segundos, minutos, horas, dias
    Obtener el valor en milisegundos, segundos, minutos, horas, o dias.
    
    Permite convertir el valor `x` de tipo `y` a tipo `z`. Donde los tipo `y` y `z`, pueden ser:
    - millisecond
    - second
    - minute
    - hour
    - day
    
    Parametros:
        Son tres parametros: `value: int | float`, `value_type: str`, y `convert_to: str`
    
    Ejemplo e uso
    ```python
    get_time( 60, "minute", "hour" )
    
    # Su resultado sera: 1.0
    ```
    
    Retunrs:
        *Por lo general devolvera un float, debido a la operación de conversión*
        int | float
    '''
    
    if ( value_type in TIME_VALUES.keys() ) and ( convert_to in TIME_VALUES.keys() ):
        millisecond_value = value*TIME_VALUES[value_type]
        
        if TIME_VALUES[value_type] != TIME_VALUES[convert_to]:
            ready_value = millisecond_value / TIME_VALUES[convert_to]
        elif TIME_VALUES[value_type] == TIME_VALUES[convert_to]:
            ready_value = value
        
        return ready_value

    else:
        return value
