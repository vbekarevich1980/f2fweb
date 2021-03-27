# Classes of characters

from random import randint


class Character:

    def __init__(self, gun, health):
        """Initiate the class with gun and health power with the help of setters for safe usage of these properties in
        the code.
        """
        self.__set_gun(gun)
        self.__set_health(health)

    def __get_gun(self):
        """Getter for the gun property."""
        return self.__gun

    def __set_gun(self, gun):
        """Setter for the gun property."""
        if gun < 0:
            self.__gun = 0
        else:
            self.__gun = gun

    # Using the method 'property' to access the property through the dot operator (.)
    gun = property(__get_gun, __set_gun)

    def __get_health(self):
        """Getter for the health property."""
        return self.__health

    def __set_health(self, health):
        """Setter for the health property."""
        self.__health = health

    # Using the method 'property' to access the property through the dot operator (.)
    health = property(__get_health, __set_health)

    def use_gun(self, shots_done):
        """Reduce the number of shots after the fire."""
        self.__set_gun(self.__gun - shots_done)

    def health_down(self, wounds):
        """Reduce the power of health after defeat."""
        self.__set_health(self.__health - wounds)


class Hero(Character):

    def charge_gun(self, shots_found):
        """Increase the number of shots after recharging."""
        self.gun += shots_found

    def health_up(self, aid_kits):
        """Increase the power of health after victory."""
        self.health += aid_kits


class Devourer(Character):

    def use_gun(self, shots_done):
        """Reduce the number of shots after the fire."""
        luck = randint(0, 1)
        if luck:
            self.gun -= shots_done
        else:
            self.gun -= shots_done * 2

    def health_down(self, wounds):
        """Reduce the power of health after defeat."""
        luck = randint(0, 1)
        if luck:
            self.health -= wounds
        else:
            self.health -= wounds * 2
