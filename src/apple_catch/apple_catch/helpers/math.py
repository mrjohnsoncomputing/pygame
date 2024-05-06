class Math:
    
    @staticmethod
    def roundto(x: float, base: int=5) -> int:
        return base * round(x/base)