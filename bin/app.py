# -*- coding: utf- 8 -*-

import web
from random import randint
from f2fweb import map
from f2fweb import f2f_config


web.config.debug = False


urls = (
    '/', 'Index',
    '/game', 'GameEngine',
    '/attack', 'Attack',
    '/robodogs', 'Robodogs',
)


app = web.application(urls, locals())
store = web.session.DiskStore('sessions')


# Store session data in folder 'sessions' under the same directory as your app.
session = web.session.Session(app, store, initializer={'scene': None})
render = web.template.render('templates/', base="layout")


class Index:
    def GET(self):
        return render.index()

    def POST(self):
        level = web.input()
        print(level.level)

        if level.level == '1':
            f2f_config.HERO_HEALTH = 25
            f2f_config.HERO_GUN = 50
            f2f_config.VILLAIN_HEALTH = 5
            f2f_config.VILLAIN_GUN = 10
            f2f_config.MAX_ROBODOGS = 5
            f2f_config.HERO_HEALTH_LEAK = 1
            game_level = 'Легко'
        elif level.level == '2':
            f2f_config.HERO_HEALTH = 20
            f2f_config.HERO_GUN = 35
            f2f_config.VILLAIN_HEALTH = 10
            f2f_config.VILLAIN_GUN = 15
            f2f_config.MAX_ROBODOGS = 10
            f2f_config.HERO_HEALTH_LEAK = 2
            game_level = 'Нормально'
        else:
            f2f_config.HERO_HEALTH = 15
            f2f_config.HERO_GUN = 20
            f2f_config.VILLAIN_HEALTH = 15
            f2f_config.VILLAIN_GUN = 20
            f2f_config.MAX_ROBODOGS = 15
            f2f_config.HERO_HEALTH_LEAK = 3
            game_level = 'Сложно'
        # используется для "настройки" сеанса с начальными значениями
        map.restart_game()
        session.scene = map.a_map.opening_scene()
        return render.level_setup(level=game_level, health=f2f_config.HERO_HEALTH, gun=f2f_config.HERO_GUN)


class GameEngine:

    choice_form = web.form.Form(
        web.form.Button("choice", value="escape", html="Попробовать убежать"),
        web.form.Button("choice", value="attack", html="Атаковать Пожирателя"),
        web.form.Button("choice", value="story", html="Посмотреть уровень сил"),
        web.form.Button("choice", value="robodogs", html="Искать аптечку"),
    )

    def GET(self):
        if session.scene:
            return render.show_story_scene(scene=session.scene, form=self.choice_form, health='')

    def POST(self):
        # Check the type of the scene object now the game at and render the needed scene template.
        # Leaving a Story scene
        if type(session.scene) == map.f2f_scenes.Story:
            # Get the data sent with POST from the webpage.
            form = web.input()

            if session.scene and form.choice:
                # Put the next scene object to session.scene.
                session.scene = map.a_map.next_scene(form.choice, str(session.scene.branch))
                # Button to escape is pressed
                if form.choice == 'escape':
                    return render.show_escape_scene(scene=session.scene)
                # Button to attack is pressed
                if form.choice == 'attack':
                    return render.show_attack_scene(scene=session.scene)

                # Button to heal is pressed
                if form.choice == 'robodogs':
                    return render.show_robodogs_scene(scene=session.scene)

                # Button to check the health is pressed

                if form.choice == 'story':
                    health = f'Ваш уровень сил равен !{session.scene.hero.health}!'
                    return render.show_story_scene(scene=session.scene, form=self.choice_form, health=health)


        # Leaving an Escape scene.
        elif type(session.scene) == map.f2f_scenes.EscapeScene:
            form = web.input(death=None, victory=None, story=None)
            # Check what button is pushed and put the needed type of a scene to session.scene.
            if session.scene and form.story:
                if session.scene.hero.health <= 0:
                    session.scene = map.a_map.next_scene('death', '35')  # !!!!!!!!!
                    return render.show_death_scene(scene=session.scene)
                else:
                    session.scene = map.a_map.next_scene('story', str(form.story))# !!!!!!!!!
                    session.scene.hero.health -= f2f_config.HERO_HEALTH_LEAK
                    return render.show_story_scene(scene=session.scene, form=self.choice_form, health='') # !!!!!!!!!
            elif session.scene and form.death:
                session.scene = map.a_map.next_scene('death', str(form.death)) # !!!!!!!!!
                return render.show_death_scene(scene=session.scene)
            elif session.scene and form.victory:
                session.scene = map.a_map.next_scene('victory', str(form.victory)) # !!!!!!!!!
                return render.show_victory_scene(scene=session.scene)



        elif type(session.scene) == map.f2f_scenes.AttackDevourer:
            print('AttackDevourer!!!!!')



        elif type(session.scene) == map.f2f_scenes.Robodogs:
            print('Robodogs!!!!!')



        elif type(session.scene) == map.f2f_scenes.Victory:
            print('Victory!!!!!')



        else:
            print('Death!!!!!')


        web.seeother("/game")


class Attack:

    fire_form = web.form.Form(
        web.form.Button("fire_btn", value="fire", html="Пли!"),
    )
    victory_form = web.form.Form(
        web.form.Button("continue_btn", value="victory", html="Вперед!"),
    )
    death_form = web.form.Form(
        web.form.Button("continue_btn", value="death", html="Вперед!"),
    )
    escape_form = web.form.Form(
        web.form.Button("continue_btn", value="escape", html="Вперед!"),
    )

    def GET(self):




        # Set up 2 parts of the text for displaying at the webpage of show_attack_action_scene
        text = ''
        next_scene = ''

        # The hero's gun is not empty
        if session.scene.hero.gun > 0:
            hero_shots_done = randint(1, session.scene.hero.gun)
            session.scene.hero.use_gun(hero_shots_done)
            hero_shots_effective = hero_shots_done // randint(1, 3)
            session.scene.villain.health_down(hero_shots_effective)
            text = text + f'\n\tВы произвели выстрел, сократив свой боезапас на {hero_shots_done} зарядов, ' \
                            f'но только {hero_shots_effective} достигло своей цели.'
            if session.scene.villain.health > 0:
                text = text + f'\n\tВаш текущий заряд бластера - {session.scene.hero.gun}. Уровень здоровья ' \
                                f'Пожирателя !{session.scene.villain.health}!'
            else:
                session.scene.villain.health = 0
        # The hero's gun is empty
        else:
            text = text + '\n\tЩелчок! Еще щелчок! Упс! Ваша обойма пуста! Теперь только чудо спасет вас!'

        if session.scene.villain.health <= 0:
            #     victory = True
            text = text + '\n\tОднако, этого хватило, чтобы вывести робота Пожирателя из строя и одержать победу!'
            next_scene = 'victory'

            return render.show_attack_action_scene(scene=session.scene, form=self.victory_form, text=text,
                                                   next_scene=next_scene)
        else:
            text = text + '\n\tПожиратель все еще опасен, он только, кажется, еще больше разозлился и жаждет ' \
                          'вашей смерти. \n\tЕго выстрел не заставил себя ждать.'
            if session.scene.villain.gun > 0:
                dev_shots_done = randint(1, session.scene.villain.gun)
                session.scene.villain.use_gun(dev_shots_done)
                dev_shots_effective = dev_shots_done // randint(2, 4)
                session.scene.hero.health_down(dev_shots_effective)
                text = text + f'\tПожиратель выпустил {dev_shots_done} ракет, но вам удалось увернуться ' \
                              f'от {dev_shots_done - dev_shots_effective} из них, однако, все ' \
                              f'же {dev_shots_effective} зацепили вас. \tУ Пожирателя ' \
                              f'осталось {session.scene.villain.gun} ракет. Ваш уровень сил ' \
                              f'!{session.scene.hero.health}!'
            else:
                text = text + '\n\tСлышен скрежет работающих механизмов Пожирателя, но ничего не происходит. Вы ' \
                              'не верите\n своему везению: у Пожирателя не осталось ракет. Однако, радоваться ' \
                              'пока не о чем: он ведь \n смертельно опасен и без своих ракет.'
                if session.scene.hero.health <= 0:
                    text = text + '\n\tВы истекаете кровью, '
                    next_scene = 'death'

                    return render.show_attack_action_scene(scene=session.scene, form=self.death_form, text=text,
                                                           next_scene=next_scene)
                else:
                    text = text + '\n\tВ этот раз вам повезло: вы ранены, но у вас есть шанс выстрелить еще раз!'

        print('session.scene.hero.gun =', session.scene.hero.gun, ' session.scene.villain.gun =', session.scene.villain.gun)
        if session.scene.hero.gun <= 0 and session.scene.villain.gun <= 0:
            text = text + '\n\tИ у вас и у Пожирателя не осталось боеприпасов. Вам повезло не погибнуть от ракет \n' \
                          'Пожирателя, но и вам не удалось его одолеть. Вам остается только снова бежать...'
            next_scene = 'escape'
            return render.show_attack_action_scene(scene=session.scene, form=self.escape_form, text=text,
                                                   next_scene=next_scene)
            #     return 'escape', str(session.scene.branch)
        return render.show_attack_action_scene(scene=session.scene, form=self.fire_form, text=text,
                                               next_scene='')

    def POST(self):

        form = web.input()

        if session.scene and form.continue_btn:
                # Put the next scene object to session.scene.
                #session.scene = map.a_map.next_scene(form.continue_btn, str(session.scene.branch))
                # Button to escape is pressed
            if form.continue_btn == 'victory':
                    # Put the next scene object to session.scene.
                session.scene = map.a_map.next_scene(form.continue_btn, '32') # !!!!!!!!!
                return render.show_victory_scene(scene=session.scene)
                # Button to attack is pressed
            elif form.continue_btn == 'death':
                session.scene = map.a_map.next_scene(form.continue_btn, '33') # !!!!!!!!!
                return render.show_death_scene(scene=session.scene)
            elif form.continue_btn == 'escape':
                session.scene = map.a_map.next_scene(form.continue_btn, str(session.scene.branch))# !!!!!!!!!

                return render.show_escape_scene(scene=session.scene)

                # Button to heal is pressed

                # Button to check the health is pressed


class Robodogs:

    choice_form = web.form.Form(
        web.form.Button("choice", value="escape", html="Попробовать убежать"),
        web.form.Button("choice", value="attack", html="Атаковать Пожирателя"),
        web.form.Button("choice", value="story", html="Посмотреть уровень сил"),
        web.form.Button("choice", value="robodogs", html="Искать аптечку"),
    )

    robodogs = randint(1, f2f_config.MAX_ROBODOGS)

    fire_form = web.form.Form(
        web.form.Button("fire_btn", value="fire", html="Пли!"),
    )

    death_form = web.form.Form(
        web.form.Button("continue_btn", value="death", html="Вперед!"),
    )
    story_form = web.form.Form(
        web.form.Button("continue_btn", value="story", html="Вперед!"),
    )

    def GET(self):

        # Entering the story scene according to the branch
        # Set up 2 parts of the text for displaying at the webpage of show_attack_action_scene
        text = ''
        next_scene = ''


        if session.scene.hero.gun > 0:
            # Shooting
            hero_shots_done = randint(1, session.scene.hero.gun)
            session.scene.hero.use_gun(hero_shots_done)
            # Reduce the effectiveness of shot by dividing all shots done by randomized number
            hero_shots_effective = hero_shots_done // randint(1, 3)
            text = text + f'\n\tВы произвели выстрел, сократив свой боезапас на {hero_shots_done} зарядов, но ' \
                          f'только \n{hero_shots_effective} достиг своей цели.'
            # Reduce the number of dogs by effective shots. The number of dogs cannot be negative.
            self.robodogs -= hero_shots_effective
            if self.robodogs <= 0:
                self.robodogs = 0
            else:
                text = text + f'\tВаш текущий заряд бластера - !{session.scene.hero.gun}! Теперь в стае робопсов ' \
                              f'осталось {self.robodogs} особей.'
        else:
            text = text + '\tЩелчок! Еще щелчок! Упс! Ваша обойма пуста! Тперь только чудо спасет вас!'

        # If all robodogs are killed, the hero collects the aid kits and cartridges to charge the gun.
        if self.robodogs <= 0:
            aid_kits = randint(0, 10)
            session.scene.hero.health_up(aid_kits)
            shots_found = randint(0, 10)
            session.scene.hero.charge_gun(shots_found)
            text = text + f'\tОднако, этого хватило, чтобы вывести всех робопсов из строя и одержать победу!\n' \
                          f'\tВы осматриваете ящики и находите кое-что из медикаментов и еды. Вы чувствуете прилив ' \
                          f'сил. \n\tТеперь ваш уровень сил - !{session.scene.hero.health}! \n\tВам несказанно везет:' \
                          f' вы находите среди ящиков несколько аккумуляторов, которые позволяют \nвам зарядить ваш ' \
                          f'бластер. Теперь у вас в обойме {session.scene.hero.gun} зарядов. Вы возвращаетесь назад, ' \
                          f'чтобы продолжить свой путь.'
            next_scene = 'story'
            return render.show_robodogs_action_scene(scene=session.scene, form=self.story_form, text=text,
                                                   next_scene=next_scene)
        else:
            text = text + '\n\tОставшиеся робопсы продолжают подступать к вам, сжимая круг и злобно лязгая железными ' \
                          'зубами.'
            if session.scene.hero.gun <= 0:
                text = text + '\tВаша обойма пуста и вы бросаетесь врукопашную.'
                session.scene.hero.health_down(self.robodogs * 2)
                if session.scene.hero.health <= 0:
                    session.scene.hero.health = 0
                    text = text + '\n\tУвы, но их слишком много...'
                    next_scene = 'death'
                    return render.show_robodogs_action_scene(scene=session.scene, form=self.death_form, text=text,
                                                             next_scene=next_scene)
                else:
                    text = text + f'\n\tВам удалось одолеть этих злобных тварей, но и вас здорово потрепали. Вы еле ' \
                                  f'уносите ноги, не найдя ни медикаментов, ни еды. \n\tТеперь ваш уровень сил ' \
                                  f'равен {session.scene.hero.health}, да еще и обойма пуста.'
                    next_scene = 'story'
                    return render.show_robodogs_action_scene(scene=session.scene, form=self.story_form, text=text,
                                                             next_scene=next_scene)
            else:
                if session.scene.hero.health > 0:
                    text = text + '\tУ вас еще есть заряд в бластере: еще не все потеряно!'
                    return render.show_robodogs_action_scene(scene=session.scene, form=self.fire_form, text=text,
                                                           next_scene='')

    def POST(self):

        form = web.input()

        if session.scene and form.continue_btn:
                # Put the next scene object to session.scene.
                # Button to escape is pressed
            if form.continue_btn == 'story':
                    # Put the next scene object to session.scene.
                session.scene = map.a_map.next_scene(form.continue_btn, str(session.scene.branch))
                return render.show_story_scene(scene=session.scene, form=self.choice_form, health='')
                # Button to attack is pressed
            elif form.continue_btn == 'death':
                session.scene = map.a_map.next_scene(form.continue_btn, '34')
                return render.show_death_scene(scene=session.scene)

                # Button to heal is pressed

                # Button to check the health is pressed


if __name__ == "__main__":
    app.run()
