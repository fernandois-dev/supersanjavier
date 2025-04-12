class StyleManager:
    _styles = None

    @classmethod
    def configure(cls, styles: dict):
        """
        Configura los estilos globales.
        Args:
            styles (dict): Un diccionario con los estilos iniciales.
        """
        cls._styles = styles

    @classmethod
    def get(cls, key: str, default=None):
        """
        Obtiene un estilo por su clave.
        Args:
            key (str): La clave del estilo.
            default: Valor por defecto si la clave no existe.
        Returns:
            El estilo correspondiente o el valor por defecto.
        """
        if cls._styles is None:
            raise RuntimeError("StyleManager no está configurado. Llama a 'StyleManager.configure()' primero.")
        return cls._styles.get(key, default)