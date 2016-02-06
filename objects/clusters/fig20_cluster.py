# Code for generating figures of the article:
# "Behavioral Diversity Generation in Autonomous Exploration Through Reuse of Past Experience"
# by Fabien C. Y. Benureau and Pierre-Yves Oudeyer
# Licensed under the Open Science License (see http://fabien.benureau.com/openscience.html)

import experiments

from fig19_clusters import rgap


if __name__ == '__main__':
    experiments.run_exps(rgap(src_env='dov_ball45_0.kb'))