from f2fweb import f2f_characters
from f2fweb import f2f_scenes
from f2fweb import f2f_config

a_hero = None
a_villain = None
a_map = None


# class Engine:
#
#     def __init__(self, scene_map):
#         self.scene_map = scene_map
#
#     # Start the game play
#     def play(self):
#         current_scene = self.scene_map.opening_scene()
#         # The hero dies if the health is down to zero
#         last_scene = self.scene_map.next_scene('death', '35')
#
#         while self.scene_map.hero.health >= 0:
#             next_scene_name, next_scene_var = current_scene.enter()
#             current_scene = self.scene_map.next_scene(next_scene_name, next_scene_var)
#
#         # не забыть вывести последнюю сцену
#         last_scene.enter()
#

class Map:

    # Types of scenes used with the names of classes for their initialization
    scenes = {
        'start': 'f2f_scenes.Story',
        'story': 'f2f_scenes.Story',
        'attack': 'f2f_scenes.AttackDevourer',
        'escape': 'f2f_scenes.EscapeScene',
        'death': 'f2f_scenes.Death',
        'victory': 'f2f_scenes.Victory',
        'robodogs': 'f2f_scenes.Robodogs',
    }

    def __init__(self, start_scene, start_scene_var, hero, villain):
        self.start_scene = start_scene
        self.start_scene_var = start_scene_var
        self.hero = hero
        self.villain = villain

    # Moving from scene to scene
    def next_scene(self, scene_name, variant=''):
        val = Map.scenes.get(scene_name)
        return eval(val + '(' + variant + ', self.hero, self.villain)')

    def opening_scene(self):
        return self.next_scene(self.start_scene, self.start_scene_var)


def restart_game():
    # Create characters
    global a_hero
    global a_villain
    global a_map
    a_hero = f2f_characters.Hero(f2f_config.HERO_GUN, f2f_config.HERO_HEALTH)
    a_villain = f2f_characters.Devourer(f2f_config.VILLAIN_GUN, f2f_config.VILLAIN_HEALTH)
    # Create a Map object with the starting scene attribute 'start' passed into
    a_map = Map('start', '1', a_hero, a_villain)
