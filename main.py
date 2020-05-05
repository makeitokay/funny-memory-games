import logging

from skill.skill import Skill

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

if __name__ == '__main__':
    skill = Skill()
    skill.start()
